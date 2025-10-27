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
                class="h-12 w-12 border-2 border-white"
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
            <div class="flex items-center">
              <button
                @click="handleLogout"
                class="bg-coral-500 hover:bg-coral-600 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </nav>

      <!-- Contenido principal -->
      <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <!-- Encabezado y búsqueda -->
        <div
          class="px-4 py-6 sm:px-0 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-x-6"
        >
          <div class="flex items-center justify-between w-full mb-4 sm:mb-0">
            <h1 class="text-3xl font-bold text-gray-900">Dashboard del Tutor</h1>
          </div>
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
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Buscar estudiante..."
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-coral-500 focus:border-coral-500"
            />
          </div>
        </div>

        <!-- Modal para Reporte Integral -->
        <Transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div
            v-if="showReporteIntegralModal"
            class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
          >
            <div
              class="relative top-20 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white"
            >
              <div class="flex justify-end items-center mb-4">
                <button
                  @click="closeReporteIntegralModal"
                  class="text-gray-500 hover:text-gray-700"
                >
                  <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
              <ReporteIntegralTutoria
                v-if="selectedStudent"
                :nombre="selectedStudent.name"
                :num_control="selectedStudent.controlNumber"
              />
            </div>
          </div>
        </Transition>

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
              class="relative top-20 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white"
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
                <PrimerReporteTutoria @cerrar="mostrarModalPrimerReporte = false" />
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

        <!-- Pestañas -->
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8">
            <a
              v-for="tab in tabs"
              :key="tab.id"
              href="#"
              @click.prevent="currentTab = tab.id"
              :class="[
                currentTab === tab.id
                  ? 'border-coral-500 text-coral-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm',
              ]"
            >
              {{ tab.name }}
            </a>
          </nav>
        </div>

        <!-- Tabla de estudiantes -->
        <div class="mt-8 flex flex-col">
          <div class="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
            <div class="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
              <div class="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg bg-white">
                <table v-if="students.length > 0" class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th
                        v-for="header in tableHeaders"
                        :key="header.key"
                        scope="col"
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        {{ header.label }}
                      </th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="student in students" :key="student.id">
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="flex items-center">
                          <div class="ml-4">
                            <div class="text-sm font-medium text-gray-900">
                              {{ student.name }}
                            </div>
                            <div class="text-sm text-gray-500">
                              {{ student.controlNumber }}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm text-gray-900">{{ student.semester }}° Semestre</div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span
                          class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                          :class="
                            student.status === 'en curso'
                              ? 'bg-orange-500/20 text-orange-400'
                              : 'bg-green-500/20 text-green-400'
                          "
                        >
                          {{ student.status }}
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {{ student.tutorialPeriod }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <a
                          href="#"
                          @click.prevent="viewDetails(student)"
                          class="text-coral-600 hover:text-coral-900 mx-4"
                          >Ver detalles</a
                        >
                        <button
                          @click="openReporteIntegralModal(student)"
                          class="px-4 py-2 bg-coral-600 text-white rounded-md hover:bg-coral-700 transition duration-150 ease-in-out"
                        >
                          Reporte Integral
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div v-if="students.length === 0" class="text-center text-gray-500 py-8">
                  No se le está aplicando tutoría a ningún alumno.
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Paginación -->
        <div class="py-3 flex items-center justify-between bg-white mt-4 rounded-lg px-4">
          <div class="flex-1 flex justify-between sm:hidden">
            <button
              @click="prevPage"
              :disabled="currentPage === 1"
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
            >
              Anterior
            </button>
            <button
              @click="nextPage"
              :disabled="currentPage === totalPages"
              class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
            >
              Siguiente
            </button>
          </div>
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                Mostrando
                <span class="font-medium">{{ (currentPage - 1) * itemsPerPage + 1 }}</span>
                a
                <span class="font-medium">{{
                  Math.min(currentPage * itemsPerPage, filteredStudents.length)
                }}</span>
                de
                <span class="font-medium">{{ filteredStudents.length }}</span>
                resultados
              </p>
            </div>
            <div>
              <nav
                class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
                aria-label="Pagination"
              >
                <button
                  @click="prevPage"
                  :disabled="currentPage === 1"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                >
                  <span class="sr-only">Anterior</span>
                  <svg
                    class="h-5 w-5"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </button>
                <button
                  v-for="page in totalPages"
                  :key="page"
                  @click="goToPage(page)"
                  :class="[
                    currentPage === page
                      ? 'z-10 bg-coral-50 border-coral-500 text-coral-600'
                      : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50',
                    'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                  ]"
                >
                  {{ page }}
                </button>
                <button
                  @click="nextPage"
                  :disabled="currentPage === totalPages"
                  class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                >
                  <span class="sr-only">Siguiente</span>
                  <svg
                    class="h-5 w-5"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </button>
              </nav>
            </div>
          </div>
        </div>

        <!-- Modal de detalles -->
        <Transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div v-if="showModal" class="fixed inset-0 z-50 overflow-y-auto">
            <div
              class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
            >
              <div class="fixed inset-0 transition-opacity" aria-hidden="true">
                <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
              </div>

              <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true"
                >&#8203;</span
              >

              <div
                v-if="selectedStudent"
                class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
              >
                <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                  <div class="absolute top-4 right-4">
                    <button
                      @click="closeModal"
                      class="text-gray-400 hover:text-gray-600 transition-colors"
                    >
                      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M6 18L18 6M6 6l12 12"
                        />
                      </svg>
                    </button>
                  </div>

                  <h2 class="text-2xl font-bold mb-6 text-gray-900 border-b pb-2">
                    Detalles del Estudiante
                  </h2>

                  <div class="space-y-6">
                    <div class="bg-gray-50 p-4 rounded-lg">
                      <h3 class="text-lg font-semibold text-coral-600 mb-3">
                        Información del Alumno
                      </h3>
                      <div class="space-y-2">
                        <div class="grid grid-cols-3 gap-2">
                          <span class="text-gray-600 font-medium">Nombre:</span>
                          <span class="col-span-2 text-gray-900"
                            >{{ selectedStudent.nombre }} {{ selectedStudent.apellido_p }}
                            {{ selectedStudent.apellido_m }}</span
                          >
                        </div>
                        <div class="grid grid-cols-3 gap-2">
                          <span class="text-gray-600 font-medium">Número de Control:</span>
                          <span class="col-span-2 text-gray-900">{{
                            selectedStudent.num_control
                          }}</span>
                        </div>
                        <div class="grid grid-cols-3 gap-2">
                          <span class="text-gray-600 font-medium">Carrera:</span>
                          <span class="col-span-2 text-gray-900">{{
                            selectedStudent.carrera
                          }}</span>
                        </div>
                        <div class="grid grid-cols-3 gap-2">
                          <span class="text-gray-600 font-medium">Semestre Actual:</span>
                          <span class="col-span-2 text-gray-900"
                            >{{ selectedStudent.semestre_actual }}°</span
                          >
                        </div>
                      </div>
                    </div>

                    <div class="bg-gray-50 p-4 rounded-lg">
                      <h3 class="text-lg font-semibold text-coral-600 mb-3">
                        Información de la Tutoría
                      </h3>
                      <div class="space-y-2">
                        <div class="grid grid-cols-3 gap-2">
                          <span class="text-gray-600 font-medium">Nivel de Tutoría:</span>
                          <span class="col-span-2 text-gray-900"
                            >{{ selectedStudent.tutoring.semestre }}°</span
                          >
                        </div>
                        <div class="grid grid-cols-3 gap-2">
                          <span class="text-gray-600 font-medium">Periodo:</span>
                          <span class="col-span-2 text-gray-900">{{
                            selectedStudent.tutoring.periodo
                          }}</span>
                        </div>
                        <div class="grid grid-cols-3 gap-2">
                          <span class="text-gray-600 font-medium">Día:</span>
                          <span class="col-span-2 text-gray-900">{{
                            capitalize(selectedStudent.tutoring)
                          }}</span>
                        </div>
                        <div class="grid grid-cols-3 gap-2">
                          <span class="text-gray-600 font-medium">Hora:</span>
                          <span class="col-span-2 text-gray-900">{{
                            formatoHora(selectedStudent.tutoring)
                          }}</span>
                        </div>
                        <div class="mt-4">
                          <span class="text-gray-600 font-medium block mb-1">Observaciones:</span>
                          <p class="text-gray-900 bg-white p-3 rounded border">
                            {{ selectedStudent.tutoring.observaciones || 'Sin observaciones' }}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="mt-6 flex justify-end">
                    <button
                      @click="closeModal"
                      class="bg-coral-500 hover:bg-coral-600 text-white font-medium py-2 px-6 rounded-lg transition-colors duration-200"
                    >
                      Cerrar
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Transition>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import ReporteIntegralTutoria from '@/components/ReporteIntegralTutoria.vue'
import PrimerReporteTutoria from '@/components/PrimerReporteTutoria.vue'
import SegundoReporteTutoria from '@/components/SegundoReporteTutoria.vue'

// ==================== ROUTER ====================
const router = useRouter()

// ==================== STATE ====================
const tutor = ref(null)
const students = ref([])
const selectedStudent = ref(null)

// ==================== UI STATE ====================
const searchQuery = ref('')
const currentTab = ref('current')
const currentPage = ref(1)
const itemsPerPage = 10

// ==================== MODALS STATE ====================
const showModal = ref(false)
const showReporteIntegralModal = ref(false)
const mostrarModalPrimerReporte = ref(false)
const mostrarModalSegundoReporte = ref(false)

// ==================== CONSTANTS ====================
const tabs = [
  { id: 'current', name: 'Tutorados Actuales' },
  { id: 'past', name: 'Tutorados Anteriores' },
]

const tableHeaders = [
  { key: 'name', label: 'Estudiante' },
  { key: 'semester', label: 'Nivel de Tutoría' },
  { key: 'status', label: 'Estado' },
  { key: 'tutorialPeriod', label: 'Periodo' },
  { key: 'actions', label: 'Acciones' },
]

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
const filteredStudents = computed(() => {
  return students.value.filter(
    (student) =>
      (currentTab.value === 'current'
        ? student.status === 'en curso'
        : student.status === 'completada') &&
      (student.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        student.controlNumber.includes(searchQuery.value)),
  )
})

const totalPages = computed(() => Math.ceil(filteredStudents.value.length / itemsPerPage))

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
      await fetchActiveTutoringSessions()
    }
  } catch (error) {
    console.error('Error al obtener datos del tutor:', error)

    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('userRole')
      router.push('/login_tutor')
    }
  }
}

