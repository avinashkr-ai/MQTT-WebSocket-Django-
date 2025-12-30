from django.apps import AppConfig
import os


class MqttAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mqtt_app'
    
    def ready(self):
        # Start MQTT client when Django starts (only if not in migration)
        if os.environ.get('RUN_MAIN') != 'true':
            return
        try:
            import mqtt_app.mqtt_client
            mqtt_app.mqtt_client.start_mqtt_client()
        except Exception as e:
            # Log error but don't crash Django startup
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Could not start MQTT client: {e}")

