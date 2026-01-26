"use client"

import { useState } from "react"
import { Navigation } from "@/components/navigation"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { GitCompare, ExternalLink, TrendingUp, TrendingDown, Minus } from "lucide-react"
import Link from "next/link"

interface ScanRecord {
  id: string
  date: string
  target: string
  environment: string
  scanType: string
  score: number
  previousScore: number | null
  findings: {
    critical: number
    high: number
    medium: number
    low: number
  }
}

const scanHistory: ScanRecord[] = [
  {
    id: "scan-007",
    date: "2025-12-26T10:42:00Z",
    target: "https://example-app.vercel.app",
    environment: "Production",
    scanType: "Full",
    score: 72,
    previousScore: 68,
    findings: { critical: 3, high: 7, medium: 15, low: 12 },
  },
  {
    id: "scan-006",
    date: "2025-12-25T14:30:00Z",
    target: "https://staging.example-app.vercel.app",
    environment: "Staging",
    scanType: "Quick",
    score: 68,
    previousScore: 65,
    findings: { critical: 4, high: 8, medium: 18, low: 10 },
  },
  {
    id: "scan-005",
    date: "2025-12-24T09:15:00Z",
    target: "https://example-app.vercel.app",
    environment: "Production",
    scanType: "Full",
    score: 65,
    previousScore: 70,
    findings: { critical: 5, high: 10, medium: 14, low: 11 },
  },
  {
    id: "scan-004",
    date: "2025-12-23T16:45:00Z",
    target: "https://dev.example-app.vercel.app",
    environment: "Development",
    scanType: "Quick",
    score: 70,
    previousScore: 70,
    findings: { critical: 2, high: 6, medium: 12, low: 15 },
  },
  {
    id: "scan-003",
    date: "2025-12-22T11:20:00Z",
    target: "https://example-app.vercel.app",
    environment: "Production",
    scanType: "Full",
    score: 62,
    previousScore: 58,
    findings: { critical: 6, high: 11, medium: 20, low: 8 },
  },
  {
    id: "scan-002",
    date: "2025-12-21T08:00:00Z",
    target: "https://staging.example-app.vercel.app",
    environment: "Staging",
    scanType: "Full",
    score: 58,
    previousScore: null,
    findings: { critical: 7, high: 12, medium: 22, low: 9 },
  },
]

const environmentColors: Record<string, string> = {
  Production: "bg-red-500/10 text-red-500 border-red-500/20",
  Staging: "bg-yellow-500/10 text-yellow-500 border-yellow-500/20",
  Development: "bg-blue-500/10 text-blue-500 border-blue-500/20",
}

export default function HistoryPage() {
  const [selectedScans, setSelectedScans] = useState<Set<string>>(new Set())

  const toggleScan = (id: string) => {
    const newSelected = new Set(selectedScans)
    if (newSelected.has(id)) {
      newSelected.delete(id)
    } else if (newSelected.size < 2) {
      newSelected.add(id)
    }
    setSelectedScans(newSelected)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  const getScoreTrend = (current: number, previous: number | null) => {
    if (previous === null) return { icon: Minus, color: "text-muted-foreground", diff: 0 }
    const diff = current - previous
    if (diff > 0) return { icon: TrendingUp, color: "text-green-500", diff }
    if (diff < 0) return { icon: TrendingDown, color: "text-red-500", diff }
    return { icon: Minus, color: "text-muted-foreground", diff: 0 }
  }

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-foreground">Scan History</h1>
            <p className="mt-2 text-muted-foreground">View and compare previous security scans.</p>
          </div>
          {selectedScans.size === 2 && (
            <Button>
              <GitCompare className="mr-2 h-4 w-4" />
              Compare Selected
            </Button>
          )}
        </div>

        {selectedScans.size > 0 && selectedScans.size < 2 && (
          <Card className="mb-6 border-primary/50 bg-primary/5">
            <CardContent className="p-4">
              <p className="text-sm text-muted-foreground">
                Select one more scan to compare ({selectedScans.size}/2 selected)
              </p>
            </CardContent>
          </Card>
        )}

        <div className="space-y-4">
          {scanHistory.map((scan) => {
            const trend = getScoreTrend(scan.score, scan.previousScore)
            const TrendIcon = trend.icon
            const totalFindings = scan.findings.critical + scan.findings.high + scan.findings.medium + scan.findings.low

            return (
              <Card
                key={scan.id}
                className={`border-border/50 transition-colors ${
                  selectedScans.has(scan.id) ? "border-primary bg-primary/5" : ""
                }`}
              >
                <CardContent className="p-6">
                  <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                    <div className="flex items-start gap-4">
                      <Checkbox
                        checked={selectedScans.has(scan.id)}
                        onCheckedChange={() => toggleScan(scan.id)}
                        className="mt-1"
                      />
                      <div className="space-y-2">
                        <div className="flex flex-wrap items-center gap-2">
                          <span className="font-mono text-sm text-muted-foreground">{scan.id}</span>
                          <Badge variant="outline" className={environmentColors[scan.environment]}>
                            {scan.environment}
                          </Badge>
                          <Badge variant="secondary">{scan.scanType} Scan</Badge>
                        </div>
                        <p className="text-sm text-foreground">{scan.target}</p>
                        <p className="text-sm text-muted-foreground">{formatDate(scan.date)}</p>
                      </div>
                    </div>

                    <div className="flex flex-wrap items-center gap-6">
                      {/* Score */}
                      <div className="text-center">
                        <div className="flex items-center gap-2">
                          <span className="text-3xl font-bold text-primary">{scan.score}</span>
                          <div className={`flex items-center ${trend.color}`}>
                            <TrendIcon className="h-4 w-4" />
                            {trend.diff !== 0 && (
                              <span className="text-sm font-medium">
                                {trend.diff > 0 ? "+" : ""}
                                {trend.diff}
                              </span>
                            )}
                          </div>
                        </div>
                        <p className="text-xs text-muted-foreground">Score</p>
                      </div>

                      {/* Findings Summary */}
                      <div className="flex items-center gap-2">
                        <div className="text-center">
                          <span className="text-lg font-semibold text-red-500">{scan.findings.critical}</span>
                          <p className="text-xs text-muted-foreground">Critical</p>
                        </div>
                        <div className="text-center">
                          <span className="text-lg font-semibold text-orange-500">{scan.findings.high}</span>
                          <p className="text-xs text-muted-foreground">High</p>
                        </div>
                        <div className="text-center">
                          <span className="text-lg font-semibold text-yellow-500">{scan.findings.medium}</span>
                          <p className="text-xs text-muted-foreground">Medium</p>
                        </div>
                        <div className="text-center">
                          <span className="text-lg font-semibold text-green-500">{scan.findings.low}</span>
                          <p className="text-xs text-muted-foreground">Low</p>
                        </div>
                      </div>

                    <Button variant="outline" size="sm" asChild>
                      <Link href={`/findings?scan_id=${scan.id}`}>
                        <ExternalLink className="mr-2 h-4 w-4" />
                        View Details
                      </Link>
                    </Button>

                    </div>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>
      </main>
    </div>
  )
}
