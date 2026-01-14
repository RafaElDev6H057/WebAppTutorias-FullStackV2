import axios from 'axios'

// ==================== CONFIGURACIÓN BASE ====================
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// ==================== INTERCEPTOR REQUEST ====================
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// ==================== INTERCEPTOR RESPONSE ====================
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Solo redirigir si:
    // 1. Es un error 401
    // 2. HAY un token en localStorage (significa que estaba autenticado)
    // 3. NO es una petición a endpoints de login

    const isLoginRequest =
      error.config?.url?.includes('/login') || error.config?.url?.includes('/set-password')

    if (error.response?.status === 401 && localStorage.getItem('accessToken') && !isLoginRequest) {
      // Guardar el rol antes de eliminarlo
      const userRole = localStorage.getItem('userRole')

      // Limpiar storage
      localStorage.removeItem('accessToken')
      localStorage.removeItem('userRole')

      // Determinar la ruta de login según el rol
      let loginRoute = '/'

      switch (userRole) {
        case 'alumno':
          loginRoute = '/login_alumno'
          break
        case 'tutor':
          loginRoute = '/login_tutor'
          break
        case 'super_admin':
          loginRoute = '/login_admin'
          break
        case 'psicologia':
        case 'ciencias_basicas':
        case 'jefatura_academica':
          loginRoute = '/'
          break
        default:
          loginRoute = '/'
      }

      console.log('🔒 Sesión expirada. Redirigiendo al login...')
      window.location.href = loginRoute
    }

    // Para cualquier otro error (incluidos los 401 en login), simplemente rechazar
    return Promise.reject(error)
  },
)

export default apiClient
