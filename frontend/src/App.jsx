import { AuthProvider } from './auth/AuthContext'
import { Navigation } from './routes/Navigation'

export default function App() {
  return <AuthProvider><Navigation /></AuthProvider>
}
