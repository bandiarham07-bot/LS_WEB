import { useQuery } from '@tanstack/react-query'
import api from '../api/client'

export function useSectionPages(section) {
  return useQuery({
    queryKey: ['section', section],
    queryFn: async () => {
      const { data } = await api.get(`/pages/${section}/`)
      return data
    },
    enabled: !!section,
  })
}
