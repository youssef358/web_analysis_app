'use client'

import { useState } from 'react'
import { UrlInput } from './components/UrlInput'
import { ReportSection } from './components/ReportSection'

export default function Home() {
  const [url, setUrl] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [showReports, setShowReports] = useState(false)

  const handleSubmit = async (submittedUrl: string) => {
    setUrl(submittedUrl);
    setIsAnalyzing(true);
    const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
  
    try {
      const response = await fetch(`${baseUrl}/generator/generate-reports`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: submittedUrl }),
      });
  
      if (!response.ok) {
        throw new Error("Report generation failed");
      }
  
      const { frontend_report_url, ui_ux_report_url, seo_report_url } = await response.json();
  
      console.log("Frontend Report URL:", frontend_report_url);
      console.log("UI/UX Report URL:", ui_ux_report_url);
      console.log("SEO Report URL:", seo_report_url);
  
      setShowReports(true);
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to generate reports. Please try again.");
    } finally {
      setIsAnalyzing(false);
    }
  };
  

  return (
    <main className="min-h-screen p-8">
      <h1 className="text-4xl font-bold mb-8 text-center">Web Analysis Tool</h1>
      <UrlInput onSubmit={handleSubmit} isDisabled={isAnalyzing} />
      {isAnalyzing && (
        <div className="text-center mt-8">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
          <p className="mt-2">Analyzing {url}...</p>
        </div>
      )}
      {showReports && (
        <div className="mt-12 space-y-8">
          <ReportSection
            title="Front-end Analysis"
            content="Technical aspects of the website..."
            downloadType="frontend"
          />
          <ReportSection
            title="UI/UX Analysis"
            content="Design and user experience evaluation..."
            downloadType="ui_ux"
          />
          <ReportSection
            title="SEO Analysis"
            content="Search engine optimization insights..."
            downloadType="seo"
          />
        </div>
      )}
    </main>
  )
}

