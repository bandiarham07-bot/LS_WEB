import { useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { usePage } from '../hooks/usePage'

// Resolves /page/:id → /:section/:id using the page's section field
export default function PageRedirect() {
  const { pageId } = useParams()
  const { data: page } = usePage(pageId)
  const navigate = useNavigate()

  useEffect(() => {
    if (page) navigate(`/${page.section}/${page.id}`, { replace: true })
  }, [page, navigate])

  return (
    <div className="flex justify-center pt-20">
      <div className="w-6 h-6 rounded-full border-2 border-[#4a6fa5] border-t-transparent animate-spin" />
    </div>
  )
}
