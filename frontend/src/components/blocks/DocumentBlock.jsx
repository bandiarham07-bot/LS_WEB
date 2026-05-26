export default function DocumentBlock({ block }) {
  return (
    <div className="bg-white border border-gray-100 rounded-2xl p-5">
      <div className="flex items-center gap-4">
        <div className="w-11 h-11 rounded-xl bg-[#eef2f8] flex items-center justify-center shrink-0">
          <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
            <path d="M13 2H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V9z" stroke="#4a6fa5" strokeWidth="1.5"/>
            <path d="M13 2v7h7" stroke="#4a6fa5" strokeWidth="1.5" strokeLinejoin="round"/>
            <path d="M8 13h6M8 16h4" stroke="#4a6fa5" strokeWidth="1.5" strokeLinecap="round"/>
          </svg>
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-gray-900 truncate">{block.title || 'Document'}</p>
          {block.body && <p className="text-xs text-gray-400 mt-0.5 truncate">{block.body}</p>}
        </div>
        <a
          href={block.url}
          target="_blank"
          rel="noopener noreferrer"
          className="shrink-0 px-4 py-2 bg-[#4a6fa5] text-white text-xs font-medium rounded-lg hover:bg-[#3d5e8e] transition-colors"
        >
          Open
        </a>
      </div>
    </div>
  )
}
