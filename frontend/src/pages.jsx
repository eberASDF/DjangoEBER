import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { registerApi, scenesApi, soapApi } from './api'
import { useAuth } from './auth/AuthContext'

const elements = [
  { name: 'Aire', glyph: '◌', code: '01' },
  { name: 'Agua', glyph: '≈', code: '02' },
  { name: 'Tierra', glyph: '◇', code: '03' },
  { name: 'Fuego', glyph: '✺', code: '04' },
]

function ElementRail() {
  return <div className="element-rail" aria-label="Los cuatro elementos">
    {elements.map((item) => <div className="element-rail__item" key={item.name}>
      <span className="element-rail__glyph" aria-hidden="true">{item.glyph}</span>
      <span>{item.name}</span>
      <small>{item.code}</small>
    </div>)}
  </div>
}

export function Home() {
  return <main>
    <section className="hero hero--home">
      <div className="hero__eyebrow"><span className="eyebrow-line" /> UN ARCHIVO PARA EXPLORAR</div>
      <div className="hero__content">
        <p className="hero__side-note">AGUA · TIERRA · FUEGO · AIRE</p>
        <div>
          <h1>El mundo<br /><em>en equilibrio.</em></h1>
          <p className="hero__intro">Una mirada a las historias de Aang, Korra y los nuevos horizontes. Entra al archivo para descubrir imágenes, personajes y los cuatro elementos.</p>
          <Link className="text-link text-link--light" to="/login">Explorar el archivo <span aria-hidden="true">↗</span></Link>
        </div>
      </div>
      <div className="hero__orb" aria-hidden="true"><span /><span /><span /></div>
      <div className="hero__foot"><span>CRÓNICAS DE AVATAR</span><span>DESLIZA PARA DESCUBRIR ↓</span></div>
    </section>
    <section className="editorial-intro">
      <p className="section-index">01 / EL ARCHIVO</p>
      <div><h2>Cuatro elementos.<br />Una historia que continúa.</h2><p>Del viaje del último maestro aire al legado de Korra. Una experiencia construida para explorar personajes del universo Avatar desde una sola pantalla.</p></div>
    </section>
    <ElementRail />
    <section className="editorial-end"><p>EL VIAJE COMIENZA AQUÍ</p><Link to="/register">Únete al archivo <span aria-hidden="true">↗</span></Link></section>
  </main>
}

function AuthFrame({ title, subtitle, children, aside }) {
  return <main className="auth-page">
    <section className="auth-page__art" aria-hidden="true">
      <span className="auth-page__vertical">LAS CUATRO NACIONES · ARCHIVO DIGITAL</span>
      <div className="auth-page__symbol">✦</div>
      <div className="auth-page__art-footer"><span>AGUA / TIERRA / FUEGO / AIRE</span><span>∞</span></div>
    </section>
    <section className="auth-page__form-area">
      <p className="section-index">{aside}</p>
      <div className="auth-page__form-inner"><h1>{title}</h1><p>{subtitle}</p>{children}</div>
      <p className="auth-page__bottom">EL EQUILIBRIO EMPIEZA CON UN PASO</p>
    </section>
  </main>
}

export function Login() {
  const { login, user } = useAuth()
  const navigate = useNavigate()
  const [values, setValues] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  useEffect(() => { if (user) navigate('/dashboard', { replace: true }) }, [user, navigate])

  async function submit(event) {
    event.preventDefault()
    setError('')
    setBusy(true)
    try {
      await login(values)
      navigate('/dashboard', { replace: true })
    } catch (failure) {
      setError(failure.message)
    } finally { setBusy(false) }
  }

  return <AuthFrame title="Bienvenido de nuevo." subtitle="Entra para continuar tu recorrido por las cuatro naciones." aside="ACCESO / 01">
    <form className="auth-form" onSubmit={submit}>
      <label>Correo electrónico<input type="email" name="email" value={values.email} onChange={(e) => setValues({ ...values, email: e.target.value })} autoComplete="username" required placeholder="tu@correo.com" /></label>
      <label>Contraseña<input type="password" name="password" value={values.password} onChange={(e) => setValues({ ...values, password: e.target.value })} autoComplete="current-password" required placeholder="Tu contraseña" /></label>
      {error && <p className="form-error" role="alert">{error}</p>}
      <button className="primary-action" disabled={busy}>{busy ? 'Ingresando…' : 'Entrar al archivo'} <span aria-hidden="true">↗</span></button>
    </form>
    <p className="auth-page__switch">¿Aún no tienes cuenta? <Link to="/register">Crea una aquí</Link></p>
  </AuthFrame>
}

