#!/usr/bin/env python3
"""
Simple MQTT Publisher Script for Testing

This script publishes test messages to the HiveMQ Cloud MQTT broker.
Use this to test your Django MQTT subscriber and WebSocket application.

Usage:
    python test_publisher.py
"""

import paho.mqtt.client as mqtt
import json
import time
import ssl
from datetime import datetime

# MQTT Broker Configuration
BROKER_HOST = "fd6ad94a23dc48f7aadb2a1c9b3f5c65.s1.eu.hivemq.cloud"
BROKER_PORT = 8883
USERNAME = "test1234"
PASSWORD = "Test1234"

# ControlByWeb Configuration
DEVICE_ID = "000CC80630E0"  # Your ControlByWeb device ID (replace {deviceID} in topic)
CLIENT_ID = "000CC80630E0"  # Your clientID from ControlByWeb

# Topic pattern matching ControlByWeb configuration
# Topic: flash/sirens/{deviceID}/status
TOPIC_STATUS = f"flash/sirens/{DEVICE_ID}/status"

def on_connect(client, userdata, flags, rc):
    """Callback when connected to MQTT broker"""
    if rc == 0:
        print(f"✓ Connected to MQTT broker: {BROKER_HOST}:{BROKER_PORT}")
    else:
        print(f"✗ Connection failed with code {rc}")

def on_publish(client, userdata, mid):
    """Callback when message is published"""
    print(f"  ✓ Message published (mid: {mid})")

def publish_test_messages():
    """Publish test messages to MQTT broker"""
    
    # Create MQTT client
    client = mqtt.Client()
    client.username_pw_set(USERNAME, PASSWORD)
    
    # Set callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    # Enable TLS (required for port 8883)
    client.tls_set()
    client.tls_insecure_set(True)  # Disable certificate verification for development
    
    try:
        # Connect to broker
        print(f"Connecting to {BROKER_HOST}:{BROKER_PORT}...")
        client.connect(BROKER_HOST, BROKER_PORT, 60)
        client.loop_start()
        
        # Wait for connection
        time.sleep(2)
        
        print("\n" + "="*50)
        print("Publishing ControlByWeb test messages...")
        print("="*50 + "\n")
        
        # ControlByWeb payload format: { "clientID": "${clientID}", "status": "${alertvalue}", "vin": "${vin}"}
        # Test with different status values
        test_statuses = ["active", "inactive", "alert", "normal", "warning"]
        test_vins = ["VIN123456789", "VIN987654321", "VIN456789123", "VIN789123456", "VIN321654987"]
        
        for i in range(5):
            # ControlByWeb status message format
            status_data = {
                "clientID": CLIENT_ID,
                "status": test_statuses[i],
                "vin": test_vins[i]
            }
            
            topic = TOPIC_STATUS
            payload = json.dumps(status_data)
            
            result = client.publish(topic, payload, qos=0)
            print(f"Published to '{topic}':")
            print(f"  {payload}")
            print()
            
            # Wait before next message
            time.sleep(3)
        
        print("="*50)
        print("✓ All test messages published successfully!")
        print("="*50)
        print("\nCheck your Django backend logs and frontend to see the messages.")
        print(f"Frontend URL: http://localhost:3000")
        print(f"API Status URL: http://localhost:8000/api/mqtt/status/")
        
        # Wait a bit before disconnecting
        time.sleep(2)
        client.loop_stop()
        client.disconnect()
        
    except Exception as e:
        print(f"✗ Error: {e}")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    print("\n" + "="*50)
    print("MQTT Test Publisher - ControlByWeb Format")
    print("="*50)
    print(f"Broker: {BROKER_HOST}:{BROKER_PORT}")
    print(f"Username: {USERNAME}")
    print(f"Topic: {TOPIC_STATUS}")
    print(f"Client ID: {CLIENT_ID}")
    print("="*50 + "\n")
    
    publish_test_messages()

