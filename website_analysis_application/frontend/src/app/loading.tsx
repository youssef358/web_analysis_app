export default function Loading() {
    return (
      <div className="fixed inset-0 bg-gray-100 bg-opacity-75 flex items-center justify-center">
        <div className="bg-white p-8 rounded-lg shadow-md">
          <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-lg font-semibold text-gray-700">Analyzing website...</p>
        </div>
      </div>
    )
  }
  
  