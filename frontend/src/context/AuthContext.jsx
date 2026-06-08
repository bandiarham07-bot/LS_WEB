/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useState, useCallback } from 'react'
import axios from 'axios'

const AuthContext = createContext(null)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

function saveSession(data) {
  sessionStorage.setItem('access_token', data.access)
  sessionStorage.setItem('refresh_token', data.refresh)
  sessionStorage.setItem('user', JSON.stringify(data.user))
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const stored = sessionStorage.getItem('user')
    if (!stored || !sessionStorage.getItem('access_token')) return null
    return JSON.parse(stored)
  })
  const loading = false

  const loginWithGoogle = useCallback(async (credential) => {
    const { data } = await axios.post(
      `${API_BASE_URL}/api/auth/google/`,
      { credential }
    )
    saveSession(data)
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
