import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function LoginPage() {
  const { loginWithGoogle, user } = useAuth()
  const navigate = useNavigate()
  const btnRef = useRef(null)
  const [loginError, setLoginError] = useState('')
  const [isSigningIn, setIsSigningIn] = useState(false)

  useEffect(() => {
    if (user) { navigate('/'); return }

    const initGoogle = () => {
      window.google.accounts.id.initialize({
        client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
        callback: async ({ credential }) => {
          setLoginError('')
          setIsSigningIn(true)
          try {
            await loginWithGoogle(credential)
            navigate('/')
          } catch {
            setLoginError('Sign in failed. Please try again.')
          } finally {
            setIsSigningIn(false)
          }
        },
      })
      window.google.accounts.id.renderButton(btnRef.current, {
        theme: 'outline',
        size: 'large',
        width: 280,
        text: 'signin_with',
      })
    }

    if (window.google?.accounts?.id) {
      initGoogle()
    } else {
      const existingScript = document.querySelector('script[src="https://accounts.google.com/gsi/client"]')
      const script = existingScript || document.createElement('script')
      script.src = 'https://accounts.google.com/gsi/client'
      script.async = true
      script.defer = true
      script.onload = initGoogle
      if (!existingScript) document.head.appendChild(script)
    }
  }, [user, loginWithGoogle, navigate])

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#f0f2f5]">
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-10 flex flex-col items-center gap-6 w-full max-w-sm">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <div className="w-9 h-9 rounded-lg bg-[#4a6fa5] flex items-center justify-center">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M4 5h12M4 10h8M4 15h10" stroke="white" strokeWidth="1.8" strokeLinecap="round"/>
            </svg>
          </div>
          <span className="text-[15px] font-semibold text-gray-800">Student Learning Hub</span>
        </div>

        <div className="text-center">
          <h1 className="text-xl font-semibold text-gray-900 mb-1">Welcome back</h1>
          <p className="text-sm text-gray-500">Sign in to continue your course</p>
        </div>

        <div ref={btnRef} />

        {isSigningIn && (
          <p className="text-xs text-gray-500">Signing in...</p>
        )}

        {loginError && (
          <p className="text-sm text-red-600 text-center">{loginError}</p>
        )}

        <p className="text-xs text-gray-400 text-center">
          Only registered students can access this platform
        </p>
      </div>
    </div>
  )
}
