import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import axios from 'axios'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  // Restore session on page reload
  useEffect(() => {
    const stored = sessionStorage.getItem('user')
    if (stored && sessionStorage.getItem('access_token')) {
      setUser(JSON.parse(stored))
    }
    setLoading(false)
  }, [])

  const loginWithGoogle = useCallback(async (credential) => {
    const { data } = await axios.post(
      import.meta.env.VITE_API_BASE_URL + '/api/auth/google/',
      { credential }
    )
    sessionStorage.setItem('access_token', data.access)
    sessionStorage.setItem('refresh_token', data.refresh)
    sessionStorage.setItem('user', JSON.stringify(data.user))
    setUser(data.user)
    return data.user
  }, [])

  const logout = useCallback(() => {
    sessionStorage.clear()
    setUser(null)
    // Revoke Google session
    if (window.google?.accounts?.id) {
      window.google.accounts.id.disableAutoSelect()
    }
  }, [])

  return (
    <AuthContext.Provider value={{ user, loading, loginWithGoogle, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider')
  return ctx
}
