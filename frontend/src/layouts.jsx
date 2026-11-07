import { Link, NavLink } from 'react-router-dom'
import { useAuth } from './auth/AuthContext'

function Brand() {
  return <Link className="brand" to="/" aria-label="Las cuatro naciones, inicio">
    <span className="brand-mark" aria-hidden="true">✦</span>
    <span>LAS CUATRO NACIONES</span>
  </Link>
}

function Shell({ children, mode }) {
  const { user, logout } = useAuth()
  return <div className={`site-shell site-shell--${mode}`}>
    <header className="site-header">
      <Brand />
      <nav aria-label="Navegación principal">
        <NavLink to="/">Inicio</NavLink>
        {user ? <NavLink to="/dashboard">Archivo</NavLink> : <NavLink to="/login">Ingresar</NavLink>}
        {user && <button type="button" onClick={logout}>Salir <span aria-hidden="true">↗</span></button>}
      </nav>
    </header>
    {children}
    <footer className="site-footer">
      <span>APPDEWEBINTEGRALCONNOMBRECAMBIADO</span>
      <span>Un archivo de las cuatro naciones</span>
      <a href="https://github.com/paigeegorry/last-airbender-api" target="_blank" rel="noreferrer">Datos e imágenes: Last Airbender API ↗</a>
    </footer>
  </div>
}

export function PublicLayout({ children }) { return <Shell mode="public">{children}</Shell> }
export function CommonLayout({ children }) { return <Shell mode="auth">{children}</Shell> }
export function DashboardLayout({ children }) { return <Shell mode="dashboard">{children}</Shell> }
