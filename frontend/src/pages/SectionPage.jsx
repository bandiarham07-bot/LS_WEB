import { useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useSectionPages } from '../hooks/useSectionPages'
import { usePage } from '../hooks/usePage'
import { useUpdateProgress } from '../hooks/useUpdateProgress'
import AssignmentDetail from '../components/AssignmentDetail'
import ContentBlockRenderer from '../components/blocks/ContentBlockRenderer'

const SECTION_LABELS = {
  resources:   'Resources',
  setups:      'Setups',
  assignments: 'Assignments',
  home:        'Home',
}

const BACK_LABELS = {
  resources:   'All resources',
  setups:      'All setups',
  assignments: 'All assignments',
}

function useSectionFromPath() {
  const path = window.location.pathname
  if (path.startsWith('/resources'))   return 'resources'
  if (path.startsWith('/setups'))      return 'setups'
  if (path.startsWith('/assignments')) return 'assignments'
  return 'home'
}

export default function SectionPage() {
  const { pageId } = useParams()
  const navigate = useNavigate()
  const section = useSectionFromPath()

  const { data: pages } = useSectionPages(section)
  const { mutate: updateProgress } = useUpdateProgress()

  const { data: page, isLoading } = usePage(pageId)

  useEffect(() => {
    if (pageId) updateProgress(pageId)
  }, [pageId]) // eslint-disable-line

  if (isLoading || !page) return (
    <div className="flex justify-center pt-20">
      <div className="w-6 h-6 rounded-full border-2 border-[#4a6fa5] border-t-transparent animate-spin" />
    </div>
  )

  const pageIndex = pages ? pages.findIndex(p => p.id === page.id) : -1
  const totalPages = pages?.length ?? 0

  function handleNext() {
    if (!page.next_page_id) return
    navigate(`/page/${page.next_page_id}`)
  }

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">
            {SECTION_LABELS[section] ?? section}
            {totalPages > 0 && (
              <span className="ml-2 font-normal normal-case">
                · {pageIndex + 1} of {totalPages}
              </span>
            )}
          </p>
          <h1 className="text-2xl font-bold text-gray-900">{page.title}</h1>
        </div>

        {/* Back to index */}
        <button
          onClick={() => navigate(`/${section}`)}
          className="flex items-center gap-1.5 px-3 py-2 text-sm text-[#4a6fa5] hover:bg-[#eef2f8] rounded-lg transition-colors"
        >
          <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
            <path d="M10 3L5 8l5 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          {BACK_LABELS[section]}
        </button>
      </div>

      {section === 'assignments' && page.assignment ? (
        <AssignmentDetail page={page} />
      ) : (
        <div className="flex flex-col gap-4 mb-8">
          {page.blocks.map(block => (
            <ContentBlockRenderer key={block.id} block={block} />
          ))}
          {page.blocks.length === 0 && (
            <div className="bg-white border border-gray-100 rounded-2xl p-10 text-center text-sm text-gray-400">
              No content on this page yet.
            </div>
          )}
        </div>
      )}

      {/* Navigation footer */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 px-4 py-2.5 text-sm text-gray-500 hover:text-gray-800 transition-colors"
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M10 3L5 8l5 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          Back
        </button>

        {page.next_page_id ? (
          <button
            onClick={handleNext}
            className="flex items-center gap-2 px-6 py-2.5 bg-[#4a6fa5] text-white text-sm font-medium rounded-xl hover:bg-[#3d5e8e] transition-colors"
          >
            Next
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M6 3l5 5-5 5" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        ) : (
          <div className="flex items-center gap-2 px-4 py-2.5 text-sm text-[#4a6fa5] font-medium">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M3 8l3.5 3.5L13 4" stroke="#4a6fa5" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            Section complete
          </div>
        )}
      </div>
    </div>
  )
}
