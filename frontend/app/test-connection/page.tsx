'use client';

import { useState } from 'react';
import api from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';

export default function TestConnectionPage() {
  const [status, setStatus] = useState<'idle' | 'testing' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState<string>('Not tested yet');
  const [details, setDetails] = useState<any>(null);

  const [scanStatus, setScanStatus] = useState<string | null>(null);
  const [scanResult, setScanResult] = useState<any>(null);

  /* -------------------- HEALTH CHECK -------------------- */
  const testConnection = async () => {
    setStatus('testing');
    setMessage('Testing connection to backend...');
    setDetails(null);

    try {
      const response = await api.healthCheck();

      if (response.success) {
        setStatus('success');
        setMessage('✅ Connection successful! Backend is running.');
        setDetails(response.data);
      } else {
        setStatus('error');
        setMessage('❌ Connection failed: ' + response.error?.message);
        setDetails(response.error);
      }
    } catch (error) {
      setStatus('error');
      setMessage('❌ Connection error');
      setDetails(error);
    }
  };

  /* -------------------- QUICK SCAN -------------------- */
  const startQuickScan = async () => {
    setStatus('testing');
    setMessage('🚀 Scan started...');
    setScanResult(null);
    setDetails(null);

    const response = await api.startAndTrackScan(
      {
        target: 'http://testphp.vulnweb.com',
        scan_type: 'quick',
      },
      (progress) => {
        setScanStatus(progress.status);
        setMessage(`🔄 Scan status: ${progress.status}`);
      }
    );

    if (response.success) {
      setStatus('success');
      setMessage('✅ Scan completed successfully');
      setScanResult(response.data);
    } else {
      setStatus('error');
      setMessage('❌ Scan failed');
      setDetails(response.error);
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <h1 className="text-3xl font-bold mb-2">Backend Connection Test</h1>
      <p className="text-muted-foreground mb-6">
        Test backend connectivity and run a quick security scan
      </p>

      <Card className="p-6 space-y-4">

        {/* Configuration Info */}
        <div className="space-y-2">
          <h3 className="font-semibold">Configuration</h3>
          <div className="text-sm space-y-1">
            <div className="flex justify-between">
              <span className="text-muted-foreground">Backend URL:</span>
              <code className="bg-muted px-2 py-1 rounded">
                {process.env.NEXT_PUBLIC_API_URL || 'Not configured'}
              </code>
            </div>
          </div>
        </div>

        {/* Buttons */}
        <Button
          onClick={testConnection}
          disabled={status === 'testing'}
          className="w-full"
        >
          Test Connection
        </Button>

        <Button
          onClick={startQuickScan}
          disabled={status === 'testing'}
          variant="secondary"
          className="w-full"
        >
          Run Quick Scan
        </Button>

        {/* Status Message */}
        {status !== 'idle' && (
          <Alert
            variant={
              status === 'success'
                ? 'default'
                : status === 'error'
                ? 'destructive'
                : 'default'
            }
          >
            <AlertDescription>
              <div className="font-mono text-sm">{message}</div>
            </AlertDescription>
          </Alert>
        )}

        {/* Scan Status */}
        {scanStatus && (
          <div className="text-sm font-mono text-muted-foreground">
            Current Scan Status: <strong>{scanStatus}</strong>
          </div>
        )}

        {/* Scan Result */}
        {scanResult && (
          <div className="mt-4">
            <h3 className="font-semibold mb-2">Scan Result</h3>
            <pre className="bg-muted p-4 rounded-lg overflow-auto text-xs">
              {JSON.stringify(scanResult, null, 2)}
            </pre>
          </div>
        )}

        {/* Error / Details */}
        {details && (
          <div className="mt-4">
            <h3 className="font-semibold mb-2">Details</h3>
            <pre className="bg-muted p-4 rounded-lg overflow-auto text-xs">
              {JSON.stringify(details, null, 2)}
            </pre>
          </div>
        )}
      </Card>
    </div>
  );
}
