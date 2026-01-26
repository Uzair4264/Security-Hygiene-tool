"use client"

import { useState } from "react"
import { Navigation } from "@/components/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import { Slider } from "@/components/ui/slider"
import { Label } from "@/components/ui/label"
import { Github, GitPullRequest, Rocket, CheckCircle2, XCircle, AlertTriangle, Settings2 } from "lucide-react"

export default function CICDPage() {
  const [githubConnected] = useState(true)
  const [enforcePR, setEnforcePR] = useState(true)
  const [enforceDeployment, setEnforceDeployment] = useState(true)
  const [blockCritical, setBlockCritical] = useState(true)
  const [minScore, setMinScore] = useState([70])

  const recentChecks = [
    {
      id: "check-001",
      type: "PR",
      branch: "feature/auth-improvements",
      status: "passed",
      score: 78,
      date: "2025-12-26T09:30:00Z",
    },
    {
      id: "check-002",
      type: "Deployment",
      branch: "main",
      status: "passed",
      score: 72,
      date: "2025-12-26T08:15:00Z",
    },
    {
      id: "check-003",
      type: "PR",
      branch: "fix/header-security",
      status: "failed",
      score: 54,
      date: "2025-12-25T16:45:00Z",
    },
    {
      id: "check-004",
      type: "PR",
      branch: "feature/api-endpoints",
      status: "passed",
      score: 85,
      date: "2025-12-25T14:20:00Z",
    },
  ]

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-foreground">CI/CD Security Enforcement</h1>
          <p className="mt-2 text-muted-foreground">Configure security gates for your development workflow.</p>
        </div>

        <div className="grid gap-6 lg:grid-cols-3">
          {/* GitHub Integration Status */}
          <Card className="border-border/50 lg:col-span-3">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Github className="h-5 w-5" />
                GitHub Integration
              </CardTitle>
              <CardDescription>Connect your GitHub repository to enable automated security checks.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div className="flex items-center gap-3">
                  {githubConnected ? (
                    <>
                      <CheckCircle2 className="h-8 w-8 text-green-500" />
                      <div>
                        <p className="font-medium text-foreground">Connected</p>
                        <p className="text-sm text-muted-foreground">acme-corp/web-application</p>
                      </div>
                    </>
                  ) : (
                    <>
                      <XCircle className="h-8 w-8 text-muted-foreground" />
                      <div>
                        <p className="font-medium text-foreground">Not Connected</p>
                        <p className="text-sm text-muted-foreground">Connect your repository to get started</p>
                      </div>
                    </>
                  )}
                </div>
                <Button variant={githubConnected ? "outline" : "default"}>
                  {githubConnected ? "Manage Connection" : "Connect GitHub"}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Enforcement Settings */}
          <Card className="border-border/50 lg:col-span-2">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings2 className="h-5 w-5 text-primary" />
                Enforcement Settings
              </CardTitle>
              <CardDescription>Configure when security checks should block your workflow.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-8">
              {/* PR Enforcement */}
              <div className="flex items-center justify-between">
                <div className="flex items-start gap-3">
                  <GitPullRequest className="mt-0.5 h-5 w-5 text-muted-foreground" />
                  <div>
                    <Label htmlFor="enforce-pr" className="text-base font-medium">
                      Enforce on Pull Requests
                    </Label>
                    <p className="text-sm text-muted-foreground">
                      Run security scans on every pull request and require passing checks.
                    </p>
                  </div>
                </div>
                <Switch id="enforce-pr" checked={enforcePR} onCheckedChange={setEnforcePR} />
              </div>

              {/* Deployment Enforcement */}
              <div className="flex items-center justify-between">
                <div className="flex items-start gap-3">
                  <Rocket className="mt-0.5 h-5 w-5 text-muted-foreground" />
                  <div>
                    <Label htmlFor="enforce-deploy" className="text-base font-medium">
                      Enforce on Deployments
                    </Label>
                    <p className="text-sm text-muted-foreground">
                      Block deployments that don't meet security requirements.
                    </p>
                  </div>
                </div>
                <Switch id="enforce-deploy" checked={enforceDeployment} onCheckedChange={setEnforceDeployment} />
              </div>

              {/* Block Critical */}
              <div className="flex items-center justify-between">
                <div className="flex items-start gap-3">
                  <AlertTriangle className="mt-0.5 h-5 w-5 text-muted-foreground" />
                  <div>
                    <Label htmlFor="block-critical" className="text-base font-medium">
                      Block on Critical Findings
                    </Label>
                    <p className="text-sm text-muted-foreground">
                      Automatically fail checks if critical vulnerabilities are found.
                    </p>
                  </div>
                </div>
                <Switch id="block-critical" checked={blockCritical} onCheckedChange={setBlockCritical} />
              </div>

              {/* Minimum Score Threshold */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <Label className="text-base font-medium">Minimum Hygiene Score</Label>
                    <p className="text-sm text-muted-foreground">Require a minimum security score to pass checks.</p>
                  </div>
                  <span className="text-2xl font-bold text-primary">{minScore[0]}</span>
                </div>
                <Slider value={minScore} onValueChange={setMinScore} max={100} min={0} step={5} className="w-full" />
                <div className="flex justify-between text-xs text-muted-foreground">
                  <span>0 (No minimum)</span>
                  <span>100 (Perfect score)</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Status Overview */}
          <Card className="border-border/50">
            <CardHeader>
              <CardTitle>Enforcement Status</CardTitle>
              <CardDescription>Current configuration summary</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">PR Checks</span>
                <Badge variant={enforcePR ? "default" : "secondary"}>{enforcePR ? "Enabled" : "Disabled"}</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Deploy Checks</span>
                <Badge variant={enforceDeployment ? "default" : "secondary"}>
                  {enforceDeployment ? "Enabled" : "Disabled"}
                </Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Block Critical</span>
                <Badge variant={blockCritical ? "destructive" : "secondary"}>
                  {blockCritical ? "Active" : "Inactive"}
                </Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Min Score</span>
                <Badge variant="outline">{minScore[0]}+</Badge>
              </div>
            </CardContent>
          </Card>

          {/* Recent Checks */}
          <Card className="border-border/50 lg:col-span-3">
            <CardHeader>
              <CardTitle>Recent Security Checks</CardTitle>
              <CardDescription>Latest CI/CD security check results</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentChecks.map((check) => (
                  <div
                    key={check.id}
                    className="flex flex-col gap-3 rounded-xl border border-border bg-card p-4 sm:flex-row sm:items-center sm:justify-between"
                  >
                    <div className="flex items-center gap-3">
                      {check.status === "passed" ? (
                        <CheckCircle2 className="h-6 w-6 text-green-500" />
                      ) : (
                        <XCircle className="h-6 w-6 text-red-500" />
                      )}
                      <div>
                        <div className="flex items-center gap-2">
                          <Badge variant="outline">{check.type}</Badge>
                          <span className="font-mono text-sm text-foreground">{check.branch}</span>
                        </div>
                        <p className="text-sm text-muted-foreground">{formatDate(check.date)}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="text-right">
                        <span className="text-lg font-bold text-primary">{check.score}</span>
                        <span className="text-muted-foreground">/100</span>
                      </div>
                      <Badge variant={check.status === "passed" ? "default" : "destructive"}>
                        {check.status === "passed" ? "Passed" : "Failed"}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
