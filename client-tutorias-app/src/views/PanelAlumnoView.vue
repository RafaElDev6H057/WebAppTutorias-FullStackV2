<template>
  <div class="min-h-screen bg-gray-900 relative overflow-hidden">
    <!-- Animated Circles -->
    <div class="absolute inset-0 pointer-events-none">
      <div
        v-for="(circle, index) in circles"
        :key="index"
        :class="[
          'absolute rounded-full opacity-30',
          circle.color,
          `animate-float-${(index % 3) + 1}`,
        ]"
        :style="{
          top: `${circle.top}%`,
          left: `${circle.left}%`,
          width: `${circle.size}px`,
          height: `${circle.size}px`,
          animationDelay: `${index * 0.2}s`,
        }"
      ></div>
    </div>

    <!-- Navigation Bar -->
    <nav class="bg-gray-800 border-b border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-20">
          <div class="flex items-center space-x-4">
            <div class="flex-shrink-0">
              <img
                class="h-12 w-12 border-2 border-white"
                src="/EscudoITSF.png"
                alt="Escudo ITSF"
              />
            </div>
            <div>
              <div class="text-white font-medium">
                {{
                  alumno
                    ? `${alumno.nombre} ${alumno.apellido_p} ${alumno.apellido_m}`
                    : 'Cargando...'
                }}
              </div>
              <div class="text-gray-400 text-sm">
                No. Control: {{ alumno?.num_control || 'Cargando...' }}
              </div>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-xl font-bold text-white">Sistema de Tutorías</span>

            <!-- Botón de Constancia (Condicional) -->
            <button
              v-if="estadoTutorias?.es_elegible"
              @click="descargarConstancia"
              :disabled="isDownloading"
              class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg
                v-if="isDownloading"
                class="animate-spin h-5 w-5"
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
              <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              <span>{{ isDownloading ? 'Descargando...' : 'Descargar Constancia' }}</span>
            </button>

            <button
              @click="handleLogout"
              class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors duration-200"
            >
              <span>Cerrar Sesión</span>
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8 relative z-10">
      <h1 class="text-3xl font-bold text-white mb-8">Mis Tutorías</h1>

      <!-- ==================== AVISOS IMPORTANTES ==================== -->
      <div class="mb-8">
        <AvisosAlumno />
      </div>

      <!-- Mensaje de Constancia no disponible -->
      <Transition
        enter-active-class="transition ease-out duration-300"
        enter-from-class="opacity-0 translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-200"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="estadoTutorias && !estadoTutorias.es_elegible"
          class="mb-6 bg-yellow-900/30 border-l-4 border-yellow-500 p-4 rounded-md backdrop-blur-sm"
        >
          <div class="flex items-start">
            <svg
              class="w-6 h-6 text-yellow-400 mr-3 flex-shrink-0"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
            <div class="flex-1">
              <h3 class="text-sm font-bold text-yellow-400 mb-1">📄 Constancia no disponible</h3>
              <p class="text-sm text-yellow-200">
                Debes completar tus <strong>4 tutorías</strong> para poder descargar tu constancia
                de acreditación.
              </p>
              <div class="mt-2 flex items-center">
                <div class="flex-1 bg-gray-700 rounded-full h-2 mr-3">
                  <div
                    class="bg-gradient-to-r from-yellow-500 to-green-500 h-2 rounded-full transition-all duration-500"
                    :style="{
                      width: `${(estadoTutorias.tutorias_completadas / 4) * 100}%`,
                    }"
                  ></div>
                </div>
                <span class="text-xs font-bold text-yellow-400">
                  {{ estadoTutorias.tutorias_completadas }} / 4 completadas
                </span>
              </div>
            </div>
          </div>
        </div>
      </Transition>

      <!-- Mensaje de éxito -->
      <Transition
        enter-active-class="transition ease-out duration-300"
        enter-from-class="opacity-0 translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-200"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="successMessage"
          class="mb-6 bg-green-900/30 border-l-4 border-green-500 p-4 rounded-md backdrop-blur-sm"
        >
          <div class="flex items-start">
            <svg
              class="w-6 h-6 text-green-400 mr-3 flex-shrink-0"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <div class="flex-1">
              <p class="text-sm font-medium text-green-400">{{ successMessage }}</p>
            </div>
            <button @click="successMessage = null" class="text-green-400 hover:text-green-300">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>
      </Transition>

      <!-- Mensaje de error -->
      <Transition
        enter-active-class="transition ease-out duration-300"
        enter-from-class="opacity-0 translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-200"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="errorMessage"
          class="mb-6 bg-red-900/30 border-l-4 border-red-500 p-4 rounded-md backdrop-blur-sm"
        >
          <div class="flex items-start">
            <svg
              class="w-6 h-6 text-red-400 mr-3 flex-shrink-0"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <div class="flex-1">
              <p class="text-sm font-medium text-red-400">{{ errorMessage }}</p>
            </div>
            <button @click="errorMessage = null" class="text-red-400 hover:text-red-300">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>
      </Transition>

      <!-- Cards de Tutorías -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div
          v-for="tutoria in sortedTutorias"
          :key="tutoria.semestre"
          :class="[
            'bg-gray-800 rounded-lg p-6 border-l-4 shadow-lg hover:shadow-xl transition-shadow duration-300',
            {
              'border-green-500': tutoria.estado === 'completada',
              'border-orange-500': tutoria.estado === 'en curso',
              'border-red-500': tutoria.estado === 'pendiente',
            },
          ]"
        >
          <div class="flex justify-between items-start mb-4">
            <h2 class="text-xl font-semibold text-white">Semestre {{ tutoria.semestre }}</h2>
            <span
              :class="[
                'px-2 py-1 text-sm rounded-full',
                {
                  'bg-green-500/20 text-green-400': tutoria.estado === 'completada',
                  'bg-orange-500/20 text-orange-400': tutoria.estado === 'en curso',
                  'bg-red-500/20 text-red-400': tutoria.estado === 'pendiente',
                },
              ]"
            >
              {{
                tutoria.estado === 'completada'
                  ? 'Acreditado'
                  : tutoria.estado === 'en curso'
                    ? 'En curso'
                    : 'Pendiente'
              }}
            </span>
          </div>
          <div class="space-y-3">
            <div class="text-gray-400">
              <p class="text-sm">Tutor</p>
              <p class="text-white">{{ getTutorName(tutoria) || 'Por asignar' }}</p>
            </div>
            <div class="text-gray-400">
              <p class="text-sm">Periodo</p>
              <p class="text-white">{{ tutoria.periodo || 'Pendiente' }}</p>
            </div>
            <div class="text-gray-400">
              <p class="text-sm">Dia</p>
              <p class="text-white">{{ capitalize(tutoria) || 'Pendiente' }}</p>
            </div>
            <div class="text-gray-400">
              <p class="text-sm">Hora</p>
              <p class="text-white">{{ formatoHora(tutoria) || 'Pendiente' }}</p>
            </div>
          </div>
          <button
            v-if="showSolicitarButton(tutoria)"
            @click="solicitarTutoria(tutoria.semestre)"
            class="w-full mt-4 bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2"
          >
            <span>Solicitar Tutoría</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
        </div>
      </div>
    </main>

    <!-- Modal de confirmación -->
    <div
      v-if="mostrarModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-gray-800 p-6 rounded-lg shadow-xl max-w-md w-full">
        <h3 class="text-xl font-bold text-white mb-4">Solicitud de Tutoría</h3>
        <p class="text-gray-300 mb-6">
          Su solicitud para la tutoría del Semestre {{ semestreSolicitado }} ha sido enviada al
          administrador. Se le notificará cuando sea aprobada.
        </p>
        <button
          @click="cerrarModal"
          class="w-full bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
        >
          Entendido
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import AvisosAlumno from '@/components/student/AvisosAlumno.vue'

