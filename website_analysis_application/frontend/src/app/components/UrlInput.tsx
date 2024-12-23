import { useState } from 'react'

interface UrlInputProps {
  onSubmit: (url: string) => void
  isDisabled: boolean
}

export function UrlInput({ onSubmit, isDisabled }: UrlInputProps) {
  const [inputUrl, setInputUrl] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (inputUrl) {
      onSubmit(inputUrl)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex justify-center">
      <input
        type="url"
        value={inputUrl}
        onChange={(e) => setInputUrl(e.target.value)}
        placeholder="Enter a URL to analyze"
        className="w-full max-w-2xl px-4 py-2 rounded-l-lg bg-gray-800 text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        required
      />
      <button
        type="submit"
        disabled={isDisabled}
        className="px-6 py-2 rounded-r-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
      >
        Analyze
      </button>
    </form>
  )
}

