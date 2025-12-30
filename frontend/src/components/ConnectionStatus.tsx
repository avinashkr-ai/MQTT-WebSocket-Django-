'use client';

import { ConnectionStatus } from '@/types/mqtt';

interface ConnectionStatusProps {
  status: ConnectionStatus;
}

export default function ConnectionStatusIndicator({ status }: ConnectionStatusProps) {
  const getStatusColor = () => {
    switch (status) {
      case 'connected':
        return 'bg-green-500';
      case 'connecting':
        return 'bg-yellow-500';
      case 'disconnected':
        return 'bg-gray-500';
      case 'error':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'connected':
        return 'Connected';
      case 'connecting':
        return 'Connecting...';
      case 'disconnected':
        return 'Disconnected';
      case 'error':
        return 'Error';
      default:
        return 'Unknown';
    }
  };

  return (
    <div className="flex items-center gap-2">
      <div className={`w-3 h-3 rounded-full ${getStatusColor()} animate-pulse`} />
      <span className="text-sm font-medium text-gray-700">{getStatusText()}</span>
    </div>
  );
}

