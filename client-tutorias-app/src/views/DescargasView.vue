<template>
  <div class="min-h-screen bg-slate-50 p-8">
    <!-- Header Simple -->
    <header
      class="flex justify-between items-center mb-12 bg-white p-6 rounded-2xl shadow-sm border border-slate-100"
    >
      <div class="flex items-center gap-4">
        <div class="p-3 bg-blue-100 rounded-xl">
          <!-- Icono genérico de edificio/departamento -->
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-8 w-8 text-blue-600"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
            />
          </svg>
        </div>
        <div>
          <h1 class="text-2xl font-bold text-slate-800">{{ tituloDepartamento }}</h1>
          <p class="text-slate-500 text-sm">Panel de Descarga de Reportes</p>
        </div>
      </div>
      <button
        @click="logout"
        class="text-red-500 hover:text-red-700 font-medium px-4 py-2 rounded-lg hover:bg-red-50 transition-colors flex items-center gap-2"
      >
        <span>Cerrar Sesión</span>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
          />
        </svg>
      </button>
    </header>

    <!-- Contenido Principal -->
    <main class="max-w-4xl mx-auto">
      <div class="bg-white rounded-3xl p-8 shadow-lg border border-slate-100 text-center">
        <div class="mb-8">
          <h2 class="text-xl font-semibold text-slate-700 mb-2">Seleccione el Periodo</h2>
          <p class="text-slate-500 mb-6">
            Descargue el reporte de alumnos canalizados correspondiente a su área.
          </p>

          <!-- Selector de Periodo (Ejemplo estático, puedes hacerlo dinámico) -->
          <select
            v-model="periodoSeleccionado"
            class="px-4 py-2 border rounded-lg bg-slate-50 text-slate-700 focus:ring-2 focus:ring-blue-500 outline-none w-64 mx-auto block"
          >
            <option value="22025">22025</option>
          </select>
        </div>

        <!-- Botón de Acción -->
        <button
          @click="descargarReporte"
          :disabled="cargando"
          class="group relative inline-flex items-center justify-center px-8 py-4 font-bold text-white transition-all duration-200 bg-blue-600 font-lg rounded-2xl hover:bg-blue-700 hover:shadow-lg focus:outline-none ring-offset-2 focus:ring-2 disabled:opacity-50 disabled:cursor-not-allowed w-full max-w-md"
        >
          <span v-if="cargando" class="flex items-center gap-2">
            <svg
              class="animate-spin h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            Generando Excel...
          </span>
          <span v-else class="flex items-center gap-3">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
              />
            </svg>
            Descargar Reporte Excel
          </span>
        </button>

        <p
          v-if="mensaje"
          :class="{ 'text-green-500': exito, 'text-red-500': !exito }"
          class="mt-4 font-medium"
        >
          {{ mensaje }}
        </p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const periodoSeleccionado = ref('22025')
const cargando = ref(false)
const mensaje = ref('')
const exito = ref(false)
const rolUsuario = ref('')

// Configuración de Endpoints según el Rol
const configRoles = {
  psicologia: {
    titulo: 'Departamento de Psicología',
    endpoint: 'psicologia',
  },
  ciencias_basicas: {
    titulo: 'Departamento de Ciencias Básicas',
    endpoint: 'ciencias-basicas',
  },
  jefatura_academica: {
    titulo: 'Jefatura Académica',
    endpoint: 'jefatura-academica',
  },
}

onMounted(() => {
  // Recuperar rol y validar sesión
  const token = localStorage.getItem('accessToken')
  const role = localStorage.getItem('userRole')

  if (!token || !role) {
    router.push('/login_admin')
    return
  }

  rolUsuario.value = role

  // Si un Super Admin intenta entrar aquí, lo mandamos a su dashboard real
  if (role === 'super_admin') {
    router.push('/login_admin/dashboard')
  }
})

const tituloDepartamento = computed(() => {
  return configRoles[rolUsuario.value]?.titulo || 'Panel de Departamento'
})

const logout = () => {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('userRole')
  router.push('/')
}

const descargarReporte = async () => {
  cargando.value = true
  mensaje.value = ''

  try {
    const roleConfig = configRoles[rolUsuario.value]
    if (!roleConfig) throw new Error('Rol no reconocido')

    // Construir URL: /api/canalizaciones/psicologia/{periodo}
    const url = `http://localhost:8000/api/canalizaciones/${roleConfig.endpoint}/${periodoSeleccionado.value}`

    const token = localStorage.getItem('accessToken')

    const response = await axios.get(url, {
      headers: { Authorization: `Bearer ${token}` },
      responseType: 'blob', // Importante para descargas
    })

    // Crear enlace de descarga invisible
    const href = URL.createObjectURL(response.data)
    const link = document.createElement('a')
    link.href = href

    // Extraer nombre de archivo del header o generarlo
    const contentDisposition = response.headers['content-disposition']
    let fileName = `Reporte_${roleConfig.endpoint}_${periodoSeleccionado.value}xlsx`
    if (contentDisposition) {
      const fileNameMatch = contentDisposition.match(/filename="?([^"]+)"?/)
      if (fileNameMatch.length === 2) fileName = fileNameMatch[1]
    }

    link.setAttribute('download', fileName)
    document.body.appendChild(link)
    link.click()

    // Limpieza
    document.body.removeChild(link)
    URL.revokeObjectURL(href)

    exito.value = true
    mensaje.value = 'Descarga iniciada correctamente.'
  } catch (error) {
    console.error(error)
    exito.value = false
    if (error.response?.status === 403) {
      mensaje.value = 'Error: No tiene permisos para descargar este reporte.'
    } else if (error.response?.status === 404) {
      mensaje.value = 'No se encontraron datos para el periodo seleccionado.'
    } else {
      mensaje.value = 'Ocurrió un error al descargar el reporte.'
    }
  } finally {
    cargando.value = false
  }
}
</script>
