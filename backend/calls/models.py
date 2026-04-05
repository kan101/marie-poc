from django.db import models


class Caller(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Call(models.Model):

    call_id = models.CharField(max_length=50, unique=True)
    caller = models.ForeignKey(Caller, on_delete=models.CASCADE, related_name='calls')
    audio_file = models.CharField(max_length=255)
    duration_seconds = models.IntegerField(default=0)
    called_at = models.DateTimeField()
    transcript = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    urgent = models.BooleanField(default=False)
    urgent_reason = models.TextField(blank=True)
    follow_up_sent = models.BooleanField(default=False)
    requires_appointment = models.BooleanField(default=False)

    class Meta:
        ordering = ['-called_at']

    CALLER_TYPE_CHOICES = [
        ('new_client', 'New Client'),
        ('existing_client', 'Existing Client'),
        ('opposing_party', 'Opposing Party'),
        ('unknown', 'Unknown'),
    ]

    caller_type = models.CharField(max_length=20, choices=CALLER_TYPE_CHOICES, default='unknown')
    
    @property
    def duration_display(self):
        m, s = divmod(self.duration_seconds, 60)
        return f"{m}:{s:02d}"

    def __str__(self):
        return f"{self.call_id} - {self.caller}"