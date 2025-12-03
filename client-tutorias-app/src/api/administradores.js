import apiClient from './client'

export const administradoresAPI = {
  // ==================== AUTH ====================
  login(credentials) {
    const formData = new URLSearchParams()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)

    return apiClient.post('/api/administradores/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
  },

  // ==================== PERFIL ====================
  getMe() {
    return apiClient.get('/api/administradores/me')
  },

  // ==================== CRUD ====================
  getAll() {
    return apiClient.get('/api/administradores')
  },

  getById(id) {
    return apiClient.get(`/api/administradores/${id}`)
  },

  create(data) {
    return apiClient.post('/api/administradores', data)
  },

  update(id, data) {
    return apiClient.put(`/api/administradores/${id}`, data)
  },

  delete(id) {
    return apiClient.delete(`/api/administradores/${id}`)
  },
}
