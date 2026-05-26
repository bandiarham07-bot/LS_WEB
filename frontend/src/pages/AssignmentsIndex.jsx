import { useNavigate } from 'react-router-dom'
import { useSectionPages } from '../hooks/useSectionPages'

export default function AssignmentsIndex() {
  const navigate = useNavigate()
  const { data: pages, isLoading } = useSectionPages('assignments')

  if (isLoading) return (
    <div className="flex justify-center pt-20">
      <div className="w-6 h-6 rounded-full border-2 border-[#4a6fa5] border-t-transparent animate-spin" />
    </div>
  )

  if (!pages?.length) return (
    <div className="text-center pt-20 text-sm text-gray-400">No assignments added yet.</div>
  )

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-8">Assignments</h1>
      <div className="flex flex-col gap-2">
        {pages.map(page => (
          <button
            key={page.id}
            onClick={() => navigate(`/assignments/${page.id}`)}
            className="w-full flex items-center justify-between px-5 py-3 bg-[#4a6fa5] hover:bg-[#3d5e8e] active:bg-[#345280] text-white text-sm font-medium rounded-xl transition-colors text-left group"
          >
            <span className="truncate">{page.title}</span>
            <svg width="15" height="15" viewBox="0 0 16 16" fill="none" className="shrink-0 ml-3 opacity-70 group-hover:opacity-100 transition-opacity">
              <path d="M6 3l5 5-5 5" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        ))}
      </div>
    </div>
  )
}
