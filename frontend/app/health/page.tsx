'use client';

import { useState } from 'react';
import api from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';

export default function HealthPage() {
  const [status, setStatus] = useState<'idle' | 'testing' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState<string>('Not tested yet');
  const [details, setDetails] = useState<any>(null);

  const testConnection = async () => {
    setStatus('testing');
    setMessage('Checking backend health...');
    setDetails(null);

    const response = await api.healthCheck();

    if (response.success) {
      setStatus('success');
      setMessage('✅ Backend is healthy');
      setDetails(response.data);
    } else {
      setStatus('error');
      setMessage('❌ Backend unreachable');
      setDetails(response.error);
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-3xl">
      <h1 className="text-3xl font-bold mb-4">Backend Health</h1>

      <Card className="p-6 space-y-4">
        <Button
          onClick={testConnection}
          disabled={status === 'testing'}
          className="w-full"
        >
          Check Health
        </Button>

        {status !== 'idle' && (
          <Alert variant={status === 'error' ? 'destructive' : 'default'}>
            <AlertDescription className="font-mono text-sm">
              {message}
            </AlertDescription>
          </Alert>
        )}

        {details && (
          <pre className="bg-muted p-4 rounded text-xs overflow-auto">
            {JSON.stringify(details, null, 2)}
          </pre>
        )}
      </Card>
    </div>
  );
}
