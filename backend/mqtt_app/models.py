from django.db import models


class MQTTMessage(models.Model):
    """Model to store MQTT messages (optional - for history)"""
    topic = models.CharField(max_length=255)
    payload = models.TextField()
    qos = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['topic']),
        ]
    
    def __str__(self):
        return f"{self.topic}: {self.payload[:50]}"


class MQTTConfig(models.Model):
    """Model to store MQTT configuration"""
    broker_host = models.CharField(max_length=255)
    broker_port = models.IntegerField(default=1883)
    username = models.CharField(max_length=255, blank=True)
    topics = models.CharField(max_length=1000, help_text="Comma-separated topics")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "MQTT Configuration"
        verbose_name_plural = "MQTT Configurations"
    
    def __str__(self):
        return f"{self.broker_host}:{self.broker_port}"