// ==================== STATE ====================
const mostrarModal = ref(false)
const semestreSolicitado = ref(null)
const alumno = ref(null)
const tutorias = ref([])
const estadoTutorias = ref(null)
const isDownloading = ref(false)
const successMessage = ref(null)
const errorMessage = ref(null)
const router = useRouter()

// ==================== API CALLS ====================

// Obtener datos del alumno con JWT
const fetchAlumnoData = async () => {
  try {
    const token = localStorage.getItem('accessToken')

    if (!token) {
      console.log('No hay token, redirigiendo al login...')
      router.push('/login_alumno')
      return
    }

    const response = await axios.get('http://localhost:8000/api/alumnos/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (response.status === 200) {
      alumno.value = response.data
      console.log('✅ Datos del alumno cargados:', alumno.value)
    }
  } catch (error) {
    console.error('❌ Error al obtener datos del alumno:', error)

    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('alumno') // Limpiar también el viejo storage
      router.push('/login_alumno')
    } else {
      errorMessage.value = 'Error al cargar tus datos. Por favor, intenta de nuevo.'
    }
  }
}

// Obtener estado de tutorías completadas
const fetchEstadoTutorias = async () => {
  try {
    const token = localStorage.getItem('accessToken')

    const response = await axios.get('http://localhost:8000/api/alumnos/me/estado-tutorias', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (response.status === 200) {
      estadoTutorias.value = response.data
      console.log('✅ Estado de tutorías:', estadoTutorias.value)
    }
  } catch (error) {
    console.error('❌ Error al obtener estado de tutorías:', error)
  }
}

// Obtener tutorías del alumno
const fetchTutorias = async () => {
  try {
    if (!alumno.value?.id_alumno) {
      console.error('No se puede obtener tutorías sin id_alumno')
      return
    }

    const response = await axios.get(
      `http://localhost:8000/api/tutorias/alumno/${alumno.value.id_alumno}`,
    )

    tutorias.value = response.data
    console.log('✅ Tutorías cargadas:', tutorias.value)
  } catch (error) {
    console.error('❌ Error al obtener las tutorías:', error)
    errorMessage.value = 'Error al cargar tus tutorías.'
  }
}

// Descargar constancia PDF
const descargarConstancia = async () => {
  try {
    isDownloading.value = true
    errorMessage.value = null

    const token = localStorage.getItem('accessToken')

    const response = await axios.get('http://localhost:8000/api/alumnos/me/constancia-pdf', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      responseType: 'blob', // IMPORTANTE: para recibir el PDF como blob
    })

    // Crear un URL temporal para el blob
    const blob = new Blob([response.data], { type: 'application/pdf' })
    const url = window.URL.createObjectURL(blob)

    // Crear un link temporal y hacer click para descargar
    const link = document.createElement('a')
    link.href = url
    link.download = `Constancia_${alumno.value.nombre}_${alumno.value.num_control}.pdf`
    document.body.appendChild(link)
    link.click()

    // Limpiar
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    successMessage.value = '✅ Constancia descargada exitosamente'
    setTimeout(() => {
      successMessage.value = null
    }, 3000)

    console.log('✅ PDF descargado exitosamente')
  } catch (error) {
    console.error('❌ Error al descargar constancia:', error)

    if (error.response?.status === 404) {
      errorMessage.value = 'No se encontró tu constancia. Contacta al administrador.'
    } else if (error.response?.status === 403) {
      errorMessage.value =
        'No tienes permisos para descargar la constancia. Completa tus 4 tutorías.'
    } else {
      errorMessage.value = 'Error al generar la constancia. Intenta de nuevo.'
    }
  } finally {
    isDownloading.value = false
  }
}

