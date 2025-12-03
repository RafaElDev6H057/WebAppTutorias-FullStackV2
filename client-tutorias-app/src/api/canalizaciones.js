import apiClient from './client'

export const canalizacionesAPI = {
  // ==================== REPORTES POR DEPARTAMENTO ====================

  /**
   * Descarga el reporte de Psicología para un periodo específico
   * @param {string} periodo - Periodo en formato "22025" (5 dígitos)
   * @returns {Promise} - Blob del archivo Excel
   */
  getPsicologiaReporte(periodo) {
    return apiClient.get(`/api/canalizaciones/psicologia/${periodo}`, {
      responseType: 'blob',
    })
  },

  /**
   * Descarga el reporte de Ciencias Básicas para un periodo específico
   * @param {string} periodo - Periodo en formato "22025" (5 dígitos)
   * @returns {Promise} - Blob del archivo Excel
   */
  getCienciasBasicasReporte(periodo) {
    return apiClient.get(`/api/canalizaciones/ciencias-basicas/${periodo}`, {
      responseType: 'blob',
    })
  },

  /**
   * Descarga el reporte de Jefatura Académica para un periodo específico
   * @param {string} periodo - Periodo en formato "22025" (5 dígitos)
   * @returns {Promise} - Blob del archivo Excel
   */
  getJefaturaAcademicaReporte(periodo) {
    return apiClient.get(`/api/canalizaciones/jefatura-academica/${periodo}`, {
      responseType: 'blob',
    })
  },

  /**
   * Método genérico para descargar reporte según el tipo de departamento
   * @param {string} tipoDepartamento - 'psicologia' | 'ciencias_basicas' | 'jefatura_academica'
   * @param {string} periodo - Periodo en formato "22025" (5 dígitos)
   * @returns {Promise} - Blob del archivo Excel
   */
  getReportePorDepartamento(tipoDepartamento, periodo) {
    const endpoints = {
      psicologia: '/api/canalizaciones/psicologia',
      ciencias_basicas: '/api/canalizaciones/ciencias-basicas',
      jefatura_academica: '/api/canalizaciones/jefatura-academica',
    }

    const endpoint = endpoints[tipoDepartamento]

    if (!endpoint) {
      return Promise.reject(new Error(`Tipo de departamento inválido: ${tipoDepartamento}`))
    }

    return apiClient.get(`${endpoint}/${periodo}`, {
      responseType: 'blob',
    })
  },
}
