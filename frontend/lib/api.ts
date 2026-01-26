import { 
  ApiResponse, 
  ScanRequest, 
  ScanStartResponse, 
  ScanStatusResponse, 
  ScanResultResponse,
  HealthResponse 
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
const API_TIMEOUT = parseInt(process.env.NEXT_PUBLIC_API_TIMEOUT || '30000');

class ZentrionAPI {
  private baseUrl: string;
  private timeout: number;

  constructor() {
    this.baseUrl = API_BASE_URL;
    this.timeout = API_TIMEOUT;
    console.log('Initialized with baseUrl:', this.baseUrl);
  }

  /**
   * Generic fetch wrapper with timeout and error handling
   */
  private async fetchWithTimeout(
    url: string,
    options: RequestInit = {}
  ): Promise<Response> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      clearTimeout(timeoutId);
      return response;
    } catch (error: any) {
      clearTimeout(timeoutId);
      
      if (error.name === 'AbortError') {
        throw new Error('Request timeout - backend might be down');
      }
      
      throw error;
    }
  }

  /**
   * Parse API response
   */
  private async parseResponse<T>(response: Response): Promise<ApiResponse<T>> {
    try {
      const data = await response.json();
      
      if (!response.ok) {
        return {
          success: false,
          error: {
            message: data.error?.message || 'Request failed',
            code: data.error?.code,
            details: data.error?.details,
          },
        };
      }

      return data;
    } catch (error) {
      return {
        success: false,
        error: {
          message: 'Failed to parse response',
          details: error,
        },
      };
    }
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<ApiResponse<HealthResponse>> {
    try {
      console.log('[API] Health check');
      const response = await this.fetchWithTimeout(`${this.baseUrl}/health`);
      const result = await this.parseResponse<HealthResponse>(response);
      console.log('[API] Health check result:', result);
      return result;
    } catch (error: any) {
      console.error('[API] Health check failed:', error);
      return {
        success: false,
        error: {
          message: error.message || 'Failed to connect to backend',
          details: error,
        },
      };
    }
  }
  
  /**
   * Start a new security scan
   */
  async startScan(request: ScanRequest): Promise<ApiResponse<ScanStartResponse>> {
    try {
      console.log('[API] Starting scan:', request);
      const response = await this.fetchWithTimeout(`${this.baseUrl}/scan/start`, {
        method: 'POST',
        body: JSON.stringify(request),
      });
      
      const result = await this.parseResponse<ScanStartResponse>(response);
      console.log('[API] Scan started:', result);
      return result;
    } catch (error: any) {
      console.error('[API] Start scan failed:', error);
      return {
        success: false,
        error: {
          message: error.message || 'Failed to start scan',
          details: error,
        },
      };
    }
  }

  /**
 * Start scan and auto-poll until completion
 */
  async startAndTrackScan(
    request: ScanRequest,
    onProgress?: (status: ScanStatusResponse) => void
  ): Promise<ApiResponse<ScanResultResponse>> {
    const startRes = await this.startScan(request);

    if (!startRes.success || !startRes.data?.scan_id) {
      return {
        success: false,
        error: {
          message: 'Failed to start scan',
          details: startRes.error,
        },
      };
    }

    const scanId = startRes.data.scan_id;

    const statusRes = await this.pollScanStatus(
      scanId,
      2000,
      60,
      onProgress
    );

    if (!statusRes.success || statusRes.data?.status !== 'COMPLETED') {
      return {
        success: false,
        error: {
          message: 'Scan did not complete',
          details: statusRes.error,
        },
      };
    }

    return this.getScanResult(scanId);
  }


  /**
   * Get scan status
   */
  async getScanStatus(scanId: string): Promise<ApiResponse<ScanStatusResponse>> {
    try {
      console.log('[API] Getting scan status:', scanId);
      const response = await this.fetchWithTimeout(
        `${this.baseUrl}/scan/${scanId}/status`
      );
      const result = await this.parseResponse<ScanStatusResponse>(response);
      console.log('[API] Scan status:', result);
      return result;
    } catch (error: any) {
      console.error('[API] Get scan status failed:', error);
      return {
        success: false,
        error: {
          message: error.message || 'Failed to get scan status',
          details: error,
        },
      };
    }
  }

  /**
   * Get scan result
   */
  async getScanResult(scanId: string): Promise<ApiResponse<ScanResultResponse>> {
    try {
      console.log('[API] Getting scan result:', scanId);
      const response = await this.fetchWithTimeout(
        `${this.baseUrl}/scan/${scanId}/result`
      );
      const result = await this.parseResponse<ScanResultResponse>(response);
      console.log('[API] Scan result:', result);
      return result;
    } catch (error: any) {
      console.error('[API] Get scan result failed:', error);
      return {
        success: false,
        error: {
          message: error.message || 'Failed to get scan result',
          details: error,
        },
      };
    }
  }

  /**
   * Poll scan status until completed or failed
   */
  async pollScanStatus(
    scanId: string,
    intervalMs: number = 2000,
    maxAttempts: number = 60,
    onProgress?: (status: ScanStatusResponse) => void
  ): Promise<ApiResponse<ScanStatusResponse>> {
    let attempts = 0;

    while (attempts < maxAttempts) {
      const response = await this.getScanStatus(scanId);

      if (!response.success) {
        return response;
      }

      const status = response.data?.status;
      
      // Call progress callback if provided
      if (onProgress && response.data) {
        onProgress(response.data);
      }
      
      if (status === 'COMPLETED' || status === 'FAILED') {
        return response;
      }

      // Wait before next poll
      await new Promise(resolve => setTimeout(resolve, intervalMs));
      attempts++;
      
      console.log(`[API] Polling attempt ${attempts}/${maxAttempts} - Status: ${status}`);
    }

    return {
      success: false,
      error: {
        message: 'Scan timeout - maximum polling attempts reached',
        code: 'TIMEOUT',
      },
    };
  }
}

// Export singleton instance
const api = new ZentrionAPI();
export default api;