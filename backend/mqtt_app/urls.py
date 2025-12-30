"""
URL routing for mqtt_app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'messages', views.MQTTMessageViewSet, basename='mqttmessage')
router.register(r'config', views.MQTTConfigViewSet, basename='mqttconfig')

urlpatterns = [
    path('mqtt/', include(router.urls)),
    path('mqtt/status/', views.mqtt_status, name='mqtt-status'),
    path('mqtt/clear-history/', views.clear_history, name='clear-history'),
]

