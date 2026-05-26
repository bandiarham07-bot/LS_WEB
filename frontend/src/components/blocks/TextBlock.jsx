export default function TextBlock({ block }) {
  return (
    <div className="bg-white border border-gray-100 rounded-2xl p-6">
      {block.title && (
        <h3 className="text-base font-semibold text-gray-900 mb-3">{block.title}</h3>
      )}
      <div className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
        {block.body}
      </div>
    </div>
  )
}
