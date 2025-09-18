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
                class="h-12 w-12 rounded-full object-cover"
                src="/login_alumno.jpg"
                alt="Foto del estudiante"
              />
            </div>
            <div>
              <div class="text-white font-medium">
                {{
                  alumno?.nombre + ' ' + alumno?.apellido_p + ' ' + alumno?.apellido_m ||
                  'Nombre no disponible'
                }}
              </div>
              <div class="text-gray-400 text-sm">
                No. Control: {{ alumno?.num_control || 'No disponible' }}
              </div>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-xl font-bold text-white">Sistema de Tutorías</span>
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

const mostrarModal = ref(false)
const semestreSolicitado = ref(null)
const alumno = ref(null)
const tutorias = ref([])
const router = useRouter()

onMounted(async () => {
  // Recupera los datos del alumno del localStorage
  const storedAlumno = localStorage.getItem('alumno')
  if (storedAlumno) {
    alumno.value = JSON.parse(storedAlumno)
    await fetchTutorias()
  } else {
    // Si no hay datos, redirige al login
    router.push('/login_alumno')
  }
})

const fetchTutorias = async () => {
  try {
    const response = await axios.get(
      `http://localhost:8000/api/tutorias/alumno/${alumno.value.id_alumno}`,
    )
    tutorias.value = response.data
    console.log(tutorias.value[0].tutor)
  } catch (error) {
    console.error('Error al obtener las tutorías:', error)
  }
}

const sortedTutorias = computed(() => {
  return [...tutorias.value].sort((a, b) => a.semestre - b.semestre)
})

const getTutorName = (tutoria) => {
  if (tutoria.tutor) {
    return `${tutoria.tutor.nombre} ${tutoria.tutor.apellido_p} ${tutoria.tutor.apellido_m}`
  }
  return 'Por asignar'
}

const capitalize = (tutoria) => {
  if (tutoria.dia != null) {
    const capitalizedStr = tutoria.dia.charAt(0).toUpperCase() + tutoria.dia.slice(1)
    console.log(capitalizedStr)
    return capitalizedStr
  } else {
    return null
  }
}

const formatoHora = (tutoria) => {
  if (tutoria.hora != null) {
    /* eslint-disable-next-line no-unused-vars */
    const [horas, minutos, segundos] = tutoria.hora.split(':').map(Number)
    const ampm = horas < 12 ? 'AM' : 'PM'
    const horaFormateada = `${horas % 12 || 12}:${minutos.toString().padStart(2, '0')} ${ampm}`
    return horaFormateada
  } else {
    return null
  }
}

const showSolicitarButton = (tutoria) => {
  const index = sortedTutorias.value.findIndex((t) => t.semestre === tutoria.semestre)
  const previousTutorias = sortedTutorias.value.slice(0, index)
  const allPreviousCompleted = previousTutorias.every((t) => t.estado === 'completada')
  return tutoria.estado === 'pendiente' && allPreviousCompleted
}

const handleLogout = () => {
  localStorage.removeItem('alumno')
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
