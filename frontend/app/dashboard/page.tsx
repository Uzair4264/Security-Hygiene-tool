"use client"

import { Navigation } from "@/components/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Shield, AlertTriangle, AlertCircle, Info, CheckCircle2 } from "lucide-react"
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts"
import { useEffect, useState } from "react"
import { useSearchParams } from "next/navigation"
import { Loader2 } from "lucide-react"
import api from '@/lib/api'

export default function DashboardPage() {
  
  const searchParams = useSearchParams()
  const scanId = searchParams.get("scan_id")
  const [scoreData, setScoreData] = useState<any>(null)
  const [completedAt, setCompletedAt] = useState<string>("")
  const [severityData, setSeverityData] = useState<any[]>([])
  const [categoryData, setCategoryData] = useState<any[]>([])
  const [summaryCards, setSummaryCards] = useState<any[]>([])
  const [loading, setLoading] = useState(true)


  
useEffect(() => {
  console.log("Dashboard scanId:", scanId)

  if (!scanId) return

  let interval: NodeJS.Timeout

  const pollStatus = async () => {
    try {
      const response = await api.getScanStatus(scanId)

      if (!response.success) return

      const status = response.data?.status

      if (status === "COMPLETED") {
        clearInterval(interval)
        fetchResult()
      }
    } catch (err) {
      console.error("Status polling failed", err)
      clearInterval(interval)
    }
  }

  const fetchResult = async () => {
    try {
      setLoading(true)
      const response = await api.getScanResult(scanId)

      if (!response.success || !response.data) {
        console.error('Failed to fetch results')
        setLoading(false)
        return
      }

      const data = response.data
      setCompletedAt(data.completed_at || '')

      const score = data.score
      setScoreData(score)

      setSeverityData([
        { name: "Critical", value: score.critical_count, color: "#ef4444" },
        { name: "High", value: score.high_count, color: "#f97316" },
        { name: "Medium", value: score.medium_count, color: "#eab308" },
        { name: "Low", value: score.low_count, color: "#22c55e" },
      ])

      // Build category data from tool_results
      const categoryMap: Record<string, number> = {}
      data.tool_results?.forEach((tool) => {
        const category = tool.category || tool.tool
        const totalIssues = tool.issues?.length || 0
        categoryMap[category] = (categoryMap[category] || 0) + totalIssues
      })

      setCategoryData(
        Object.entries(categoryMap).map(([name, issues]) => ({
          name: name.toUpperCase(),
          issues,
        }))
      )

      setSummaryCards([
        {
          label: "Score",
          value: score.score,
          icon: Shield,
          color: "text-green-500",
        },
        {
          label: "Grade",
          value: score.grade,
          icon: CheckCircle2,
          color: "text-blue-500",
        },
        {
          label: "Critical",
          value: score.critical_count,
          icon: AlertCircle,
          color: "text-red-500",
        },
        {
          label: "High",
          value: score.high_count,
          icon: AlertTriangle,
          color: "text-orange-500",
        },
        {
          label: "Medium",
          value: score.medium_count,
          icon: Info,
          color: "text-yellow-500",
        },
      ])

      setLoading(false)
    } catch (err) {
      console.error("Result fetch failed", err)
      setLoading(false)
    }
  }

  interval = setInterval(pollStatus, 2000)

  return () => clearInterval(interval)
}, [scanId])


if (loading || !scoreData) {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <div className="flex items-center justify-center" style={{ minHeight: 'calc(100vh - 64px)' }}>
        <div className="text-center space-y-4">
          <Loader2 className="h-12 w-12 animate-spin text-primary mx-auto" />
          <p className="text-muted-foreground">Loading scan results...</p>
          {scanId && <p className="text-xs text-muted-foreground">Scan ID: {scanId}</p>}
        </div>
      </div>
    </div>
  )
}
  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-foreground">Security Dashboard</h1>
          <p className="mt-2 text-muted-foreground">Overview of your application's security hygiene status.</p>
        </div>

        <div className="grid gap-6">
          {/* Score Card */}
          <Card className="border-border/50">
            <CardContent className="flex flex-col items-center p-8 sm:flex-row sm:justify-between">
              <div className="text-center sm:text-left">
                <CardDescription className="text-base">Security Hygiene Score</CardDescription>
                <div className="mt-2 flex items-baseline gap-2">
                  <span className="text-6xl font-bold text-primary">{scoreData.score}</span>
                  <span className="text-2xl text-muted-foreground">/100</span>
                </div>
                <Badge variant="secondary" className="mt-4">
                  <Shield className="mr-1 h-3 w-3" />
                  Last scanned: {new Date(completedAt).toLocaleString()}
                </Badge>
              </div>
              <div className="mt-6 flex h-32 w-32 items-center justify-center rounded-full border-8 border-primary/20 sm:mt-0">
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary">{scoreData.score}%</div>
                  <div className="text-xs text-muted-foreground">Healthy</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Summary Cards */}
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
            {summaryCards.map((card) => {
              const Icon = card.icon
              return (
                <Card key={card.label} className="border-border/50">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <Icon className={`h-8 w-8 ${card.color}`} />
                      <span className="text-3xl font-bold text-foreground">{card.value}</span>
                    </div>
                    <div className="mt-2 text-sm text-muted-foreground">{card.label}</div>
                  </CardContent>
                </Card>
              )
            })}
          </div>

          {/* Charts */}
          <div className="grid gap-6 lg:grid-cols-2">
            {/* Severity Distribution */}
            <Card className="border-border/50">
              <CardHeader>
                <CardTitle>Severity Distribution</CardTitle>
                <CardDescription>Breakdown of findings by severity level</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={severityData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={100}
                        paddingAngle={2}
                        dataKey="value"
                      >
                        {severityData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip
                        contentStyle={{
                          backgroundColor: "hsl(var(--card))",
                          border: "1px solid hsl(var(--border))",
                          borderRadius: "8px",
                        }}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
                <div className="mt-4 flex flex-wrap justify-center gap-4">
                  {severityData.map((item) => (
                    <div key={item.name} className="flex items-center gap-2">
                      <div className="h-3 w-3 rounded-full" style={{ backgroundColor: item.color }} />
                      <span className="text-sm text-muted-foreground">
                        {item.name}: {item.value}
                      </span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Category Breakdown */}
            <Card className="border-border/50">
              <CardHeader>
                <CardTitle>Category Breakdown</CardTitle>
                <CardDescription>Issues grouped by security category</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={categoryData} layout="vertical">
                      <XAxis type="number" stroke="hsl(var(--muted-foreground))" fontSize={12} />
                      <YAxis
                        type="category"
                        dataKey="name"
                        stroke="hsl(var(--muted-foreground))"
                        fontSize={12}
                        width={60}
                      />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: "hsl(var(--card))",
                          border: "1px solid hsl(var(--border))",
                          borderRadius: "8px",
                        }}
                      />
                      <Bar dataKey="issues" fill="hsl(var(--primary))" radius={[0, 4, 4, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  )
}
