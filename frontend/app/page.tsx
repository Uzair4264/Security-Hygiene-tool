import { Navigation } from "@/components/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Shield, Scan, Lock, GitBranch, ArrowRight, CheckCircle2 } from "lucide-react"
import Link from "next/link"



const features = [
  {
    icon: Scan,
    title: "Automated Security Hygiene",
    description: "Continuous monitoring and automated scanning to maintain your application's security posture.",
  },
  {
    icon: Shield,
    title: "OWASP ZAP Passive Scanning",
    description: "Leverage industry-standard vulnerability detection with passive scanning capabilities.",
  },
  {
    icon: Lock,
    title: "TLS & Header Analysis",
    description: "Comprehensive analysis of TLS configurations and security headers for maximum protection.",
  },
  {
    icon: GitBranch,
    title: "CI/CD Enforcement",
    description: "Integrate security checks directly into your deployment pipeline with configurable thresholds.",
  },
]

const steps = [
  { step: "01", title: "Connect Repository", description: "Link your GitHub repository or enter target URL" },
  { step: "02", title: "Configure Scan", description: "Select scan type and environment settings" },
  { step: "03", title: "Run Analysis", description: "Automated security hygiene checks execute" },
  { step: "04", title: "Review & Fix", description: "Get actionable remediation guidance" },
]

const stats = [
  { value: "50K+", label: "Scans completed" },
  { value: "99.9%", label: "Uptime SLA" },
  { value: "< 2min", label: "Average scan time" },
  { value: "200+", label: "Security checks" },
]

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      {/* Hero Section */}
      <section className="relative overflow-hidden px-4 py-24 sm:px-6 lg:px-8">
        <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-primary/20 via-background to-background" />
        <div className="mx-auto max-w-7xl">
          <div className="mx-auto max-w-3xl text-center">
            <h1 className="text-balance text-4xl font-bold tracking-tight text-foreground sm:text-6xl">
              Security Hygiene
              <span className="block text-primary">Automation Platform</span>
            </h1>
            <p className="mt-6 text-pretty text-lg leading-relaxed text-muted-foreground">
              Proactively identify vulnerabilities, enforce security policies, and maintain compliance with automated
              security hygiene scanning for your applications.
            </p>
            <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
              <Button asChild size="lg" className="w-full sm:w-auto">
                <Link href="/scan">
                  Start Scan
                  <Scan className="ml-2 h-4 w-4" />
                </Link>
              </Button>
              <Button asChild variant="outline" size="lg" className="w-full sm:w-auto bg-transparent">
                <Link href="/dashboard">
                  View Dashboard
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </div>
          </div>

          {/* Stats */}
          <div className="mt-20 grid grid-cols-2 gap-4 sm:grid-cols-4">
            {stats.map((stat) => (
              <Card key={stat.label} className="border-border/50 bg-card/50 backdrop-blur">
                <CardContent className="p-6 text-center">
                  <div className="text-3xl font-bold text-primary">{stat.value}</div>
                  <div className="mt-1 text-sm text-muted-foreground">{stat.label}</div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="border-t border-border bg-card/30 px-4 py-24 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-foreground">Enterprise-Grade Security</h2>
            <p className="mt-4 text-muted-foreground">
              Comprehensive security scanning and enforcement tools designed for modern development workflows.
            </p>
          </div>
          <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {features.map((feature) => {
              const Icon = feature.icon
              return (
                <Card
                  key={feature.title}
                  className="border-border/50 bg-card transition-colors hover:border-primary/50"
                >
                  <CardHeader>
                    <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10">
                      <Icon className="h-6 w-6 text-primary" />
                    </div>
                    <CardTitle className="mt-4 text-lg">{feature.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-muted-foreground">{feature.description}</CardDescription>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section className="px-4 py-24 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-foreground">How It Works</h2>
            <p className="mt-4 text-muted-foreground">
              Get started with security hygiene automation in four simple steps.
            </p>
          </div>
          <div className="mt-16 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {steps.map((step, index) => (
              <div key={step.step} className="relative">
                {index < steps.length - 1 && (
                  <div className="absolute left-1/2 top-8 hidden h-0.5 w-full bg-border lg:block" />
                )}
                <div className="relative flex flex-col items-center text-center">
                  <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-primary text-2xl font-bold text-primary-foreground">
                    {step.step}
                  </div>
                  <h3 className="mt-6 text-lg font-semibold text-foreground">{step.title}</h3>
                  <p className="mt-2 text-sm text-muted-foreground">{step.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="border-t border-border bg-card/30 px-4 py-24 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <Card className="border-primary/20 bg-primary/5">
            <CardContent className="flex flex-col items-center p-12 text-center">
              <CheckCircle2 className="h-12 w-12 text-primary" />
              <h2 className="mt-6 text-2xl font-bold text-foreground">Ready to secure your applications?</h2>
              <p className="mt-4 max-w-xl text-muted-foreground">
                Start your first security scan in minutes. No credit card required.
              </p>
              <Button asChild size="lg" className="mt-8">
                <Link href="/scan">
                  Get Started Free
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border px-4 py-12 sm:px-6 lg:px-8">
        <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 sm:flex-row">
          <div className="flex items-center gap-2">
            <Shield className="h-6 w-6 text-primary" />
            <span className="font-semibold text-foreground">ShieldGuard</span>
          </div>
          <p className="text-sm text-muted-foreground">© 2025 ShieldGuard. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}
