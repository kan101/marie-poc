from rest_framework import serializers
from .models import Call, Caller


class CallerSerializer(serializers.ModelSerializer):
    # full_name is a model property, ReadOnlyField exposes it without a dedicated serializer method
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Caller
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'phone_number']


class CallListSerializer(serializers.ModelSerializer):
    # Nested serializer — avoids a second API call to fetch caller details
    caller = CallerSerializer(read_only=True)
    # duration_display is a model property, exposed the same way as full_name
    duration_display = serializers.ReadOnlyField()

    class Meta:
        model = Call
        # Intentionally excludes transcript and notes — not needed for the list view
        # Keeping the payload light when rendering 20+ cards
        fields = [
            'id', 'call_id', 'caller', 'duration_seconds', 'duration_display',
            'called_at', 'summary', 'audio_file', 'caller_type', 'urgent',
            'urgent_reason', 'follow_up_sent', 'requires_appointment',
            'proposed_appointment',
        ]


class CallDetailSerializer(serializers.ModelSerializer):
    caller = CallerSerializer(read_only=True)
    duration_display = serializers.ReadOnlyField()

    class Meta:
        model = Call
        # Full payload including transcript and notes — used in the detail modal only
        fields = [
            'id', 'call_id', 'caller', 'duration_seconds', 'duration_display',
            'called_at', 'transcript', 'summary', 'notes', 'audio_file',
            'created_at', 'updated_at', 'caller_type', 'urgent',
            'urgent_reason', 'follow_up_sent', 'requires_appointment',
            'proposed_appointment',
        ]


class CallNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        # Dedicated serializer for PATCH /calls/:id/notes/ — limits what can be updated
        fields = ['notes']