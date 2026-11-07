const API_BASE = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '')

async function request(path, { token, ...options } = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    const detail = data.detail || Object.values(data)[0]
    throw new Error(Array.isArray(detail) ? detail.join(' ') : detail || 'La solicitud no pudo completarse.')
  }
  return data
}

export const loginApi = (values) => request('/api/v1/auth/token/', {
  method: 'POST', body: JSON.stringify(values),
})

export const registerApi = (values) => request('/api/v1/auth/register/', {
  method: 'POST', body: JSON.stringify(values),
})

export const meApi = (token) => request('/api/v1/auth/me/', { token })

export const scenesApi = (token) => request('/api/v1/external/avatar-scenes/', { token })

export const soapApi = (token) => request('/api/v1/external/soap/capital/?pais=MX', { token })
