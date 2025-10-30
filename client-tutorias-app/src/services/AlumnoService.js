// src/services/AlumnoService.js

import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// --- Interceptor de Petición (Añade el token) ---
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken') // O la key que uses
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    // Manejar errores de configuración de la petición
    console.error('Error en configuración de petición Axios:', error)
    return Promise.reject(error)
  },
)

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
