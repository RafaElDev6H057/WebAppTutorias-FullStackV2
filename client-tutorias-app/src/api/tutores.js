import apiClient from './client'

export const tutoresAPI = {
  // ==================== AUTH ====================
  login(credentials) {
    const formData = new URLSearchParams()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)

    return apiClient.post('/api/tutores/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
  },

  // ==================== PERFIL ====================
  getMe() {
    return apiClient.get('/api/tutores/me')
  },

  // ==================== PASSWORD ====================
  setPassword(data) {
    return apiClient.post('api/tutores/set-password', data)
  },

  changePassword(data) {
    return apiClient.put('/api/tutores/change-password', data)
  },

  // ==================== CRUD (ADMIN) ====================
  getAll(page = 1, size = 10, search = '') {
    let url = '/api/tutores'
    const params = new URLSearchParams()

    params.append('page', page)
    params.append('size', size)

    if (search) {
      params.append('search', search)
    }

    return apiClient.get(`${url}?${params.toString()}`)
  },

  getById(id) {
    return apiClient.get(`/api/tutores/${id}`)
  },

  create(data) {
    return apiClient.post('/api/tutores', data)
  },

  update(id, data) {
    return apiClient.put(`/api/tutores/${id}`, data)
  },

  delete(id) {
    return apiClient.delete(`/api/tutores/${id}`)
  },
}
