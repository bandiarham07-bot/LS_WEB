/* eslint-disable react-refresh/only-export-components */
import { useState, createContext, useContext, useCallback } from 'react'

const ToastContext = createContext(null)

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])

  const showToast = useCallback((message, duration = 6000) => {
    const id = Date.now()
    setToasts(t => [...t, { id, message }])
    setTimeout(() => setToasts(t => t.filter(x => x.id !== id)), duration)
  }, [])

  const dismiss = useCallback((id) => {
    setToasts(t => t.filter(x => x.id !== id))
  }, [])

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      {/* Toast container — bottom right */}
      <div className="fixed bottom-5 right-5 flex flex-col gap-3 z-50 pointer-events-none">
        {toasts.map(toast => (
          <div
            key={toast.id}
            className="pointer-events-auto flex items-start gap-3 bg-white border border-gray-100 rounded-2xl shadow-lg px-4 py-3 w-72 animate-in"
          >
            <div className="w-8 h-8 rounded-xl bg-[#eef2f8] flex items-center justify-center shrink-0 mt-0.5">
              <svg width="16" height="16" viewBox="0 0 20 20" fill="none">
                <path d="M10 2a6 6 0 0 1 6 6c0 4-6 10-6 10S4 12 4 8a6 6 0 0 1 6-6z" stroke="#4a6fa5" strokeWidth="1.5"/>
                <circle cx="10" cy="8" r="2" stroke="#4a6fa5" strokeWidth="1.5"/>
              </svg>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-semibold text-gray-500">Upcoming Assignment:</p>
              <p className="text-sm text-gray-800 truncate">{toast.message}</p>
            </div>
            <button
              onClick={() => dismiss(toast.id)}
              className="shrink-0 text-gray-300 hover:text-gray-500 transition-colors mt-0.5"
            >
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                <path d="M3 3l8 8M11 3l-8 8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}

export function useToast() {
  const ctx = useContext(ToastContext)
  if (!ctx) throw new Error('useToast must be used inside ToastProvider')
  return ctx
}
