import { useState, useCallback } from 'react';
import api from '@/lib/api';
import { 
  ScanRequest, 
  ScanStartResponse, 
  ScanStatusResponse, 
  ScanResultResponse 
} from '@/lib/types';

export function useScan() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Start scan
  const startScan = useCallback(async (request: ScanRequest) => {
    setLoading(true);
    setError(null);

    try {
      const response = await api.startScan(request);
      
      if (!response.success) {
        throw new Error(response.error?.message || 'Failed to start scan');
      }

      return response.data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Get scan status
  const getScanStatus = useCallback(async (scanId: string) => {
    setLoading(true);
    setError(null);

    try {
      const response = await api.getScanStatus(scanId);
      
      if (!response.success) {
        throw new Error(response.error?.message || 'Failed to get status');
      }

      return response.data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Get scan result
  const getScanResult = useCallback(async (scanId: string) => {
    setLoading(true);
    setError(null);

    try {
      const response = await api.getScanResult(scanId);
      
      if (!response.success) {
        throw new Error(response.error?.message || 'Failed to get result');
      }

      return response.data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Poll for scan completion
  const pollScanStatus = useCallback(async (
    scanId: string,
    onProgress?: (status: ScanStatusResponse) => void
  ) => {
    setLoading(true);
    setError(null);

    try {
      const response = await api.pollScanStatus(scanId, 2000, 60, onProgress);
      
      if (!response.success) {
        throw new Error(response.error?.message || 'Failed to poll status');
      }

      return response.data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    startScan,
    getScanStatus,
    getScanResult,
    pollScanStatus,
    loading,
    error,
  };
}