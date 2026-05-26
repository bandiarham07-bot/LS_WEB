import { useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../api/client'

export function useUpdateProgress() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (pageId) => api.patch('/progress/', { page_id: pageId }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['home'] }),
  })
}
