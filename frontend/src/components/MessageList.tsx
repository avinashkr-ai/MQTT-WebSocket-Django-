'use client';

import { MQTTMessage } from '@/types/mqtt';

interface MessageListProps {
  messages: MQTTMessage[];
  onClear: () => void;
}

export default function MessageList({ messages, onClear }: MessageListProps) {
  const formatTimestamp = (timestamp?: string) => {
    if (!timestamp) return 'N/A';
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  const formatPayload = (payload: any) => {
    if (typeof payload === 'object') {
      return JSON.stringify(payload, null, 2);
    }
    return String(payload);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-gray-800">MQTT Messages</h2>
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-600">
            Total: {messages.length}
          </span>
          <button
            onClick={onClear}
            className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors"
          >
            Clear
          </button>
        </div>
      </div>

      {messages.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <p>No messages received yet.</p>
          <p className="text-sm mt-2">Waiting for MQTT messages...</p>
        </div>
      ) : (
        <div className="space-y-4 max-h-[600px] overflow-y-auto">
          {messages.map((message, index) => (
            <div
              key={index}
              className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors"
            >
              <div className="flex justify-between items-start mb-2">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="font-semibold text-blue-600">{message.topic}</span>
                    <span className="px-2 py-1 bg-gray-200 text-xs rounded">QoS: {message.qos}</span>
                  </div>
                  <div className="text-xs text-gray-500 mb-2">
                    {formatTimestamp(message.timestamp)}
                  </div>
                </div>
              </div>
              <div className="bg-gray-100 rounded p-3 mt-2">
                <pre className="text-sm text-gray-800 whitespace-pre-wrap break-words">
                  {formatPayload(message.payload)}
                </pre>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

