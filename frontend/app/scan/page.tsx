"use client"
import { useRouter } from "next/navigation"
import { useState } from "react"
import { Navigation } from "@/components/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Progress } from "@/components/ui/progress"
import { Scan, Github, Loader2, CheckCircle2, Shield } from "lucide-react"
import api from '@/lib/api'
import type { ScanRequest } from '@/lib/types'

export default function ScanPage() {
  const [targetUrl, setTargetUrl] = useState("https://example-app.vercel.app")
  const [githubRepo, setGithubRepo] = useState("acme-corp/web-application")
  const [scanType, setScanType] = useState("quick")
  const [environment, setEnvironment] = useState("staging")
  const [isScanning, setIsScanning] = useState(false)
  const [scanProgress, setScanProgress] = useState(0)
  const [scanPhase, setScanPhase] = useState("")
  const [scanId, setScanId] = useState<string | null>(null)
  const router = useRouter()


// stauts polling 

const pollScanStatus = (scanId: string) => {
  const interval = setInterval(async () => {
    try {
      const response = await api.getScanStatus(scanId)

      if (!response.success) {
        console.error('Status check failed:', response.error)
        return
      }

      const status = response.data?.status

      const statusProgressMap: Record<string, number> = {
        PENDING: 10,
        RUNNING: 50,
        COMPLETED: 100,
        FAILED: 100,
      }

      setScanProgress(statusProgressMap[status || 'PENDING'] ?? 0)
      setScanPhase(`Status: ${status}`)

      if (status === 'COMPLETED') {
        clearInterval(interval)
        setIsScanning(false)
        router.push(`/dashboard?scan_id=${scanId}`)
      }

      if (status === 'FAILED') {
        clearInterval(interval)
        setIsScanning(false)
        setScanPhase('Scan failed')
      }
    } catch (err) {
      console.error("Status polling error:", err)
      clearInterval(interval)
      setIsScanning(false)
    }
  }, 2000)
}

// starting scan 
const startScan = async () => {
  setIsScanning(true)
  setScanProgress(0)
  setScanPhase("Initializing scan...")

  try {
    const scanRequest: ScanRequest = {
      target: targetUrl,
      scan_type: scanType as 'quick' | 'full',
      environment: environment as 'dev' | 'staging' | 'production',
      github_repo: githubRepo || undefined
    }

    const response = await api.startScan(scanRequest)

    if (response.success && response.data) {
      const id = response.data.scan_id
      setScanId(id)
      setScanPhase(`Scan created! Processing automatically...`)
      pollScanStatus(id)
    } else {
      throw new Error(response.error?.message || 'Failed to start scan')
    }
  } catch (err) {
    console.error("Error starting scan:", err)
    setIsScanning(false)
    setScanPhase(`Error: ${err}`)
  }
}

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <main className="mx-auto max-w-4xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-foreground">Security Scan</h1>
          <p className="mt-2 text-muted-foreground">Configure and run a security hygiene scan on your application.</p>
        </div>

        <div className="grid gap-8">
          {/* Target Configuration */}
          <Card className="border-border/50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="h-5 w-5 text-primary" />
                Target Configuration
              </CardTitle>
              <CardDescription>Enter the URL of the application you want to scan.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="target-url">Target URL</Label>
                <Input
                  id="target-url"
                  type="url"
                  placeholder="https://your-app.com"
                  value={targetUrl}
                  onChange={(e) => setTargetUrl(e.target.value)}
                  className="bg-input"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="github-repo" className="flex items-center gap-2">
                  <Github className="h-4 w-4" />
                  GitHub Repository (Optional)
                </Label>
                <Input
                  id="github-repo"
                  type="text"
                  placeholder="owner/repository"
                  value={githubRepo}
                  onChange={(e) => setGithubRepo(e.target.value)}
                  className="bg-input"
                />
              </div>
            </CardContent>
          </Card>

          {/* Scan Settings */}
          <Card className="border-border/50">
            <CardHeader>
              <CardTitle>Scan Settings</CardTitle>
              <CardDescription>Choose your scan type and target environment.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-3">
                <Label>Scan Type</Label>
                <RadioGroup value={scanType} onValueChange={setScanType} className="grid gap-3 sm:grid-cols-2">
                  <Label
                    htmlFor="quick"
                    className="flex cursor-pointer items-start gap-3 rounded-xl border border-border bg-card p-4 transition-colors hover:border-primary/50 [&:has(:checked)]:border-primary [&:has(:checked)]:bg-primary/5"
                  >
                    <RadioGroupItem value="quick" id="quick" className="mt-1" />
                    <div>
                      <div className="font-medium text-foreground">Quick Scan</div>
                      <div className="text-sm text-muted-foreground">
                        Fast scan covering essential security checks (~2 min)
                      </div>
                    </div>
                  </Label>
                  <Label
                    htmlFor="full"
                    className="flex cursor-pointer items-start gap-3 rounded-xl border border-border bg-card p-4 transition-colors hover:border-primary/50 [&:has(:checked)]:border-primary [&:has(:checked)]:bg-primary/5"
                  >
                    <RadioGroupItem value="full" id="full" className="mt-1" />
                    <div>
                      <div className="font-medium text-foreground">Full Scan</div>
                      <div className="text-sm text-muted-foreground">
                        Comprehensive scan with all security checks (~10 min)
                      </div>
                    </div>
                  </Label>
                </RadioGroup>
              </div>

              <div className="space-y-2">
                <Label htmlFor="environment">Environment</Label>
                <Select value={environment} onValueChange={setEnvironment}>
                  <SelectTrigger className="bg-input">
                    <SelectValue placeholder="Select environment" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="development">Development</SelectItem>
                    <SelectItem value="staging">Staging</SelectItem>
                    <SelectItem value="production">Production</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Scan Progress */}
          {isScanning && (
            <Card className="border-primary/50 bg-primary/5">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Loader2 className="h-5 w-5 animate-spin text-primary" />
                  Scan in Progress
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <Progress value={scanProgress} className="h-2" />
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Scan running…</span>
                  <span className="font-medium text-primary">{Math.round(scanProgress)}%</span>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Scan Complete */}
          {scanProgress === 100 && !isScanning && (
            <Card className="border-green-500/50 bg-green-500/5">
              <CardContent className="flex items-center gap-4 p-6">
                <CheckCircle2 className="h-8 w-8 text-green-500" />
                <div>
                  <div className="font-semibold text-foreground">Scan Complete!</div>
                  <div className="text-sm text-muted-foreground">
                    Found 12 issues across 4 severity levels. View results in the Dashboard.
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Start Scan Button */}
          <Button size="lg" onClick={startScan} disabled={isScanning || !targetUrl} className="w-full">
            {isScanning ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Scanning...
              </>
            ) : (
              <>
                <Scan className="mr-2 h-4 w-4" />
                Start Security Scan
              </>
            )}
          </Button>
        </div>
      </main>
    </div>
  )
}
