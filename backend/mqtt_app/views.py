"""
Views for MQTT app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.utils import timezone
from .models import MQTTMessage, MQTTConfig
from .serializers import MQTTMessageSerializer, MQTTConfigSerializer, MQTTStatusSerializer
from .mqtt_client import get_mqtt_client
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

logger = logging.getLogger(__name__)


class MQTTMessageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing MQTT messages (history)
    
    list: Get list of MQTT messages (paginated)
    retrieve: Get a specific MQTT message by ID
    """
    queryset = MQTTMessage.objects.all()
    serializer_class = MQTTMessageSerializer
    
    @swagger_auto_schema(
        operation_description="Get list of MQTT messages (history)",
        manual_parameters=[
            openapi.Parameter('topic', openapi.IN_QUERY, description="Filter by topic", type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of MQTT messages with optional topic filter"""
        queryset = self.get_queryset()
        
        # Filter by topic if provided
        topic = request.query_params.get('topic', None)
        if topic:
            queryset = queryset.filter(topic__icontains=topic)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MQTTConfigViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing MQTT configuration
    
    list: Get MQTT configurations
    create: Create new MQTT configuration
    retrieve: Get a specific MQTT configuration
    update: Update MQTT configuration
    destroy: Delete MQTT configuration
    """
    queryset = MQTTConfig.objects.all()
    serializer_class = MQTTConfigSerializer
    
    @swagger_auto_schema(
        operation_description="Get MQTT connection status",
        responses={200: MQTTStatusSerializer}
    )
    @action(detail=False, methods=['get'])
    def status(self, request):
        """Get current MQTT connection status"""
        mqtt_client = get_mqtt_client()
        status_data = mqtt_client.get_status()
        serializer = MQTTStatusSerializer(status_data)
        return Response(serializer.data)


@swagger_auto_schema(
    method='get',
    operation_description="Get MQTT connection status",
    responses={200: MQTTStatusSerializer}
)
@api_view(['GET'])
def mqtt_status(request):
    """Get MQTT connection status"""
    mqtt_client = get_mqtt_client()
    status_data = mqtt_client.get_status()
    serializer = MQTTStatusSerializer(status_data)
    return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    operation_description="Clear MQTT message history",
    responses={200: openapi.Response(description="History cleared successfully")}
)
@api_view(['POST'])
def clear_history(request):
    """Clear all MQTT message history"""
    deleted_count, _ = MQTTMessage.objects.all().delete()
    return Response({
        'message': f'Deleted {deleted_count} messages from history',
        'deleted_count': deleted_count
    }, status=status.HTTP_200_OK)

