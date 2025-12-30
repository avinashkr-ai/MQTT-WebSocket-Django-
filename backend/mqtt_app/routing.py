"""
WebSocket URL routing for mqtt_app
"""
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/mqtt/$', consumers.MQTTConsumer.as_asgi()),
]

