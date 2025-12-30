from django.contrib import admin
from .models import MQTTMessage, MQTTConfig


@admin.register(MQTTMessage)
class MQTTMessageAdmin(admin.ModelAdmin):
    list_display = ['topic', 'payload_preview', 'qos', 'timestamp']
    list_filter = ['topic', 'qos', 'timestamp']
    search_fields = ['topic', 'payload']
    readonly_fields = ['timestamp']
    
    def payload_preview(self, obj):
        return obj.payload[:100] + '...' if len(obj.payload) > 100 else obj.payload
    payload_preview.short_description = 'Payload'


@admin.register(MQTTConfig)
class MQTTConfigAdmin(admin.ModelAdmin):
    list_display = ['broker_host', 'broker_port', 'is_active', 'updated_at']
    list_filter = ['is_active', 'updated_at']

