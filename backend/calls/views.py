from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import FileResponse, Http404
from django.conf import settings
from django.db.models import Avg
import os

from .models import Call, Caller
from .serializers import CallListSerializer, CallDetailSerializer, CallNotesSerializer


class CallListView(generics.ListAPIView):
    serializer_class = CallListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['caller__first_name', 'caller__last_name', 'caller__email', 'caller__phone_number']
    ordering_fields = ['called_at', 'duration_seconds']
    ordering = ['-called_at']

    def get_queryset(self):
        queryset = Call.objects.select_related('caller').all()
        return queryset


class CallDetailView(generics.RetrieveAPIView):
    serializer_class = CallDetailSerializer
    queryset = Call.objects.select_related('caller').all()


class CallNotesView(generics.UpdateAPIView):
    serializer_class = CallNotesSerializer
    queryset = Call.objects.all()
    http_method_names = ['patch']


class StatsView(APIView):
    def get(self, request):
        total = Call.objects.count()
        urgent = Call.objects.filter(urgent=True).count()
        email_sent = Call.objects.filter(follow_up_sent=True).count()
        no_action = Call.objects.filter(urgent=False, follow_up_sent=False).count()

        avg_duration = 0
        if total:
            avg_duration = Call.objects.aggregate(avg=Avg('duration_seconds'))['avg'] or 0

        return Response({
            'total_calls': total,
            'urgent': urgent,
            'email_sent': email_sent,
            'no_action': no_action,
            'avg_duration_seconds': round(avg_duration),
        })