// ==================== COMPUTED ====================
const sortedTutorias = computed(() => {
  return [...tutorias.value].sort((a, b) => a.semestre - b.semestre)
})

// ==================== HELPER FUNCTIONS ====================
const getTutorName = (tutoria) => {
  if (tutoria.tutor) {
    return `${tutoria.tutor.nombre} ${tutoria.tutor.apellido_p} ${tutoria.tutor.apellido_m}`
  }
  return 'Por asignar'
}

const capitalize = (tutoria) => {
  if (tutoria.dia != null) {
    return tutoria.dia.charAt(0).toUpperCase() + tutoria.dia.slice(1)
  }
  return null
}

const formatoHora = (tutoria) => {
  if (tutoria.hora != null) {
    /* eslint-disable-next-line no-unused-vars */
    const [horas, minutos, segundos] = tutoria.hora.split(':').map(Number)
    const ampm = horas < 12 ? 'AM' : 'PM'
    const horaFormateada = `${horas % 12 || 12}:${minutos.toString().padStart(2, '0')} ${ampm}`
    return horaFormateada
  }
  return null
}

const showSolicitarButton = (tutoria) => {
  const index = sortedTutorias.value.findIndex((t) => t.semestre === tutoria.semestre)
  const previousTutorias = sortedTutorias.value.slice(0, index)
  const allPreviousCompleted = previousTutorias.every((t) => t.estado === 'completada')
  return tutoria.estado === 'pendiente' && allPreviousCompleted
}

const handleLogout = () => {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('alumno') // Limpiar también por compatibilidad
  router.push('/login_alumno')
}

const solicitarTutoria = (semestre) => {
  console.log(`Solicitando tutoría para el Semestre ${semestre}`)
  semestreSolicitado.value = semestre
  mostrarModal.value = true
}

const cerrarModal = () => {
  mostrarModal.value = false
}

// ==================== LIFECYCLE ====================
onMounted(async () => {
  await fetchAlumnoData()

  if (alumno.value) {
    await Promise.all([fetchTutorias(), fetchEstadoTutorias()])
  }
})

// ==================== CIRCLES ANIMATION ====================
const circles = [
  { color: 'bg-purple-600', size: 120, top: 5, left: 5 },
  { color: 'bg-purple-400', size: 80, top: 20, left: 80 },
  { color: 'bg-purple-500', size: 150, top: 70, left: 20 },
  { color: 'bg-purple-300', size: 100, top: 40, left: 95 },
  { color: 'bg-purple-700', size: 130, top: 85, left: 70 },
  { color: 'bg-purple-200', size: 60, top: 25, left: 30 },
  { color: 'bg-purple-800', size: 90, top: 60, left: 50 },
  { color: 'bg-purple-100', size: 70, top: 5, left: 90 },
]
</script>

<style scoped>
@keyframes float-1 {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes float-2 {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-15px);
  }
}

@keyframes float-3 {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

.animate-float-1 {
  animation: float-1 4s ease-in-out infinite;
}

.animate-float-2 {
  animation: float-2 6s ease-in-out infinite;
}

.animate-float-3 {
  animation: float-3 5s ease-in-out infinite;
}
</style>
