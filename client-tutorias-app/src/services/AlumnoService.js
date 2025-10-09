// src/services/AlumnoService.js

import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export default {
  // MODIFICAMOS ESTE MÉTODO
  getAlumnos(page = 1, size = 10, search = '') {
    // Construimos la URL base con la paginación
    let url = `/alumnos?page=${page}&size=${size}`

    // Si el término de búsqueda no está vacío, lo añadimos como parámetro
    if (search) {
      url += `&search=${search}`
    }

    // Hacemos la petición con la URL construida
    return apiClient.get(url)
  },

  uploadAlumnos(file) {
    const formData = new FormData()
    formData.append('file', file)
    return apiClient.post('alumnos/upload-excel', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
}
