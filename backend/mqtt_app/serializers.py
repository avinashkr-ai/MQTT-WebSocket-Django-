"""
Serializers for MQTT app
"""
from rest_framework import serializers
from .models import MQTTMessage, MQTTConfig


class MQTTMessageSerializer(serializers.ModelSerializer):
    """Serializer for MQTT messages"""
    class Meta:
        model = MQTTMessage
        fields = ['id', 'topic', 'payload', 'qos', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class MQTTConfigSerializer(serializers.ModelSerializer):
    """Serializer for MQTT configuration"""
    class Meta:
        model = MQTTConfig
        fields = ['id', 'broker_host', 'broker_port', 'username', 'topics', 'is_active', 'updated_at']
        read_only_fields = ['id', 'updated_at']


class MQTTStatusSerializer(serializers.Serializer):
    """Serializer for MQTT connection status"""
    connected = serializers.BooleanField()
    broker_host = serializers.CharField()
    broker_port = serializers.IntegerField()
    topics = serializers.ListField(child=serializers.CharField())

