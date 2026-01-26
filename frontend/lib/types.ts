// API Response wrapper
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    message: string;
    code?: string;
    details?: any;
  };
  message?: string;
}

// Scan Types
export type ScanType = 'quick' | 'full';
export type ScanStatus = 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED';
export type Environment = 'dev' | 'staging' | 'production';
export type Severity = 'critical' | 'high' | 'medium' | 'low' | 'info';
export type Category = 'headers' | 'tls' | 'cookies' | 'dast' | 'sast';

// Scan Request
export interface ScanRequest {
  target: string;
  scan_type: ScanType;
  environment?: Environment;
  github_repo?: string;
}

// Scan Response (when starting scan)
export interface ScanStartResponse {
  scan_id: string;
  status: ScanStatus;
  message: string;
}

// Issue
export interface Issue {
  name: string;
  description: string;
  severity: Severity;
  category: Category;
  cwe?: string;
  owasp?: string;
  recommendation: string;
  evidence?: string;
}

// Tool Result
export interface ToolResult {
  tool: string;
  category: Category;
  severity: {
    critical: number;
    high: number;
    medium: number;
    low: number;
    info: number;
  };
  issues: Issue[];
  execution_time: number;
  status: string;
  error?: string;
}

// Security Score
export interface SecurityScore {
  score: number;
  grade: string;
  summary: string;
  total_issues: number;
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
  breakdown: Record<string, number>;
}

// Recommendation
export interface Recommendation {
  priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  title: string;
  description: string;
  action: string;
}

// Scan Status Response
export interface ScanStatusResponse {
  scan_id: string;
  status: ScanStatus;
  target: string;
  scan_type: ScanType;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  error?: string;
  score?: {
    value: number;
    grade: string;
  };
}

// Scan Result Response
export interface ScanResultResponse {
  scan_id: string;
  user_id: string;
  target: string;
  scan_type: ScanType;
  environment?: Environment;
  status: ScanStatus;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  tool_results: ToolResult[];
  score: SecurityScore;
  recommendations: Recommendation[];
}

// Health Check Response
export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  stage: string;
}

// Severity color mapping
export const severityColors: Record<Severity, string> = {
  critical: 'destructive',
  high: 'destructive',
  medium: 'warning',
  low: 'secondary',
  info: 'default',
};

// Category display names
export const categoryNames: Record<Category, string> = {
  headers: 'HTTP Headers',
  tls: 'TLS/SSL',
  cookies: 'Cookies',
  dast: 'Dynamic Analysis',
  sast: 'Static Analysis',
};