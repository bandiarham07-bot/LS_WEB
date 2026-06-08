import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''
let refreshPromise = null

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: { 'Content-Type': 'application/json' },
})

// Attach JWT access token to every request
api.interceptors.request.use((config) => {
  const token = sessionStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// On 401, try refreshing the token once
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true
      try {
        const refresh = sessionStorage.getItem('refresh_token')
        if (!refresh) throw new Error('Missing refresh token')

        refreshPromise ||= axios
          .post(`${API_BASE_URL}/api/auth/token/refresh/`, { refresh })
          .finally(() => {
            refreshPromise = null
          })

        const { data } = await refreshPromise
        sessionStorage.setItem('access_token', data.access)
        original.headers.Authorization = `Bearer ${data.access}`
        return api(original)
      } catch {
        sessionStorage.clear()
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default api
