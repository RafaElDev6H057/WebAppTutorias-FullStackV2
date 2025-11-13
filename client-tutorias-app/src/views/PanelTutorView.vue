<template>
  <div class="min-h-screen bg-gray-100 relative overflow-hidden">
    <!-- Animated Circles -->
    <div class="absolute inset-0 pointer-events-none overflow-hidden">
      <div
        v-for="(circle, index) in circles"
        :key="index"
        :class="[
          'absolute rounded-full opacity-70',
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

    <!-- Dashboard content -->
    <div class="relative z-10">
      <!-- Barra de navegación -->
      <nav class="bg-white shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between h-16">
            <div class="flex items-center">
              <img
                class="h-12 w-12 border-2 border-white rounded-full"
                src="/EscudoITSF.png"
                alt="Escudo ITSF"
              />
              <div class="ml-4">
                <div class="text-lg font-medium text-gray-900">
                  {{
                    tutor?.nombre + ' ' + tutor?.apellido_p + ' ' + tutor?.apellido_m ||
                    'Nombre no disponible'
                  }}
                </div>
                <div class="text-sm text-gray-500">{{ tutor?.correo }}</div>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <button
                @click="openChangePasswordModal"
                class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Cambiar Contraseña
              </button>
              <button
                @click="descargarPDFReporteIntegral"
                :disabled="loading || !studentsData.length"
                class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed inline-flex items-center gap-2"
              >
                <svg
                  v-if="loading"
                  class="animate-spin h-4 w-4"
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
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
                {{ loading ? 'Generando...' : 'Descargar PDF' }}
              </button>
              <button
                @click="handleLogout"
                class="bg-coral-500 hover:bg-coral-600 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </nav>

      <!-- Contenido principal -->
      <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <BannerPasswordWarning
          :show="tutor?.requires_password_change"
          @change-password="openChangePasswordModal"
        />

        <!-- Encabezado y búsqueda -->
        <div
          class="px-4 py-6 sm:px-0 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-x-6"
        >
          <div class="flex items-center justify-between w-full mb-4 sm:mb-0 gap-4">
            <h1 class="text-3xl font-bold text-gray-900">Dashboard del Tutor</h1>
            <button
              @click="abrirModalCrear"
              class="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-md font-medium inline-flex items-center gap-2 transition-colors shadow-md hover:shadow-lg"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 4v16m8-8H4"
                />
              </svg>
              Crear Tutoría
            </button>
          </div>
          <button
            @click="openReporteIntegralMasivo"
            class="w-44 px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition-colors font-medium"
          >
            Reporte Integral
          </button>
          <button
            @click="mostrarModalPrimerReporte = true"
            class="w-44 px-4 py-2 bg-coral-600 text-white rounded-md hover:bg-orange-600 transition-colors font-medium"
          >
            1° Reporte
          </button>
          <button
            @click="mostrarModalSegundoReporte = true"
            class="w-44 px-4 py-2 bg-coral-600 text-white rounded-md hover:bg-orange-600 transition-colors font-medium"
          >
            2° Reporte
          </button>
          <div class="w-full sm:w-64">
            <BaseSearchInput
              v-model="searchQuery"
              :disabled="loading"
              placeholder="Buscar estudiante..."
            />
          </div>
        </div>

        <!-- Mensaje de Error -->
        <Transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="opacity-0 translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <div
            v-if="error"
            class="mx-4 mb-4 p-4 bg-red-50 border-l-4 border-red-500 rounded-md flex items-start"
          >
            <svg
              class="w-5 h-5 text-red-500 mr-3 flex-shrink-0 mt-0.5"
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
              <p class="text-sm font-medium text-red-800">{{ error }}</p>
            </div>
            <button @click="error = null" class="text-red-500 hover:text-red-700 ml-4">
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
        </Transition>

        <!-- Tabla de Alumnos Tutorados (COMPONENTE) -->
        <TablaAlumnosTutorados
          :students="students"
          :loading="loading"
          :search-query="searchQuery"
          :current-page="currentPage"
          :total-pages="totalPages"
          :total-items="totalItems"
          :items-per-page="itemsPerPage"
          @view-details="viewDetails"
          @delete-tutoria="abrirModalEliminar"
          @prev-page="prevPage"
          @next-page="nextPage"
          @go-to-page="goToPage"
        />

        <!-- Modal de detalles del estudiante -->
        <ModalDetallesEstudiante :show="showModal" :student="selectedStudent" @close="closeModal" />

        <!-- Modal de Cambio de Contraseña -->
        <ModalCambiarPassword
          :show="showChangePasswordModal"
          user-type="tutor"
          :requires-password-change="tutor?.requires_password_change"
          :current-email="tutor?.correo"
          @close="showChangePasswordModal = false"
          @success="handlePasswordChanged"
        />

        <!-- Modal para Primer Reporte -->
        <Transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div
            v-if="mostrarModalPrimerReporte"
            class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
          >
            <div
              class="relative top-20 mx-auto p-5 border w-11/12 max-w-5xl shadow-lg rounded-md bg-white"
            >
              <div class="p-4 border-b flex justify-end items-center">
                <button
                  @click="mostrarModalPrimerReporte = false"
                  class="text-gray-500 hover:text-gray-700"
                >
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
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
              <div class="p-4">
                <ReporteIndividual1 @cerrar="mostrarModalPrimerReporte = false" />
              </div>
            </div>
          </div>
        </Transition>

        <!-- Modal para Segundo Reporte -->
        <Transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div
            v-if="mostrarModalSegundoReporte"
            class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
          >
            <div
              class="relative top-20 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white"
            >
              <div class="p-4 border-b flex justify-end items-center">
                <button
                  @click="mostrarModalSegundoReporte = false"
                  class="text-gray-500 hover:text-gray-700"
                >
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
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
              <div class="p-4">
                <SegundoReporteTutoria @cerrar="mostrarModalSegundoReporte = false" />
              </div>
            </div>
          </div>
        </Transition>
      </main>
    </div>

    <!-- Modal Reporte Integral Masivo -->
    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="showReporteIntegralMasivo" class="fixed inset-0 z-[9999]">
        <ReporteIntegralMasivo
          :tutor-info="{
            nombre: tutor?.nombre + ' ' + tutor?.apellido_p + ' ' + tutor?.apellido_m,
            departamento: 'Sistemas Computacionales',
            periodo: '22025',
            carrera: 'Ingeniería en Sistemas',
          }"
          :tutor-id="tutor?.id_tutor"
          @close="closeReporteIntegralMasivo"
          @success="handleReporteIntegralSuccess"
        />
      </div>
    </Transition>

    <!-- Modal Crear Tutoría (COMPONENTE) -->
    <ModalCrearTutoria
      :show="showModalCrearTutoria"
      :tutor-id="tutor?.id_tutor"
      @close="showModalCrearTutoria = false"
      @success="handleTutoriaCreada"
    />

    <!-- Modal Eliminar Tutoría (COMPONENTE) -->
    <ModalEliminarTutoria
      :show="showModalEliminarTutoria"
      :tutoria="tutoriaAEliminar"
      :tutor-email="tutor?.correo"
      @close="showModalEliminarTutoria = false"
      @success="handleTutoriaEliminada"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import TutorService from '@/services/TutorService.js'
