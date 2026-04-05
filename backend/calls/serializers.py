from rest_framework import serializers
from .models import Call, Caller


class CallerSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Caller
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'phone_number']


class CallListSerializer(serializers.ModelSerializer):
    caller = CallerSerializer(read_only=True)
    duration_display = serializers.ReadOnlyField()

    class Meta:
        model = Call
        fields = [
            'id', 'call_id', 'caller', 'duration_seconds', 'duration_display',
            'called_at', 'summary', 'audio_file', 'caller_type','urgent',
            'urgent_reason',
            'follow_up_sent',
            'requires_appointment',
        ]


class CallDetailSerializer(serializers.ModelSerializer):
    caller = CallerSerializer(read_only=True)
    duration_display = serializers.ReadOnlyField()

    class Meta:
        model = Call
        fields = [
            'id', 'call_id', 'caller', 'duration_seconds', 'duration_display',
            'called_at', 'transcript', 'summary', 'notes', 'audio_file',
            'created_at', 'updated_at', 'caller_type','urgent',
            'urgent_reason',
            'follow_up_sent',
            'requires_appointment',
        ]


class CallNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = ['notes']