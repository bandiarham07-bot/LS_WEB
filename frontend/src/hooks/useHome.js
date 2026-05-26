import { useQuery } from '@tanstack/react-query'
import api from '../api/client'

export function useHome() {
  return useQuery({
    queryKey: ['home'],
    queryFn: async () => {
      const { data } = await api.get('/home/')
      return data
    },
  })
}
