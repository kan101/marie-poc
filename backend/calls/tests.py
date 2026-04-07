from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient

from calls.models import Call, Caller
from calls.management.commands.import_calls import get_duration, next_business_day_at_10


class CallerModelTests(TestCase):
    def setUp(self):
        self.caller = Caller.objects.create(
            first_name='Johanna',
            last_name='Schmidt',
            email='johanna.schmidt@gmail.com',
            phone_number='+49 152 11223456',
        )

    def test_full_name(self):
        self.assertEqual(self.caller.full_name, 'Johanna Schmidt')

    def test_str(self):
        self.assertEqual(str(self.caller), 'Johanna Schmidt')


class CallModelTests(TestCase):
    def setUp(self):
        self.caller = Caller.objects.create(
            first_name='Johanna',
            last_name='Schmidt',
            email='johanna.schmidt@gmail.com',
            phone_number='+49 152 11223456',
        )
        self.call = Call.objects.create(
            call_id='call_01',
            caller=self.caller,
            audio_file='call_01.wav',
            duration_seconds=125,
            caller_type='new_client',
            called_at=timezone.now(),
        )

    def test_duration_display(self):
        self.assertEqual(self.call.duration_display, '2:05')

    def test_duration_display_under_minute(self):
        self.call.duration_seconds = 45
        self.assertEqual(self.call.duration_display, '0:45')

    def test_str(self):
        self.assertIn('call_01', str(self.call))


class NextBusinessDayTests(TestCase):
    def test_weekday_returns_next_day(self):
        # Monday
        monday = timezone.now().replace(hour=15, minute=0)
        monday = monday - timedelta(days=monday.weekday()) 
        result = next_business_day_at_10(monday)
        self.assertEqual(result.weekday(), 1)  # Tuesday
        self.assertEqual(result.hour, 10)

    def test_friday_returns_monday(self):
        # Friday
        friday = timezone.now().replace(hour=15, minute=0)
        friday = friday - timedelta(days=friday.weekday()) + timedelta(days=4)
        result = next_business_day_at_10(friday)
        self.assertEqual(result.weekday(), 0)  # Monday
        self.assertEqual(result.hour, 10)

    def test_saturday_returns_monday(self):
        saturday = timezone.now().replace(hour=10, minute=0)
        saturday = saturday - timedelta(days=saturday.weekday()) + timedelta(days=5)
        result = next_business_day_at_10(saturday)
        self.assertEqual(result.weekday(), 0)  # Monday


class CallListAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.caller = Caller.objects.create(
            first_name='Johanna',
            last_name='Schmidt',
            email='johanna.schmidt@gmail.com',
            phone_number='+49 152 11223456',
        )
        self.call = Call.objects.create(
            call_id='call_01',
            caller=self.caller,
            audio_file='call_01.wav',
            duration_seconds=125,
            caller_type='new_client',
            called_at=timezone.now(),
            urgent=False,
            follow_up_sent=True,
        )

    def test_list_returns_200(self):
        res = self.client.get('/api/calls/')
        self.assertEqual(res.status_code, 200)

    def test_list_returns_calls(self):
        res = self.client.get('/api/calls/')
        self.assertEqual(res.data['count'], 1)

    def test_search_by_name(self):
        res = self.client.get('/api/calls/?search=Johanna')
        self.assertEqual(res.data['count'], 1)

    def test_search_no_match(self):
        res = self.client.get('/api/calls/?search=Nobody')
        self.assertEqual(res.data['count'], 0)

    def test_filter_urgent(self):
        # Non-urgent call should not appear when filtering for urgent
        res = self.client.get('/api/calls/?urgent=true')
        self.assertEqual(res.data['count'], 0)

    def test_filter_urgent_returns_urgent_calls(self):
        # Create an urgent call and verify it appears in the filter
        Call.objects.create(
            call_id='call_02',
            caller=self.caller,
            audio_file='call_02.wav',
            duration_seconds=60,
            caller_type='new_client',
            called_at=timezone.now(),
            urgent=True,
            follow_up_sent=False,
        )
        res = self.client.get('/api/calls/?urgent=true')
        self.assertEqual(res.data['count'], 1)

    def test_detail_returns_200(self):
        res = self.client.get(f'/api/calls/{self.call.id}/')
        self.assertEqual(res.status_code, 200)

    def test_detail_contains_transcript(self):
        self.call.transcript = 'Test transcript'
        self.call.save()
        res = self.client.get(f'/api/calls/{self.call.id}/')
        self.assertEqual(res.data['transcript'], 'Test transcript')

    def test_notes_patch(self):
        res = self.client.patch(
            f'/api/calls/{self.call.id}/notes/',
            {'notes': 'Follow up on Monday'},
            format='json',
        )
        self.assertEqual(res.status_code, 200)
        self.call.refresh_from_db()
        self.assertEqual(self.call.notes, 'Follow up on Monday')


class StatsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        caller = Caller.objects.create(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            phone_number='+49 123 456789',
        )
        Call.objects.create(
            call_id='call_01',
            caller=caller,
            audio_file='call_01.wav',
            duration_seconds=120,
            caller_type='new_client',
            called_at=timezone.now(),
            urgent=True,
            follow_up_sent=False,
        )
        Call.objects.create(
            call_id='call_02',
            caller=caller,
            audio_file='call_02.wav',
            duration_seconds=180,
            caller_type='existing_client',
            called_at=timezone.now(),
            urgent=False,
            follow_up_sent=True,
        )

    def test_stats_returns_200(self):
        res = self.client.get('/api/stats/')
        self.assertEqual(res.status_code, 200)

    def test_stats_total(self):
        res = self.client.get('/api/stats/')
        self.assertEqual(res.data['total_calls'], 2)

    def test_stats_urgent(self):
        res = self.client.get('/api/stats/')
        self.assertEqual(res.data['urgent'], 1)

    def test_stats_email_sent(self):
        res = self.client.get('/api/stats/')
        self.assertEqual(res.data['email_sent'], 1)

    def test_stats_avg_duration(self):
        res = self.client.get('/api/stats/')
        self.assertEqual(res.data['avg_duration_seconds'], 150)