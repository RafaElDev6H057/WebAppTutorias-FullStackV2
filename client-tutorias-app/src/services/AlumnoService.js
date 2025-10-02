import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export default {
  getAlumnos(page = 1, size = 10) {
    return apiClient.get(`/alumnos?page=${page}&size=${size}`)
  },

  // --- NUEVO MÉTODO PARA SUBIR EL ARCHIVO ---
  uploadAlumnos(file) {
    // FormData es el objeto especial para empaquetar archivos
    const formData = new FormData()
    formData.append('file', file)

    // Hacemos la petición POST a la ruta /upload/excel
    return apiClient.post('alumnos/upload-excel', formData, {
      headers: {
        'Content-Type': 'multipart/form-data', // Header especial para archivos
      },
    })
  },
}
