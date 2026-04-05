from django.urls import path
from . import views

urlpatterns = [
    path('calls/', views.CallListView.as_view(), name='call-list'),
    path('calls/<int:pk>/', views.CallDetailView.as_view(), name='call-detail'),
    path('calls/<int:pk>/notes/', views.CallNotesView.as_view(), name='call-notes'),
    path('stats/', views.StatsView.as_view(), name='stats'),
]