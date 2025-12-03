import apiClient from './client'

export const alumnosAPI = {
  // ==================== AUTH ====================
  login(credentials) {
    const formData = new URLSearchParams()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)

    return apiClient.post('/api/alumnos/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
  },

  // ==================== PERFIL ====================
  getMe() {
    return apiClient.get('/api/alumnos/me')
  },

  // ==================== CONSTANCIA ====================
  getConstanciaPDF() {
    return apiClient.get('/api/alumnos/me/constancia-pdf', {
      responseType: 'blob',
    })
  },

  // ==================== ESTADO ====================
  getEstadoTutorias() {
    return apiClient.get('/api/alumnos/me/estado-tutorias')
  },

  // ==================== PASSWORD ====================
  setPassword(data) {
    return apiClient.post('/api/alumnos/set-password', data)
  },

  changePassword(data) {
    return apiClient.put('/api/alumnos/change-password', data)
  },

  // ==================== CRUD (ADMIN) ====================
  getAll(page = 1, size = 10, search = '') {
    let url = '/api/alumnos'
    const params = new URLSearchParams()

    params.append('page', page)
    params.append('size', size)

    if (search) {
      params.append('search', search)
    }

    return apiClient.get(`${url}?${params.toString()}`)
  },

  getById(id) {
    return apiClient.get(`/api/alumnos/${id}`)
  },

  create(data) {
    return apiClient.post('/api/alumnos', data)
  },

  update(id, data) {
    return apiClient.put(`/api/alumnos/${id}`, data)
  },

  delete(id) {
    return apiClient.delete(`/api/alumnos/${id}`)
  },

  // ==================== EXCEL ====================
  uploadExcel(file) {
    const formData = new FormData()
    formData.append('file', file)

    return apiClient.post('/api/alumnos/upload-excel', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
}
