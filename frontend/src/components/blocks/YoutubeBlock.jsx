function getYoutubeId(url) {
  try {
    const u = new URL(url)
    return u.searchParams.get('v') || u.pathname.split('/').pop()
  } catch {
    return null
  }
}

export default function YoutubeBlock({ block }) {
  const videoId = getYoutubeId(block.url)
  return (
    <div className="bg-white border border-gray-100 rounded-2xl overflow-hidden">
      {block.title && (
        <div className="px-6 pt-5 pb-3">
          <h3 className="text-base font-semibold text-gray-900">{block.title}</h3>
          {block.body && <p className="text-sm text-gray-500 mt-1">{block.body}</p>}
        </div>
      )}
      <div className="relative w-full" style={{ paddingBottom: '56.25%' }}>
        {videoId ? (
          <iframe
            className="absolute inset-0 w-full h-full"
            src={`https://www.youtube.com/embed/${videoId}`}
            title={block.title || 'Video'}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-50 text-sm text-gray-400">
            Invalid YouTube URL
          </div>
        )}
      </div>
    </div>
  )
}
