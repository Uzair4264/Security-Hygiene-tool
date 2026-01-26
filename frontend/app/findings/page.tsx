import { Navigation } from "@/components/navigation"
import { FindingsContent } from "@/components/findings-content" // <-- import here

export default function FindingsPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <div className="p-6 text-muted-foreground">
        {/* Optional: placeholder text */}
        {/* Select a scan from History to view findings. */}
      </div>

      {/* Render the actual findings content */}
      <FindingsContent />
    </div>
  )
}