export function Register() {
  const navigate = useNavigate()
  const [values, setValues] = useState({ username: '', email: '', first_name: '', telefono: '', password: '', password_confirm: '' })
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  async function submit(event) {
    event.preventDefault()
    setError('')
    if (values.password !== values.password_confirm) { setError('Las contraseñas no coinciden.'); return }
    setBusy(true)
    try {
      await registerApi(values)
      navigate('/login', { state: { registered: true } })
    } catch (failure) { setError(failure.message) }
    finally { setBusy(false) }
  }

  const update = (event) => setValues({ ...values, [event.target.name]: event.target.value })

  return <AuthFrame title="Empieza tu viaje." subtitle="Crea una cuenta para acceder al archivo de las cuatro naciones." aside="REGISTRO / 02">
    <form className="auth-form auth-form--register" onSubmit={submit}>
      <label>Nombre de usuario<input name="username" value={values.username} onChange={update} required maxLength="150" autoComplete="username" placeholder="Tu nombre de usuario" /></label>
      <label>Correo electrónico<input type="email" name="email" value={values.email} onChange={update} required autoComplete="email" placeholder="tu@correo.com" /></label>
      <label>Nombre<input name="first_name" value={values.first_name} onChange={update} placeholder="¿Cómo te llamas?" /></label>
      <label>Teléfono <small>opcional</small><input name="telefono" value={values.telefono} onChange={update} placeholder="Tu número" /></label>
      <label>Contraseña<input type="password" name="password" value={values.password} onChange={update} required minLength="8" autoComplete="new-password" placeholder="Mínimo 8 caracteres" /></label>
      <label>Confirmar contraseña<input type="password" name="password_confirm" value={values.password_confirm} onChange={update} required autoComplete="new-password" placeholder="Repite tu contraseña" /></label>
      {error && <p className="form-error" role="alert">{error}</p>}
      <button className="primary-action" disabled={busy}>{busy ? 'Creando cuenta…' : 'Crear cuenta'} <span aria-hidden="true">↗</span></button>
    </form>
    <p className="auth-page__switch">¿Ya tienes cuenta? <Link to="/login">Inicia sesión</Link></p>
  </AuthFrame>
}

export function Dashboard() {
  const { user, token } = useAuth()
  const [scenes, setScenes] = useState([])
  const [source, setSource] = useState('')
  const [index, setIndex] = useState(0)
  const [scenesError, setScenesError] = useState('')
  const [soap, setSoap] = useState(null)
  const [soapError, setSoapError] = useState('')

  useEffect(() => {
    let live = true
    scenesApi(token).then((data) => { if (live) { setScenes(data.imagenes || []); setSource(data.fuente || '') } })
      .catch((failure) => { if (live) setScenesError(failure.message) })
    soapApi(token).then((data) => { if (live) setSoap(data) })
      .catch((failure) => { if (live) setSoapError(failure.message) })
    return () => { live = false }
  }, [token])

  const scene = scenes[index]
  const displayName = user?.first_name || user?.username || user?.email?.split('@')[0] || 'viajero'
  return <main className="dashboard">
    <section className="dashboard__head">
      <p className="section-index">ARCHIVO PERSONAL / {new Date().getFullYear()}</p>
      <div><p className="dashboard__greeting">HOLA, {displayName.toLocaleUpperCase('es-MX')}</p><h1>El mundo sigue<br /><em>en movimiento.</em></h1></div>
      <div className="dashboard__head-bottom"><span>UN VIAJE POR EL UNIVERSO AVATAR</span><span>↓ EXPLORA</span></div>
    </section>
    <section className="scene-section" aria-labelledby="scene-heading">
      <div className="scene-section__top"><p className="section-index">01 / PERSONAJES DEL UNIVERSO</p><p>THE LAST AIRBENDER · THE LEGEND OF KORRA</p></div>
      <div className={`scene-stage ${scene ? 'scene-stage--loaded' : ''}`}>
        {scene ? <img key={scene.imagen} src={scene.imagen} alt={`${scene.titulo || 'Escena'} de ${scene.serie}`} /> : <div className="scene-stage__placeholder" aria-hidden="true">✦</div>}
        <div className="scene-stage__shade" />
        <div className="scene-stage__copy"><span>IMAGEN {String(index + 1).padStart(2, '0')} / {String(scenes.length).padStart(2, '0')}</span><h2 id="scene-heading">{scene?.titulo || scene?.serie || 'Un mundo por descubrir'}</h2></div>
      </div>
      <div className="scene-section__controls"><p>{scenesError || (scene ? `Imágenes de personajes obtenidas desde ${source}.` : 'Cargando imágenes de la API…')}</p><button type="button" onClick={() => setIndex((index + 1) % scenes.length)} disabled={scenes.length < 2}>Cambiar imagen <span aria-hidden="true">↗</span></button></div>
    </section>
    <section className="dashboard__details">
      <div><p className="section-index">02 / SERVICIO SOAP</p><h2>Otro mapa.<br />Una capital.</h2></div>
      <div className="soap-result"><span>COUNTRYINFOSERVICE / ZEEP</span><strong>{soap?.capital || '—'}</strong><p>{soap ? `Capital de ${soap.pais}, consultada mediante un servicio SOAP público.` : (soapError || 'Consultando el servicio SOAP…')}</p></div>
    </section>
    <section className="credits"><h2>Acerca de las imágenes</h2><p>Las imágenes de personajes llegan desde la API pública Last Airbender API. Los retratos enlazan a imágenes alojadas por Avatar Wiki.</p><a href="https://github.com/paigeegorry/last-airbender-api" target="_blank" rel="noreferrer">Ver la API y su código ↗</a></section>
  </main>
}

export function NotFound() { return <main className="not-found"><span>404</span><h1>Te alejaste del mapa.</h1><Link className="text-link" to="/">Volver al inicio ↗</Link></main> }