import ReporteIntegralMasivo from '@/components/ReporteIntegralMasivo.vue'
import SegundoReporteTutoria from '@/components/SegundoReporteTutoria.vue'
import BaseSearchInput from '@/components/ui/BaseSearchInput.vue'
import ReporteIndividual1 from '@/components/tutor/ReporteIndividual1.vue'
import TablaAlumnosTutorados from '@/components/tutor/TablaAlumnosTutorados.vue'
import ModalCrearTutoria from '@/components/tutor/ModalCrearTutoria.vue'
import ModalEliminarTutoria from '@/components/tutor/ModalEliminarTutoria.vue'
import ModalCambiarPassword from '@/components/shared/ModalCambiarPassword.vue'
import ModalDetallesEstudiante from '@/components/tutor/ModalDetallesEstudiante.vue'
import BannerPasswordWarning from '@/components/shared/BannerPasswordWarning.vue'

// ==================== ROUTER ====================
const router = useRouter()

// ==================== STATE ====================
const tutor = ref(null)
const studentsData = ref([])
const selectedStudent = ref(null)
const totalItems = ref(0)
let debounceTimer = null

// ==================== UI STATE ====================
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = ref(5)
const loading = ref(false)
const error = ref(null)

// ==================== MODALS STATE ====================
const showModal = ref(false)
const mostrarModalPrimerReporte = ref(false)
const mostrarModalSegundoReporte = ref(false)
const showChangePasswordModal = ref(false)
const showReporteIntegralMasivo = ref(false)
const showModalCrearTutoria = ref(false)
const showModalEliminarTutoria = ref(false)
const tutoriaAEliminar = ref(null)

