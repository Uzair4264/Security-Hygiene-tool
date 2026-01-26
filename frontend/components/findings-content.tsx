"use client"

import React, { useEffect, useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Search, ChevronDown, ChevronUp, ExternalLink } from "lucide-react"
import { useSearchParams } from "next/navigation"

/* ---------------- TYPES ---------------- */

type Severity = "critical" | "high" | "medium" | "low"

interface Finding {
  id: string
  title: string
  severity: Severity
  category: string
  source: string
  description: string

  // 🔽 REQUIRED FOR DIALOG
  location?: string
  risk?: string
  remediation?: string

  recommendation: string
  evidence?: string
  cwe?: string
  owasp?: string
}

/* ---------------- CONSTANTS ---------------- */

const severityColors: Record<Severity, string> = {
  critical: "bg-red-500/10 text-red-500 border-red-500/20",
  high: "bg-orange-500/10 text-orange-500 border-orange-500/20",
  medium: "bg-yellow-500/10 text-yellow-500 border-yellow-500/20",
  low: "bg-green-500/10 text-green-500 border-green-500/20",
}

/* ---------------- COMPONENT ---------------- */

export function FindingsContent() {
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedFinding, setSelectedFinding] = useState<Finding | null>(null)
  const [expandedRows, setExpandedRows] = useState<Set<string>>(new Set())
  const [findings, setFindings] = useState<Finding[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const searchParams = useSearchParams()
  const scanId = searchParams.get("scan_id")

  /* ---------------- FETCH DATA ---------------- */

  useEffect(() => {
    if (!scanId) {
      setError("Scan ID missing")
      setLoading(false)
      return
    }

    const fetchFindings = async () => {
      try {
        setLoading(true)

        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/scan/${scanId}/result`
        )

        const json = await res.json()
        const result = json?.data

        if (!result || !Array.isArray(result.tool_results)) {
          throw new Error("Invalid scan result format")
        }

        const flattenedFindings: Finding[] =
          result.tool_results.flatMap(
            (tool: any, toolIndex: number) =>
              (tool.issues || []).map((issue: any, index: number) => ({
                id: `${tool.tool.toUpperCase()}-${toolIndex + 1}-${index + 1}`,
                title: issue.name,
                severity: issue.severity.toLowerCase() as Severity,
                category: issue.category || tool.tool,
                source: tool.tool,

                description:
                  issue.description || "No description available",

                // 🔽 DIALOG FIELDS
                location:
                  issue.location ||
                  issue.url ||
                  issue.endpoint ||
                  "Not specified",

                risk:
                  issue.risk ||
                  issue.impact ||
                  issue.severity_reason ||
                  "Risk not specified",

                remediation:
                  issue.remediation ||
                  issue.fix ||
                  issue.recommendation ||
                  "No remediation provided",

                recommendation:
                  issue.recommendation ||
                  "No recommendation available",

                evidence: issue.evidence,
                cwe: issue.cwe,
                owasp: issue.owasp,
              }))
          )

        setFindings(flattenedFindings)
      } catch (err: any) {
        setError(err.message || "Failed to load findings")
      } finally {
        setLoading(false)
      }
    }

    fetchFindings()
  }, [scanId])

  /* ---------------- FILTER ---------------- */

  const filteredFindings = findings.filter(
    (finding) =>
      finding.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      finding.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      finding.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
      finding.severity.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const toggleRow = (id: string) => {
    const next = new Set(expandedRows)
    next.has(id) ? next.delete(id) : next.add(id)
    setExpandedRows(next)
  }

  /* ---------------- STATES ---------------- */

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-muted-foreground">
        Loading scan findings...
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center text-destructive">
        {error}
      </div>
    )
  }

  if (!findings.length) {
    return (
      <div className="min-h-screen flex items-center justify-center text-muted-foreground">
        No findings were generated for this scan.
      </div>
    )
  }

  /* ---------------- UI ---------------- */

  return (
    <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      {/* HEADER */}
      <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">
            Security Findings
          </h1>
          <p className="mt-2 text-muted-foreground">
            {filteredFindings.length} issues detected in your application.
          </p>
        </div>

        <div className="relative w-full sm:w-80">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search findings..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      {/* TABLE */}
      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-12" />
                <TableHead>ID</TableHead>
                <TableHead>Title</TableHead>
                <TableHead>Severity</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>Source</TableHead>
                <TableHead className="w-12" />
              </TableRow>
            </TableHeader>

            <TableBody>
              {filteredFindings.map((finding) => (
                <React.Fragment key={finding.id}>
                  <TableRow
                    className="cursor-pointer hover:bg-secondary/50"
                    onClick={() => toggleRow(finding.id)}
                  >
                    <TableCell>
                      <Button variant="ghost" size="icon">
                        {expandedRows.has(finding.id) ? (
                          <ChevronUp className="h-4 w-4" />
                        ) : (
                          <ChevronDown className="h-4 w-4" />
                        )}
                      </Button>
                    </TableCell>

                    <TableCell className="font-mono text-sm">
                      {finding.id}
                    </TableCell>

                    <TableCell className="font-medium">
                      {finding.title}
                    </TableCell>

                    <TableCell>
                      <Badge
                        variant="outline"
                        className={severityColors[finding.severity]}
                      >
                        {finding.severity}
                      </Badge>
                    </TableCell>

                    <TableCell>{finding.category}</TableCell>
                    <TableCell>{finding.source}</TableCell>

                    <TableCell>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={(e) => {
                          e.stopPropagation()
                          setSelectedFinding(finding)
                        }}
                      >
                        <ExternalLink className="h-4 w-4" />
                      </Button>
                    </TableCell>
                  </TableRow>

                  {expandedRows.has(finding.id) && (
                    <TableRow className="bg-secondary/30">
                      <TableCell colSpan={7} className="p-6">
                        <div className="space-y-4">
                          <div>
                            <h4 className="font-semibold">Description</h4>
                            <p className="mt-2 text-sm text-muted-foreground">
                              {finding.description}
                            </p>
                          </div>

                          {finding.evidence && (
                            <div>
                              <h4 className="font-semibold">Evidence</h4>
                              <code className="mt-2 block rounded bg-background p-2 font-mono text-xs whitespace-pre-wrap">
                                {finding.evidence}
                              </code>
                            </div>
                          )}

                          <div>
                            <h4 className="font-semibold text-primary">
                              Recommendation
                            </h4>
                            <p className="mt-2 text-sm text-muted-foreground">
                              {finding.recommendation}
                            </p>
                          </div>
                        </div>
                      </TableCell>
                    </TableRow>
                  )}
                </React.Fragment>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* ---------------- DETAIL DIALOG ---------------- */}

      <Dialog
        open={!!selectedFinding}
        onOpenChange={() => setSelectedFinding(null)}
      >
        <DialogContent className="max-w-2xl">
          {selectedFinding && (
            <>
              <DialogHeader>
                <div className="flex gap-3">
                  <Badge
                    variant="outline"
                    className={severityColors[selectedFinding.severity]}
                  >
                    {selectedFinding.severity}
                  </Badge>

                  <div>
                    <DialogTitle>{selectedFinding.title}</DialogTitle>
                    <DialogDescription>
                      {selectedFinding.id} • {selectedFinding.category} •{" "}
                      {selectedFinding.source}
                    </DialogDescription>
                  </div>
                </div>
              </DialogHeader>

              <div className="space-y-6 pt-4">
                <div>
                  <h4 className="font-semibold">Description</h4>
                  <p className="mt-2 text-sm text-muted-foreground">
                    {selectedFinding.description}
                  </p>
                </div>

                <div>
                  <h4 className="font-semibold">Location</h4>
                  <code className="mt-2 block rounded bg-secondary p-3 font-mono text-sm">
                    {selectedFinding.location}
                  </code>
                </div>

                <div>
                  <h4 className="font-semibold text-destructive">Risk</h4>
                  <p className="mt-2 text-sm text-muted-foreground">
                    {selectedFinding.risk}
                  </p>
                </div>

                <div>
                  <h4 className="font-semibold text-primary">Remediation</h4>
                  <pre className="mt-2 whitespace-pre-wrap rounded bg-secondary p-3 font-mono text-sm text-muted-foreground">
                    {selectedFinding.remediation}
                  </pre>
                </div>
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </main>
  )
}
