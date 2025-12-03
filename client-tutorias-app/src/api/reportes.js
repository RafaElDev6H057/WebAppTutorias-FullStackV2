import apiClient from './client'

export const reportesAPI = {
  // ==================== REPORTE INTEGRAL ====================
  getIntegralByTutoria(idTutoria) {
    return apiClient.get(`/api/reportes/integral/tutoria/${idTutoria}`)
  },

  getIntegralByReporte(id) {
    return apiClient.get(`/api/reportes/integral/${id}`)
  },

  createIntegral(data) {
    return apiClient.post('/api/reportes/integral', data)
  },

  updateIntegral(id, data) {
    return apiClient.put(`/api/reportes/integral/${id}`, data)
  },

  deleteIntegral(id) {
    return apiClient.delete(`/api/reportes/integral/${id}`)
  },

  downloadIntegralPDF(id, periodo) {
    return apiClient.get(`/api/reportes/integral/pdf/tutor/${id}/periodo/${periodo}`, {
      responseType: 'blob',
    })
  },
  // ==================== REPORTE GENERAL 1 ====================
  getGeneral1ByTutor() {
    return apiClient.get('/api/reportes/general-1/tutor')
  },

  getGeneral1ById(id) {
    return apiClient.get(`/api/reportes/general-1/${id}`)
  },

  createGeneral1(data) {
    return apiClient.post('/api/reportes/general-1', data)
  },

  updateGeneral1(id, data) {
    return apiClient.put(`/api/reportes/general-1/${id}`, data)
  },

  deleteGeneral1(id) {
    return apiClient.delete(`/api/reportes/general-1/${id}`)
  },

  downloadGeneral1PDF(id) {
    return apiClient.get(`/api/reportes/general-1/${id}/pdf`, {
      responseType: 'blob',
    })
  },

  // ==================== REPORTE GENERAL 2 ====================
  getGeneral2ByTutor() {
    return apiClient.get('/api/reportes/general-2/tutor')
  },

  getGeneral2ById(id) {
    return apiClient.get(`/api/reportes/general-2/${id}`)
  },

  createGeneral2(data) {
    return apiClient.post('/api/reportes/general-2', data)
  },

  updateGeneral2(id, data) {
    return apiClient.put(`/api/reportes/general-2/${id}`, data)
  },

  deleteGeneral2(id) {
    return apiClient.delete(`/api/reportes/general-2/${id}`)
  },

  downloadGeneral2PDF(id) {
    return apiClient.get(`/api/reportes/general-2/${id}/pdf`, {
      responseType: 'blob',
    })
  },
}
