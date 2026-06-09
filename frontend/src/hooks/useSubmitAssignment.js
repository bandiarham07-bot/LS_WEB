import { useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../api/client'

export function useSubmitAssignment(pageId, assignmentId) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async ({ githubRepoUrl, rollNumber }) => {
      const { data } = await api.post(`/assignments/${assignmentId}/submit/`, {
        github_repo_url: githubRepoUrl,
        roll_number: rollNumber,
      })
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['page', pageId] })
    },
  })
}