// ==================== PASSWORD CHANGE STATE ====================
const passwordForm = ref({
  correo: '',
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})
const passwordChangeError = ref(null)
const passwordChangeSuccess = ref(false)

// ==================== CONSTANTS ====================
const circles = [
  { color: 'bg-coral-500', size: 96, top: 10, left: 5 },
  { color: 'bg-navy-600', size: 64, top: 20, left: 80 },
  { color: 'bg-coral-400', size: 128, top: 70, left: 20 },
  { color: 'bg-navy-300', size: 80, top: 40, left: 95 },
  { color: 'bg-coral-300', size: 112, top: 85, left: 70 },
  { color: 'bg-navy-400', size: 48, top: 55, left: 10 },
  { color: 'bg-coral-600', size: 72, top: 60, left: 50 },
  { color: 'bg-navy-500', size: 56, top: 5, left: 90 },
  { color: 'bg-coral-500', size: 88, top: 80, left: 40 },
  { color: 'bg-navy-300', size: 40, top: 90, left: 10 },
  { color: 'bg-coral-400', size: 104, top: 15, left: 60 },
  { color: 'bg-navy-400', size: 68, top: 50, left: 85 },
]

// ==================== COMPUTED ====================
const students = computed(() => {
  return studentsData.value
})

const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value))

// ==================== API CALLS ====================
const fetchCurrentTutor = async () => {
  try {
    const token = localStorage.getItem('accessToken')

    if (!token) {
      console.log('No hay token, redirigiendo al login...')
      router.push('/login_tutor')
      return
    }

    const response = await axios.get('http://localhost:8000/api/tutores/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (response.status === 200) {
      tutor.value = response.data
      console.log('Tutor cargado:', tutor.value)

      passwordForm.value.correo = tutor.value.correo

      await fetchAssignedStudents(currentPage.value)
    }
  } catch (err) {
    console.error('Error al obtener datos del tutor:', err)

    if (err.response && (err.response.status === 401 || err.response.status === 403)) {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('userRole')
      router.push('/login_tutor')
    }
  }
}

const fetchAssignedStudents = async (page) => {
  if (!tutor.value || tutor.value.id_tutor === null) {
    error.value = 'Datos del tutor no disponibles.'
    return
  }

  // loading.value = true
  error.value = null

  try {
    const response = await TutorService.getTutoriasPorTutor(
      tutor.value.id_tutor,
      page,
      itemsPerPage.value,
      searchQuery.value,
    )
    console.log(response.data)

    totalItems.value = response.data.total_tutorias

    studentsData.value = response.data.tutorias.map((tutoria) => ({
      id: tutoria.alumno?.id_alumno || null,
      name: tutoria.alumno
        ? `${tutoria.alumno.nombre || ''} ${tutoria.alumno.apellido_p || ''} ${tutoria.alumno.apellido_m || ''}`.trim()
        : 'Alumno Desconocido',
      controlNumber: tutoria.alumno?.num_control || 'N/A',
      semester: tutoria.semestre,
      status: tutoria.alumno?.estado || 'N/A',
      tutorialPeriod: tutoria.periodo,
      tutoringId: tutoria.id_tutoria,
      nombre: tutoria.alumno
        ? `${tutoria.alumno.nombre || ''} ${tutoria.alumno.apellido_p || ''} ${tutoria.alumno.apellido_m || ''}`.trim()
        : 'Alumno Desconocido',
      num_control: tutoria.alumno?.num_control || 'N/A',
    }))
  } catch (err) {
    console.error('Error al obtener las tutorías asignadas:', err)
    if (
      err.response &&
      err.response.status === 400 &&
      err.response.data.detail?.includes('string_too_short')
    ) {
      error.value = 'Favor de ingresar mínimo 3 caracteres a buscar.'
    } else if (err.response?.status !== 401 && err.response?.status !== 403) {
      error.value = 'No se pudo cargar la lista de alumnos asignados.'
    }
    studentsData.value = []
    totalItems.value = 0
  } finally {
    loading.value = false
  }
}

// ==================== PASSWORD CHANGE HANDLERS ====================
const openChangePasswordModal = () => {
  showChangePasswordModal.value = true
  passwordChangeError.value = null
  passwordChangeSuccess.value = false
  passwordForm.value = {
    correo: tutor.value?.correo || '',
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  }
}

