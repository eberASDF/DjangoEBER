import { BrowserRouter, Navigate, Route, Routes, useLocation } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'
import { CommonLayout, DashboardLayout, PublicLayout } from '../layouts'
import { Dashboard, Home, Login, NotFound, Register } from '../pages'

function ProtectedRoute({ children }) {
  const { token, loading } = useAuth()
  const location = useLocation()
  if (loading) return <div className="loading-screen">Abriendo el archivo de las cuatro naciones…</div>
  if (!token) return <Navigate to="/login" replace state={{ from: location.pathname }} />
  return children
}

export function Navigation() {
  return <BrowserRouter>
    <Routes>
      <Route path="/" element={<PublicLayout><Home /></PublicLayout>} />
      <Route path="/login" element={<CommonLayout><Login /></CommonLayout>} />
      <Route path="/register" element={<CommonLayout><Register /></CommonLayout>} />
      <Route path="/dashboard" element={<ProtectedRoute><DashboardLayout><Dashboard /></DashboardLayout></ProtectedRoute>} />
      <Route path="*" element={<PublicLayout><NotFound /></PublicLayout>} />
    </Routes>
  </BrowserRouter>
}
