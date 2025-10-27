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
  /**
   * Obtiene una lista paginada de tutores, con opción de búsqueda.
   * Requiere que el interceptor de apiClient añada el token de Admin.
   * @param {number} page Número de página (por defecto 1).
   * @param {number} size Tamaño de la página (por defecto 10).
   * @param {string} search Término de búsqueda (opcional).
   * @returns {Promise<AxiosResponse<TutoresPage>>} La respuesta de Axios con { total_tutores, tutores }.
   */
  getTutores(page = 1, size = 10, search = '') {
    // Construimos la URL base con la paginación
    let url = `/tutores?page=${page}&size=${size}`

    // Si el término de búsqueda no está vacío y tiene al menos 3 caracteres (opcional, pero buena idea)
    if (search) {
      // Codificamos el término de búsqueda por si tiene espacios o caracteres especiales
      url += `&search=${encodeURIComponent(search)}`
    }

    // Hacemos la petición con la URL construida
    // El interceptor de apiClient añadirá el token 'Authorization' automáticamente
    return apiClient.get(url)
  },

  getTutoriasPorTutor(idTutor, page = 1, size = 5, search = '') {
    if (!idTutor) {
      return Promise.reject(new Error('Se requiere el ID del tutor.'))
    }
    let url = `/tutorias/tutor/${idTutor}?page=${page}&size=${size}`
    if (search && search.length >= 3) {
      url += `&search=${encodeURIComponent(search)}`
    }
    // El interceptor de apiClient añade el token automáticamente
    return apiClient.get(url)
  },

  // Aquí podrías añadir otras funciones relacionadas con tutores si las necesitas,
  // como createTutor, updateTutor, deleteTutor, etc., que también usarían apiClient.
  // Ejemplo:
  /*
  deleteTutor(idTutor) {
    return apiClient.delete(`/tutores/${idTutor}`);
  }
  */
}