// ==================== TUTORÍA HANDLERS ====================
const handleTutoriaCreada = async () => {
  showModalCrearTutoria.value = false
  await fetchAssignedStudents(currentPage.value)
}

const abrirModalCrear = () => {
  showModalCrearTutoria.value = true
}

const abrirModalEliminar = (student) => {
  tutoriaAEliminar.value = student
  showModalEliminarTutoria.value = true
}

const handleTutoriaEliminada = async () => {
  showModalEliminarTutoria.value = false
  tutoriaAEliminar.value = null
  await fetchAssignedStudents(1)
}

// ==================== SEARCH WATCHER ====================
watch(searchQuery, () => {
  clearTimeout(debounceTimer)

  debounceTimer = setTimeout(() => {
    currentPage.value = 1
    fetchAssignedStudents()
  }, 500)
})

// ==================== MODAL HANDLERS ====================
const viewDetails = async (student) => {
  try {
    const tutoringResponse = await axios.get(
      `http://localhost:8000/api/tutorias/alumno/${student.tutoringId}`,
    )

    selectedStudent.value = {
      ...tutoringResponse.data.alumno,
      tutoring: tutoringResponse.data,
    }
    showModal.value = true
  } catch (err) {
    console.error('Error fetching student details:', err)
    error.value = 'No se pudieron cargar los detalles del estudiante.'
  }
}

const closeModal = () => {
  showModal.value = false
  selectedStudent.value = null
}

const openReporteIntegralMasivo = () => {
  showReporteIntegralMasivo.value = true
}

const closeReporteIntegralMasivo = () => {
  showReporteIntegralMasivo.value = false
}

const handleReporteIntegralSuccess = () => {
  closeReporteIntegralMasivo()
}

// Handler de éxito
const handlePasswordChanged = async () => {
  showChangePasswordModal.value = false

  // Actualizar el estado del tutor
  if (tutor.value) {
    tutor.value.requires_password_change = false
  }
}

// ==================== PAGINATION ====================
const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    fetchAssignedStudents(currentPage.value)
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    fetchAssignedStudents(currentPage.value)
  }
}

const goToPage = (page) => {
  currentPage.value = page
  fetchAssignedStudents(page)
}

// ==================== AUTH ====================
const handleLogout = () => {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('userRole')
  router.push('/login_tutor')
}

// ==================== DESCARGA PDF ====================
const descargarPDFReporteIntegral = async () => {
  try {
    loading.value = true
    const token = localStorage.getItem('accessToken')

    const periodo = studentsData.value[0]?.tutorialPeriod || '22025'

    const response = await axios.get(
      `http://localhost:8000/api/reportes/integral/pdf/tutor/${tutor.value.id_tutor}/periodo/${periodo}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        responseType: 'blob',
      },
    )

    const blob = new Blob([response.data], { type: 'application/pdf' })
    const url = window.URL.createObjectURL(blob)

    const link = document.createElement('a')
    link.href = url
    link.download = `Reporte_Integral_${tutor.value.nombre}_${periodo}.pdf`
    document.body.appendChild(link)
    link.click()

    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    console.log('✅ PDF descargado exitosamente')
  } catch (err) {
    console.error('Error al descargar PDF:', err)
    if (err.response?.status === 404) {
      error.value = 'No se encontraron reportes integrales para descargar.'
    } else {
      error.value = 'Error al generar el PDF. Intenta de nuevo.'
    }
  } finally {
    loading.value = false
  }
}

// ==================== LIFECYCLE ====================
onMounted(async () => {
  await fetchCurrentTutor()
})
</script>

<style>
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

/* Animaciones para los círculos */
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

/* Colores personalizados */
.bg-coral-300 {
  background-color: #ff9f92;
}
.bg-coral-400 {
  background-color: #ff8576;
}
.bg-coral-500 {
  background-color: #ff6b5b;
}
.bg-coral-600 {
  background-color: #ff5242;
}

.bg-navy-300 {
  background-color: #4a5568;
}
.bg-navy-400 {
  background-color: #2d3748;
}
.bg-navy-500 {
  background-color: #1a202c;
}
.bg-navy-600 {
  background-color: #171923;
}

.text-coral-600 {
  color: #ff5242;
}
.hover\:bg-coral-600:hover {
  background-color: #ff5242;
}
.hover\:text-coral-900:hover {
  color: #cc2d1d;
}
.bg-coral-50 {
  background-color: #fff1f0;
}
.border-coral-500 {
  border-color: #ff6b5b;
}
</style>
