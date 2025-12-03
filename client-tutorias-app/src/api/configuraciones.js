import apiClient from './client'

export const configuracionesAPI = {
  // ==================== CONFIGURACION ETAPAS ====================
  getEtapaActual() {
    return apiClient.get('/api/configuracion')
  },

  updateEtapaActual(data) {
    return apiClient.put('/api/configuracion', data)
  },

  // ==================== CONFIGURACION PLANTILLAS ====================
  updatePlantillaIntegral(file) {
    const formData = new FormData()
    formData.append('file', file)

    return apiClient.post('/api/configuracion/upload-template/integral', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  resetPlantillaIntegral() {
    return apiClient.post('/api/configuracion/reset-template/integral')
  },
}
