import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider } from './context/AuthContext'
import { ToastProvider } from './components/Toast'
import ProtectedRoute from './components/ProtectedRoute'
import Layout from './components/Layout'
import LoginPage from './pages/LoginPage'
import HomePage from './pages/HomePage'
import ResourcesIndex from './pages/ResourcesIndex'
import SetupsIndex from './pages/SetupsIndex'
import AssignmentsIndex from './pages/AssignmentsIndex'
import SectionPage from './pages/SectionPage'
import PageRedirect from './pages/PageRedirect'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 1000 * 60, retry: 1 },
  },
})

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <ToastProvider>
          <BrowserRouter>
            <Routes>
              <Route path="/login" element={<LoginPage />} />

              <Route
                element={
                  <ProtectedRoute>
                    <Layout />
                  </ProtectedRoute>
                }
              >
                <Route index element={<HomePage />} />

                <Route path="resources" element={<ResourcesIndex />} />
                <Route path="resources/:pageId" element={<SectionPage />} />

                <Route path="setups" element={<SetupsIndex />} />
                <Route path="setups/:pageId" element={<SectionPage />} />

                <Route path="assignments" element={<AssignmentsIndex />} />
                <Route path="assignments/:pageId" element={<SectionPage />} />

                <Route path="page/:pageId" element={<PageRedirect />} />
              </Route>

              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </BrowserRouter>
        </ToastProvider>
      </AuthProvider>
    </QueryClientProvider>
  )
}
