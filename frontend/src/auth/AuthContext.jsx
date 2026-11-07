import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { loginApi, meApi } from '../api'

const AuthContext = createContext(null)
const STORAGE_KEY = 'avatar_archive_access'

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem(STORAGE_KEY))
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(Boolean(token))

  const logout = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY)
    setToken(null)
    setUser(null)
    setLoading(false)
  }, [])

  useEffect(() => {
    if (!token) return
    let active = true
    meApi(token).then((profile) => {
      if (active) setUser(profile)
    }).catch(() => {
      if (active) logout()
    }).finally(() => {
      if (active) setLoading(false)
    })
    return () => { active = false }
  }, [token, logout])

  const login = useCallback(async (values) => {
    const result = await loginApi(values)
    localStorage.setItem(STORAGE_KEY, result.access)
    setLoading(true)
    setToken(result.access)
    const profile = await meApi(result.access)
    setUser(profile)
    setLoading(false)
    // La consola confirma la recepción sin exponer el JWT completo.
    console.info('Token JWT obtenido; longitud:', result.access.length)
    return profile
  }, [])

  const value = useMemo(() => ({ token, user, loading, login, logout }), [token, user, loading, login, logout])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth requiere AuthProvider')
  return context
}
