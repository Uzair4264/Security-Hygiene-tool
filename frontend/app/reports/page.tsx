"use client"

import { Navigation } from "@/components/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { FileText, FileJson, Download, Calendar, Target, Shield, AlertTriangle } from "lucide-react"

export default function ReportsPage() {
  const reportData = {
    generatedAt: "2025-12-26T10:42:00Z",
    target: "https://example-app.vercel.app",
    score: 72,
    totalFindings: 37,
    breakdown: {
      critical: 3,
      high: 7,
      medium: 15,
      low: 12,
    },
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      month: "long",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-foreground">Security Reports</h1>
          <p className="mt-2 text-muted-foreground">Generate and download security assessment reports.</p>
        </div>

        <div className="grid gap-6 lg:grid-cols-3">
          {/* Download Options */}
          <Card className="border-border/50 lg:col-span-2">
            <CardHeader>
              <CardTitle>Export Report</CardTitle>
              <CardDescription>Download your security assessment in your preferred format.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 sm:grid-cols-2">
                <Card className="border-border bg-secondary/30">
                  <CardContent className="flex flex-col items-center p-6 text-center">
                    <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-red-500/10">
                      <FileText className="h-8 w-8 text-red-500" />
                    </div>
                    <h3 className="mt-4 font-semibold text-foreground">PDF Report</h3>
                    <p className="mt-2 text-sm text-muted-foreground">
                      Professional formatted report suitable for stakeholders and compliance documentation.
                    </p>
                    <Button className="mt-4 w-full">
                      <Download className="mr-2 h-4 w-4" />
                      Download PDF
                    </Button>
                  </CardContent>
                </Card>

                <Card className="border-border bg-secondary/30">
                  <CardContent className="flex flex-col items-center p-6 text-center">
                    <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-yellow-500/10">
                      <FileJson className="h-8 w-8 text-yellow-500" />
                    </div>
                    <h3 className="mt-4 font-semibold text-foreground">JSON Export</h3>
                    <p className="mt-2 text-sm text-muted-foreground">
                      Machine-readable format for integration with other tools and automated processing.
                    </p>
                    <Button variant="outline" className="mt-4 w-full bg-transparent">
                      <Download className="mr-2 h-4 w-4" />
                      Download JSON
                    </Button>
                  </CardContent>
                </Card>
              </div>
            </CardContent>
          </Card>

          {/* Report Info */}
          <Card className="border-border/50">
            <CardHeader>
              <CardTitle>Report Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center gap-3">
                <Calendar className="h-5 w-5 text-muted-foreground" />
                <div>
                  <p className="text-sm text-muted-foreground">Generated</p>
                  <p className="text-sm font-medium text-foreground">{formatDate(reportData.generatedAt)}</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Target className="h-5 w-5 text-muted-foreground" />
                <div>
                  <p className="text-sm text-muted-foreground">Target</p>
                  <p className="truncate text-sm font-medium text-foreground">{reportData.target}</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Shield className="h-5 w-5 text-muted-foreground" />
                <div>
                  <p className="text-sm text-muted-foreground">Score</p>
                  <p className="text-sm font-medium text-primary">{reportData.score}/100</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <AlertTriangle className="h-5 w-5 text-muted-foreground" />
                <div>
                  <p className="text-sm text-muted-foreground">Findings</p>
                  <p className="text-sm font-medium text-foreground">{reportData.totalFindings} issues</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Executive Summary */}
          <Card className="border-border/50 lg:col-span-3">
            <CardHeader>
              <CardTitle>Executive Summary</CardTitle>
              <CardDescription>High-level overview of your application's security posture.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Score Overview */}
              <div className="rounded-xl border border-border bg-secondary/30 p-6">
                <div className="flex flex-col items-center gap-6 sm:flex-row sm:justify-between">
                  <div>
                    <h3 className="text-lg font-semibold text-foreground">Security Hygiene Score</h3>
                    <p className="mt-1 text-muted-foreground">
                      Your application scored {reportData.score} out of 100, indicating a{" "}
                      {reportData.score >= 80 ? "strong" : reportData.score >= 60 ? "moderate" : "weak"} security
                      posture.
                    </p>
                  </div>
                  <div className="flex h-24 w-24 items-center justify-center rounded-full border-4 border-primary">
                    <span className="text-3xl font-bold text-primary">{reportData.score}</span>
                  </div>
                </div>
              </div>

              {/* Findings Breakdown */}
              <div>
                <h3 className="mb-4 text-lg font-semibold text-foreground">Findings Breakdown</h3>
                <div className="grid gap-4 sm:grid-cols-4">
                  <Card className="border-red-500/20 bg-red-500/5">
                    <CardContent className="p-4 text-center">
                      <span className="text-3xl font-bold text-red-500">{reportData.breakdown.critical}</span>
                      <p className="mt-1 text-sm text-muted-foreground">Critical</p>
                    </CardContent>
                  </Card>
                  <Card className="border-orange-500/20 bg-orange-500/5">
                    <CardContent className="p-4 text-center">
                      <span className="text-3xl font-bold text-orange-500">{reportData.breakdown.high}</span>
                      <p className="mt-1 text-sm text-muted-foreground">High</p>
                    </CardContent>
                  </Card>
                  <Card className="border-yellow-500/20 bg-yellow-500/5">
                    <CardContent className="p-4 text-center">
                      <span className="text-3xl font-bold text-yellow-500">{reportData.breakdown.medium}</span>
                      <p className="mt-1 text-sm text-muted-foreground">Medium</p>
                    </CardContent>
                  </Card>
                  <Card className="border-green-500/20 bg-green-500/5">
                    <CardContent className="p-4 text-center">
                      <span className="text-3xl font-bold text-green-500">{reportData.breakdown.low}</span>
                      <p className="mt-1 text-sm text-muted-foreground">Low</p>
                    </CardContent>
                  </Card>
                </div>
              </div>

              {/* Key Recommendations */}
              <div>
                <h3 className="mb-4 text-lg font-semibold text-foreground">Key Recommendations</h3>
                <div className="space-y-3">
                  <div className="flex items-start gap-3 rounded-lg border border-border bg-card p-4">
                    <Badge variant="destructive" className="mt-0.5">
                      Critical
                    </Badge>
                    <div>
                      <p className="font-medium text-foreground">Disable legacy TLS protocols</p>
                      <p className="text-sm text-muted-foreground">
                        TLS 1.0 and 1.1 are enabled on your server. Upgrade to TLS 1.2+ immediately.
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3 rounded-lg border border-border bg-card p-4">
                    <Badge className="mt-0.5 bg-orange-500 text-white">High</Badge>
                    <div>
                      <p className="font-medium text-foreground">Implement Content Security Policy</p>
                      <p className="text-sm text-muted-foreground">
                        Add CSP headers to protect against XSS and code injection attacks.
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3 rounded-lg border border-border bg-card p-4">
                    <Badge className="mt-0.5 bg-orange-500 text-white">High</Badge>
                    <div>
                      <p className="font-medium text-foreground">Restrict CORS configuration</p>
                      <p className="text-sm text-muted-foreground">
                        Replace wildcard CORS with specific trusted origins.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
