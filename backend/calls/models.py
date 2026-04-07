from django.db import models


class Caller(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)  # not all callers leave an email
    phone_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Call(models.Model):
    # Caller is a separate model — one person can call multiple times
    caller = models.ForeignKey(Caller, on_delete=models.CASCADE, related_name='calls')
    call_id = models.CharField(max_length=50, unique=True)  # ID from the recordings JSON
    audio_file = models.CharField(max_length=255)  # filename only, served from MEDIA_ROOT
    duration_seconds = models.IntegerField(default=0)
    called_at = models.DateTimeField()
    transcript = models.TextField(blank=True)  # populated by Whisper during import
    summary = models.TextField(blank=True)     # populated by AI during import
    notes = models.TextField(blank=True)       # editable by the lawyer in the dashboard
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Urgency and follow-up — set during import based on transcript analysis
    urgent = models.BooleanField(default=False)
    urgent_reason = models.TextField(blank=True)
    requires_appointment = models.BooleanField(default=False)  # true if caller left an email
    follow_up_sent = models.BooleanField(default=False)
    proposed_appointment = models.DateTimeField(null=True, blank=True)  # next business day

    CALLER_TYPE_CHOICES = [
        ('new_client', 'New Client'),
        ('existing_client', 'Existing Client'),
        ('opposing_party', 'Opposing Party'),
        ('unknown', 'Unknown'),
    ]
    caller_type = models.CharField(max_length=20, choices=CALLER_TYPE_CHOICES, default='unknown')

    class Meta:
        ordering = ['-called_at']  # most recent calls first

    @property
    def duration_display(self):
        m, s = divmod(self.duration_seconds, 60)
        return f"{m}:{s:02d}"

    def __str__(self):
        return f"{self.call_id} - {self.caller}"