const fetchActiveTutoringSessions = async () => {
  try {
    const response = await axios.get(
      `http://localhost:8000/api/tutorias/tutor/${tutor.value.id_tutor}`,
    )
    const activeTutorings = response.data
    console.log('TUTORIAS ACTIVAS', activeTutorings)

    students.value = await Promise.all(
      activeTutorings.map(async (tutoring) => {
        const studentResponse = await axios.get(
          `http://localhost:8000/api/alumnos/${tutoring.alumno_id}`,
        )
        const student = studentResponse.data

        return {
          id: student.id_alumno,
          name: `${student.nombre} ${student.apellido_p} ${student.apellido_m}`,
          controlNumber: student.num_control,
          semester: tutoring.semestre,
          status: student.estado,
          tutorialPeriod: tutoring.periodo,
          tutoringId: tutoring.id_tutoria,
        }
      }),
    )
  } catch (error) {
    console.error('Error fetching active tutoring sessions:', error)
  }
}

// ==================== MODAL HANDLERS ====================
const openReporteIntegralModal = (student) => {
  selectedStudent.value = student
  showReporteIntegralModal.value = true
}

const closeReporteIntegralModal = () => {
  showReporteIntegralModal.value = false
  selectedStudent.value = null
}

const viewDetails = async (student) => {
  try {
    const tutoringResponse = await axios.get(
      `http://localhost:8000/api/tutorias/alumno/${student.tutoringId}`,
    )
    console.log('STUDENT', student)
    console.log('TUTORIA RESPONSE', tutoringResponse)

    selectedStudent.value = {
      ...tutoringResponse.data.alumno,
      tutoring: tutoringResponse.data,
    }
    showModal.value = true
  } catch (error) {
    console.error('Error fetching student details:', error)
  }
}

const closeModal = () => {
  showModal.value = false
  selectedStudent.value = null
}

// ==================== PAGINATION ====================
const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const goToPage = (page) => {
  currentPage.value = page
}

// ==================== UTILITY FUNCTIONS ====================
const capitalize = (tutoria) => {
  if (tutoria.dia != null) {
    return tutoria.dia.charAt(0).toUpperCase() + tutoria.dia.slice(1)
  }
  return null
}

const formatoHora = (tutoria) => {
  if (tutoria.hora != null) {
    const [horas, minutos] = tutoria.hora.split(':').map(Number)
    const ampm = horas < 12 ? 'AM' : 'PM'
    const horaFormateada = `${horas % 12 || 12}:${minutos.toString().padStart(2, '0')} ${ampm}`
    return horaFormateada
  }
  return null
}

// ==================== AUTH ====================
const handleLogout = () => {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('userRole')
  router.push('/login_tutor')
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
