import { useNavigate } from 'react-router-dom'
import { useHome } from '../hooks/useHome'
import { useSectionPages } from '../hooks/useSectionPages'

function LastSeenCard({ page }) {
  const navigate = useNavigate()
  if (!page) return (
    <div className="bg-[#eef2f8] border border-[#d0ddf0] rounded-2xl p-6">
      <p className="text-xs font-semibold text-[#4a6fa5] uppercase tracking-wider mb-2">Last seen</p>
      <p className="text-gray-500 text-sm">No progress yet — start from Resources.</p>
      <button
        onClick={() => navigate('/resources')}
        className="mt-4 w-full bg-[#4a6fa5] text-white rounded-xl py-2.5 text-sm font-medium hover:bg-[#3d5e8e] transition-colors"
      >
        Get started
      </button>
    </div>
  )
  return (
    <div className="bg-[#eef2f8] border border-[#d0ddf0] rounded-2xl p-6">
      <p className="text-xs font-semibold text-[#4a6fa5] uppercase tracking-wider mb-2">Last seen</p>
      <h2 className="text-xl font-bold text-gray-900 mb-4">{page.title}</h2>
      <button
        onClick={() => navigate(`/${page.section}/${page.id}`)}
        className="w-full bg-[#4a6fa5] text-white rounded-xl py-2.5 text-sm font-medium hover:bg-[#3d5e8e] transition-colors"
      >
        Continue
      </button>
    </div>
  )
}

function AssignmentReminderCard({ pages }) {
  // Show the last assignments page as a reminder
  const last = pages?.[pages.length - 1];
  
  if (!last) return null;
  
  return (
    <div className="bg-white border border-gray-100 rounded-2xl p-5 flex items-start gap-3">
      <div className="w-9 h-9 rounded-xl bg-[#eef2f8] flex items-center justify-center shrink-0">
        <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
          <path d="M10 2a6 6 0 0 1 6 6c0 4-6 10-6 10S4 12 4 8a6 6 0 0 1 6-6z" stroke="#4a6fa5" strokeWidth="1.5"/>
          <circle cx="10" cy="8" r="2" stroke="#4a6fa5" strokeWidth="1.5"/>
        </svg>
      </div>
      <div>
        <p className="text-sm font-medium text-gray-900">Upcoming Assignment:</p>
        <p className="text-sm text-gray-500 mt-0.5">{last.title}</p>
      </div>
    </div>
  )
}

function CourseStatusCard({ status }) {
  if (!status) return null
  const topics = status.current_topic
    ? status.current_topic.split(',').map(t => t.trim())
    : []
  return (
    <div className="bg-white border border-gray-100 rounded-2xl p-6">
      <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Course status</p>
      <div className="mb-4">
        <p className="text-xs text-gray-400 mb-0.5">Current</p>
        <p className="text-lg font-bold text-gray-900">Week {status.current_week}: {status.current_topic}</p>
      </div>
      {topics.length > 1 && (
        <div className="flex flex-col gap-2">
          {topics.map((topic, i) => (
            <div key={i} className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded-full border-2 border-gray-300" />
                <span className="text-sm text-gray-600">{topic}</span>
              </div>
              <div className="w-5 h-5 rounded bg-[#4a6fa5] flex items-center justify-center">
                <svg width="11" height="11" viewBox="0 0 11 11" fill="none">
                  <path d="M2 5.5l2.5 2.5L9 3" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default function HomePage() {
  const { data, isLoading } = useHome()
  const { data: assignmentPages } = useSectionPages('assignments')

  if (isLoading) return (
    <div className="flex justify-center pt-20">
      <div className="w-6 h-6 rounded-full border-2 border-[#4a6fa5] border-t-transparent animate-spin" />
    </div>
  )

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">My Course Progress</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <LastSeenCard page={data?.last_page} />
        <div className="flex flex-col gap-4">
          <AssignmentReminderCard pages={assignmentPages} />
          <CourseStatusCard status={data?.course_status} />
        </div>
      </div>
    </div>
  )
}
