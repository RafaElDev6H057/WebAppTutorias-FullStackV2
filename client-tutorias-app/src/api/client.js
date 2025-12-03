import axios from 'axios'
// eslnt-disable-next-line no-unused-vars
// import { useRouter } from 'vue-router'

// ==================== CONFIGURACIÓN BASE ====================
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

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
    // Si el token expiró (401), redirigir al login
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('userRole')

      // Determinar la ruta de login según el rol previo
      const userRole = localStorage.getItem('userRole')
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
        default:
          loginRoute = '/'
      }

      // Redirigir (nota: en composables se puede usar router.push directamente)
      window.location.href = loginRoute
    }

    return Promise.reject(error)
  },
)

export default apiClient
