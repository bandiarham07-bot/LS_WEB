import { useQuery } from '@tanstack/react-query'
import api from '../api/client'

export function usePage(pageId) {
  return useQuery({
    queryKey: ['page', pageId],
    queryFn: async () => {
      const { data } = await api.get(`/page/${pageId}/`)
      return data
    },
    enabled: !!pageId,
  })
}
