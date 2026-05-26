import { useNavigate } from 'react-router-dom'
import { useSectionPages } from '../hooks/useSectionPages'

const BLOCK_ICONS = {
  youtube: (
    <svg width="15" height="15" viewBox="0 0 20 20" fill="none">
      <rect x="2" y="4" width="16" height="12" rx="3" stroke="currentColor" strokeWidth="1.5"/>
      <path d="M8 7.5l5 2.5-5 2.5V7.5z" fill="currentColor"/>
    </svg>
  ),
  document: (
    <svg width="15" height="15" viewBox="0 0 20 20" fill="none">
      <path d="M6 2h8a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z" stroke="currentColor" strokeWidth="1.5"/>
      <path d="M7 7h6M7 10h6M7 13h4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    </svg>
  ),
  text: (
    <svg width="15" height="15" viewBox="0 0 20 20" fill="none">
      <path d="M4 5h12M4 9h12M4 13h8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    </svg>
  ),
}

export default function SetupsIndex() {
  const navigate = useNavigate()
  const { data: pages, isLoading } = useSectionPages('setups')

  if (isLoading) return (
    <div className="flex justify-center pt-20">
      <div className="w-6 h-6 rounded-full border-2 border-[#4a6fa5] border-t-transparent animate-spin" />
    </div>
  )

  if (!pages?.length) return (
    <div className="text-center pt-20 text-sm text-gray-400">No setups added yet.</div>
  )

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-8">Setups by Week</h1>
      <div className="flex flex-col gap-8">
        {pages.map(page => (
          <div key={page.id}>
            <h2 className="text-base font-semibold text-gray-800 mb-3 px-1">{page.title}</h2>
            <div className="flex flex-col gap-2">
              {page.blocks.length === 0 ? (
                <p className="text-sm text-gray-400 px-1">No content yet.</p>
              ) : (
                page.blocks.map(block => (
                  <button
                    key={block.id}
                    onClick={() => navigate(`/setups/${page.id}`)}
                    className="w-full flex items-center justify-between px-5 py-3 bg-[#4a6fa5] hover:bg-[#3d5e8e] active:bg-[#345280] text-white text-sm font-medium rounded-xl transition-colors text-left group"
                  >
                    <span className="truncate">
                      {block.title || (block.type === 'youtube' ? 'Video' : block.type === 'document' ? 'Document' : 'Reading')}
                    </span>
                    <span className="shrink-0 ml-3 opacity-70 group-hover:opacity-100 transition-opacity">
                      {BLOCK_ICONS[block.type]}
                    </span>
                  </button>
                ))
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
