import json
import os
import random

import whisper
import wave
from openai import OpenAI
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from calls.models import Call, Caller


load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_duration(audio_path: str) -> int:
    with wave.open(audio_path, 'r') as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return round(frames / rate)

def next_business_day_at_10(from_dt):
    dt = from_dt + timedelta(days=1)
    while dt.weekday() >= 5:
        dt += timedelta(days=1)
    return dt.replace(hour=10, minute=0, second=0, microsecond=0)

def extract_info(transcript: str) -> dict:
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                'role': 'system',
                'content': (
                    'You are extracting structured information from a call transcript '
                    'between an AI phone assistant at a law firm and a caller. '
                    'Return only valid JSON with these fields: '
                    'caller_type (one of: new_client, existing_client, opposing_party, unknown), '
                    'summary (2-3 sentence summary of the call in English), '
                    'requires_appointment (boolean, true if caller leaves an email'
                    'urgent (boolean, true the caller explicitly stating the matter is urgent), '
                    'urgent_reason (1-2 sentences explaining your choice for your chouce for the urgent property. What in the transcript led to this decision.)'
                    'Do not include any explanation or markdown. '
                    'If the transcript is in German, still return the JSON fields in English.'
                )
            },
            {
                'role': 'user',
                'content': f'Transcript:\n{transcript}'
            }
        ],
        response_format={'type': 'json_object'},
    )
    return json.loads(response.choices[0].message.content)

def send_follow_up_email(call: Call) -> None:
    proposed = next_business_day_at_10(call.called_at)
    proposed_str = proposed.strftime('%A, %d %B at %I:%M %p')

    smtp_host = os.getenv('MAILTRAP_HOST')
    smtp_port = int(os.getenv('MAILTRAP_PORT', 2525))
    smtp_user = os.getenv('MAILTRAP_USER')
    smtp_password = os.getenv('MAILTRAP_PASSWORD')

    msg = MIMEMultipart('alternative')

    msg['From'] = smtp_user
    msg['To'] = call.caller.email
    msg['Subject'] = 'Your appointment with our law firm'

    body = f"""Hi {call.caller.first_name},

        Thank you for contacting our office. We have received your message and would like to schedule a consultation with you.

        We have provisionally booked an appointment for:

        {proposed_str}

        If this time does not work for you, please reply to this email or reschedule using the link below:

        [Calendly link]

        We look forward to speaking with you.

        Kind regards,
        Marie"""

    msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(build_email_html(call.caller.first_name, proposed_str), 'html'))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, call.caller.email, msg.as_string())


def build_email_html(first_name: str, proposed_str: str) -> str:
    return f"""
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; background: #f9f9f9; margin: 0; padding: 0; }}
                .container {{ max-width: 560px; margin: 40px auto; background: #ffffff; border-radius: 8px; overflow: hidden; border: 1px solid #e5e5e5; }}
                .header {{ background: #111111; padding: 24px 32px; }}
                .header h1 {{ color: #ffffff; font-size: 18px; margin: 0; font-weight: 600; }}
                .header p {{ color: #999999; font-size: 13px; margin: 4px 0 0; }}
                .body {{ padding: 32px; }}
                .body p {{ color: #444444; font-size: 15px; line-height: 1.6; margin: 0 0 16px; }}
                .slot {{ background: #f4f4f4; border-left: 4px solid #111111; padding: 16px 20px; margin: 24px 0; border-radius: 4px; }}
                .slot p {{ margin: 0; font-size: 16px; font-weight: 600; color: #111111; }}
                .reschedule {{ display: inline-block; margin-top: 8px; color: #555; font-size: 13px; }}
                .footer {{ padding: 16px 32px; border-top: 1px solid #e5e5e5; }}
                .footer p {{ color: #aaaaaa; font-size: 12px; margin: 0; }}
            </style>
            </head>
            <body>
            <div class="container">
                <div class="header">
                <h1>Marie</h1>
                <p>Legal AI Phone Assistant</p>
                </div>
                <div class="body">
                <p>Dear {first_name},</p>
                <p>Thank you for contacting our office. We have received your message and would like to schedule a consultation with you.</p>
                <p>We have provisionally booked an appointment for:</p>
                <div class="slot">
                    <p>{proposed_str}</p>
                </div>
                <p>If this time does not work for you, please reply to this email or use the link below to reschedule:</p>
                <a href="#" class="reschedule">Reschedule your appointment →</a>
                <p style="margin-top: 24px;">We look forward to speaking with you.</p>
                <p>Kind regards,<br><strong>Marie</strong><br>Legal AI Assistant</p>
                </div>
                <div class="footer">
                <p>This message was sent on behalf of your law firm by Marie, an AI phone assistant.</p>
                </div>
            </div>
            </body>
            </html>
            """

class Command(BaseCommand):
    help = 'Import and process calls from recordings JSON and wav files'

    def add_arguments(self, parser):
        parser.add_argument('json_path', type=str, help='Path to recordings JSON file')
        parser.add_argument('recordings_dir', type=str, help='Path to directory containing wav files')

    def handle(self, *args, **options):
        with open(options['json_path']) as f:
            data = json.load(f)

        Call.objects.all().delete()
        Caller.objects.all().delete()

        self.stdout.write('Loading Whisper model...')
        model = whisper.load_model('base')

        now = timezone.now()
        created = 0

        for rec in data['recordings']:
            call_id = rec['id']
            self.stdout.write(f'Processing {call_id}...')

            audio_path = os.path.join(options['recordings_dir'], rec['file'])

            # Transcribe
            try:
                transcript = model.transcribe(audio_path, language='de')['text']
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  Transcription failed: {e}'))
                transcript = ''

            # Extract structured info
            try:
                info = extract_info(transcript) if transcript else {}
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  Extraction failed: {e}'))
                info = {}

            # Caller from ground truth JSON
            exp = rec['expected']
            caller = Caller.objects.create(
                first_name=exp['first_name'],
                last_name=exp['last_name'],
                email=exp['email'],
                phone_number=exp['phone_number'],
            )

            called_at = now - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )

            call = Call.objects.create(
                    call_id=call_id,
                    caller=caller,
                    audio_file=rec['file'],
                    duration_seconds=get_duration(audio_path),
                    caller_type=info.get('caller_type', 'unknown'),
                    called_at=called_at,
                    transcript=transcript,
                    summary=info.get('summary', ''),
                    urgent=info.get('urgent', False),
                    urgent_reason=info.get('urgent_reason', ''),
                    requires_appointment=info.get('requires_appointment', False),
                )

            if call.requires_appointment:
                try:
                    send_follow_up_email(call)
                    call.follow_up_sent = True
                    call.save(update_fields=['follow_up_sent'])
                    self.stdout.write(self.style.SUCCESS(f'  Follow-up email sent to {caller.email}'))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'  Email failed: {e}'))
            else:
                self.stdout.write(f'  No action required')
            created += 1
            self.stdout.write(self.style.SUCCESS(f'  Done'))

        self.stdout.write(self.style.SUCCESS(f'\nImported {created} calls successfully.'))

