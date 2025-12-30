'use client';

import { useWebSocket } from '@/hooks/useWebSocket';
import ConnectionStatusIndicator from './ConnectionStatus';
import MessageList from './MessageList';

export default function MQTTMessages() {
  const { connectionStatus, messages, clearMessages, lastMessage } = useWebSocket();

  return (
    <div className="min-h-screen bg-gray-100 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            MQTT WebSocket Monitor
          </h1>
          <p className="text-gray-600">
            Real-time monitoring of MQTT messages from ControlByWeb device
          </p>
        </div>

        <div className="mb-6">
          <ConnectionStatusIndicator status={connectionStatus} />
        </div>

        {lastMessage && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <h3 className="text-lg font-semibold text-blue-900 mb-2">Latest Message</h3>
            <div className="text-sm">
              <p><span className="font-medium">Topic:</span> {lastMessage.topic}</p>
              <p><span className="font-medium">Payload:</span> {typeof lastMessage.payload === 'object' ? JSON.stringify(lastMessage.payload) : lastMessage.payload}</p>
            </div>
          </div>
        )}

        <MessageList messages={messages} onClear={clearMessages} />
      </div>
    </div>
  );
}

