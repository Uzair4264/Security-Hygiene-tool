"use client"

import { useState } from "react"
import { Navigation } from "@/components/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import { Slider } from "@/components/ui/slider"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Bell, Shield, Palette, Save } from "lucide-react"

export default function SettingsPage() {
  // Scan Settings
  const [defaultScanType, setDefaultScanType] = useState("full")
  const [defaultEnvironment, setDefaultEnvironment] = useState("staging")
  const [autoScan, setAutoScan] = useState(true)
  const [scanFrequency, setScanFrequency] = useState("daily")

  // Severity Weights
  const [criticalWeight, setCriticalWeight] = useState([10])
  const [highWeight, setHighWeight] = useState([7])
  const [mediumWeight, setMediumWeight] = useState([4])
  const [lowWeight, setLowWeight] = useState([1])

  // Notifications
  const [emailNotifications, setEmailNotifications] = useState(true)
  const [slackNotifications, setSlackNotifications] = useState(false)
  const [notifyOnCritical, setNotifyOnCritical] = useState(true)
  const [notifyOnScanComplete, setNotifyOnScanComplete] = useState(true)
  const [notifyEmail, setNotifyEmail] = useState("security-team@acme-corp.com")

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <main className="mx-auto max-w-4xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-foreground">Settings</h1>
          <p className="mt-2 text-muted-foreground">Configure your security platform preferences.</p>
        </div>

        <Tabs defaultValue="scan" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="scan" className="flex items-center gap-2">
              <Shield className="h-4 w-4" />
              Scan
            </TabsTrigger>
            <TabsTrigger value="severity" className="flex items-center gap-2">
              <Palette className="h-4 w-4" />
              Severity
            </TabsTrigger>
            <TabsTrigger value="notifications" className="flex items-center gap-2">
              <Bell className="h-4 w-4" />
              Notifications
            </TabsTrigger>
          </TabsList>

          {/* Scan Settings */}
          <TabsContent value="scan">
            <Card className="border-border/50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="h-5 w-5 text-primary" />
                  Default Scan Configuration
                </CardTitle>
                <CardDescription>Set your preferred default settings for new scans.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid gap-6 sm:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="scan-type">Default Scan Type</Label>
                    <Select value={defaultScanType} onValueChange={setDefaultScanType}>
                      <SelectTrigger className="bg-input">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="quick">Quick Scan</SelectItem>
                        <SelectItem value="full">Full Scan</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="environment">Default Environment</Label>
                    <Select value={defaultEnvironment} onValueChange={setDefaultEnvironment}>
                      <SelectTrigger className="bg-input">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="development">Development</SelectItem>
                        <SelectItem value="staging">Staging</SelectItem>
                        <SelectItem value="production">Production</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="flex items-center justify-between rounded-xl border border-border bg-card p-4">
                  <div>
                    <Label htmlFor="auto-scan" className="text-base font-medium">
                      Automated Scanning
                    </Label>
                    <p className="text-sm text-muted-foreground">Automatically run security scans on a schedule.</p>
                  </div>
                  <Switch id="auto-scan" checked={autoScan} onCheckedChange={setAutoScan} />
                </div>

                {autoScan && (
                  <div className="space-y-2">
                    <Label htmlFor="frequency">Scan Frequency</Label>
                    <Select value={scanFrequency} onValueChange={setScanFrequency}>
                      <SelectTrigger className="bg-input">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="hourly">Every Hour</SelectItem>
                        <SelectItem value="daily">Daily</SelectItem>
                        <SelectItem value="weekly">Weekly</SelectItem>
                        <SelectItem value="monthly">Monthly</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                )}

                <Button className="w-full sm:w-auto">
                  <Save className="mr-2 h-4 w-4" />
                  Save Scan Settings
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Severity Weights */}
          <TabsContent value="severity">
            <Card className="border-border/50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Palette className="h-5 w-5 text-primary" />
                  Severity Weighting
                </CardTitle>
                <CardDescription>Customize how different severity levels impact your security score.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-8">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="h-3 w-3 rounded-full bg-red-500" />
                      <Label>Critical</Label>
                    </div>
                    <span className="font-mono text-lg font-bold text-red-500">{criticalWeight[0]}x</span>
                  </div>
                  <Slider value={criticalWeight} onValueChange={setCriticalWeight} max={15} min={1} step={1} />
                </div>

                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="h-3 w-3 rounded-full bg-orange-500" />
                      <Label>High</Label>
                    </div>
                    <span className="font-mono text-lg font-bold text-orange-500">{highWeight[0]}x</span>
                  </div>
                  <Slider value={highWeight} onValueChange={setHighWeight} max={15} min={1} step={1} />
                </div>

                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="h-3 w-3 rounded-full bg-yellow-500" />
                      <Label>Medium</Label>
                    </div>
                    <span className="font-mono text-lg font-bold text-yellow-500">{mediumWeight[0]}x</span>
                  </div>
                  <Slider value={mediumWeight} onValueChange={setMediumWeight} max={15} min={1} step={1} />
                </div>

                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="h-3 w-3 rounded-full bg-green-500" />
                      <Label>Low</Label>
                    </div>
                    <span className="font-mono text-lg font-bold text-green-500">{lowWeight[0]}x</span>
                  </div>
                  <Slider value={lowWeight} onValueChange={setLowWeight} max={15} min={1} step={1} />
                </div>

                <Button className="w-full sm:w-auto">
                  <Save className="mr-2 h-4 w-4" />
                  Save Severity Weights
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Notifications */}
          <TabsContent value="notifications">
            <Card className="border-border/50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Bell className="h-5 w-5 text-primary" />
                  Notification Preferences
                </CardTitle>
                <CardDescription>Configure how and when you receive security alerts.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-4">
                  <h4 className="font-medium text-foreground">Channels</h4>
                  <div className="flex items-center justify-between rounded-xl border border-border bg-card p-4">
                    <div>
                      <Label className="text-base font-medium">Email Notifications</Label>
                      <p className="text-sm text-muted-foreground">Receive security alerts via email.</p>
                    </div>
                    <Switch checked={emailNotifications} onCheckedChange={setEmailNotifications} />
                  </div>
                  <div className="flex items-center justify-between rounded-xl border border-border bg-card p-4">
                    <div>
                      <Label className="text-base font-medium">Slack Notifications</Label>
                      <p className="text-sm text-muted-foreground">Send alerts to your Slack workspace.</p>
                    </div>
                    <Switch checked={slackNotifications} onCheckedChange={setSlackNotifications} />
                  </div>
                </div>

                {emailNotifications && (
                  <div className="space-y-2">
                    <Label htmlFor="email">Notification Email</Label>
                    <Input
                      id="email"
                      type="email"
                      value={notifyEmail}
                      onChange={(e) => setNotifyEmail(e.target.value)}
                      className="bg-input"
                    />
                  </div>
                )}

                <div className="space-y-4">
                  <h4 className="font-medium text-foreground">Triggers</h4>
                  <div className="flex items-center justify-between rounded-xl border border-border bg-card p-4">
                    <div>
                      <Label className="text-base font-medium">Critical Findings</Label>
                      <p className="text-sm text-muted-foreground">Alert immediately when critical issues are found.</p>
                    </div>
                    <Switch checked={notifyOnCritical} onCheckedChange={setNotifyOnCritical} />
                  </div>
                  <div className="flex items-center justify-between rounded-xl border border-border bg-card p-4">
                    <div>
                      <Label className="text-base font-medium">Scan Complete</Label>
                      <p className="text-sm text-muted-foreground">Notify when a security scan finishes.</p>
                    </div>
                    <Switch checked={notifyOnScanComplete} onCheckedChange={setNotifyOnScanComplete} />
                  </div>
                </div>

                <Button className="w-full sm:w-auto">
                  <Save className="mr-2 h-4 w-4" />
                  Save Notification Settings
                </Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}
