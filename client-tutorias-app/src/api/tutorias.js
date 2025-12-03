import apiClient from './client'

export const tutoriasAPI = {
  // ==================== CRUD ====================
  getAll() {
    return apiClient.get('/api/tutorias')
  },

  getById(id) {
    return apiClient.get(`/api/tutorias/${id}`)
  },

  getByAlumno(idAlumno) {
    return apiClient.get(`/api/tutorias/alumno/${idAlumno}`)
  },

  getByTutor(idTutor, page = 1, size = 5, search = '') {
    if (!idTutor) {
      return Promise.reject(new Error('Se requiere el ID del tutor.'))
    }

    const params = new URLSearchParams()
    params.append('page', page)
    params.append('size', size)

    // Solo agregar search si tiene al menos 3 caracteres
    if (search && search.length >= 3) {
      params.append('search', search)
    }

    return apiClient.get(`/api/tutorias/tutor/${idTutor}?${params.toString()}`)
  },

  create(data) {
    return apiClient.post('/api/tutorias', data)
  },

  update(id, data) {
    return apiClient.put(`/api/tutorias/${id}`, data)
  },

  delete(id) {
    return apiClient.delete(`/api/tutorias/${id}`)
  },

  // ==================== UPLOAD ASSIGNMENT ====================
  uploadAssignment(file) {
    const formData = new FormData()
    formData.append('file', file)

    return apiClient.post('/api/tutorias/upload-assignment', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
}
