interface ReportSectionProps {
  title: string;
  content: string;
  downloadType: string;
}

export function ReportSection({ title, content, downloadType }: ReportSectionProps) {
  const handleDownload = async () => {
    const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
    try {
      const response = await fetch(`${baseUrl}/generator/download-report?type=${downloadType}`, {
        method: "GET",
      });

      if (!response.ok) {
        throw new Error("Failed to download the report");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `${downloadType}_report.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Download error:", error);
      alert("Failed to download the report. Please try again.");
    }
  };

  return (
    <section className="bg-gray-800 rounded-lg p-6 shadow-lg">
      <h2 className="text-2xl font-semibold mb-4">{title}</h2>
      <p className="mb-4">{content}</p>
      <button
        onClick={handleDownload}
        className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
      >
        Download PDF
      </button>
    </section>
  );
}
