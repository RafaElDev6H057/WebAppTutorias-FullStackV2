import apiClient from './client'

export const avisosAPI = {
  // ==================== CRUD ====================
  getAll() {
    return apiClient.get('/api/avisos/admin/todos')
  },

  getActivos() {
    return apiClient.get('/api/avisos')
  },

  create(data) {
    return apiClient.post('/api/avisos/admin', data)
  },

  update(id, data) {
    return apiClient.put(`/api/avisos/admin/${id}`, data)
  },

  delete(id) {
    return apiClient.delete(`/api/avisos/admin/${id}`)
  },
}
