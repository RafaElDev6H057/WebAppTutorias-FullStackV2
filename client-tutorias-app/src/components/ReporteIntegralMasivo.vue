<template>
  <div class="fixed inset-0 bg-gray-100 overflow-hidden flex flex-col z-[9999]">
    <div class="flex-1 flex flex-col max-h-screen">
      <!-- Header -->
      <div
        class="bg-gradient-to-r from-coral-600 to-coral-700 shadow-lg p-6 text-white flex-shrink-0"
      >
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-3xl font-bold">Reporte Integral de Tutoría</h1>
            <p class="text-coral-100 text-sm mt-1">Periodo 22025 - Vista Masiva</p>
          </div>
          <button @click="closeModal" class="text-white hover:text-gray-200 transition-colors">
            <svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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

      <!-- Información del Tutor -->
      <div class="bg-white p-6 shadow-md flex-shrink-0">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">Nombre del Tutor</label>
            <p class="text-sm font-semibold text-gray-900">{{ tutorInfo.nombre }}</p>
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1"
              >Departamento Académico</label
            >
            <p class="text-sm font-semibold text-gray-900">{{ tutorInfo.departamento }}</p>
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">Periodo Semestral</label>
            <p class="text-sm font-semibold text-gray-900">{{ tutorInfo.periodo }}</p>
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">Carrera</label>
            <p class="text-sm font-semibold text-gray-900">{{ tutorInfo.carrera }}</p>
          </div>
        </div>
      </div>

      <!-- Toolbar -->
      <div
        class="bg-white p-4 shadow-md flex flex-col md:flex-row justify-between items-start md:items-center gap-4 flex-shrink-0"
      >
        <div class="flex-1 max-w-md">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar alumno por nombre o número de control..."
            class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-coral-500 focus:border-coral-500"
          />
        </div>
        <div class="flex gap-3 items-center">
          <span class="text-sm text-gray-600">
            Mostrando {{ alumnosFiltrados.length }} de {{ totalAlumnos }} alumnos
          </span>
          <button
            v-if="isLoadingMore"
            disabled
            class="px-6 py-2 bg-gray-400 text-white rounded-lg font-medium cursor-not-allowed inline-flex items-center"
          >
            <svg
              class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
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
            Cargando...
          </button>
          <button
            v-else
            @click="guardarTodo"
            :disabled="isSaving || alumnosFiltrados.length === 0"
            class="px-6 py-2 bg-coral-600 text-white rounded-lg font-medium hover:bg-coral-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-coral-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors inline-flex items-center"
          >
            <svg
              v-if="isSaving"
              class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
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
            <svg v-else class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"
              />
            </svg>
            {{ isSaving ? 'Guardando...' : 'Guardar Todo' }}
          </button>
        </div>
      </div>

      <!-- Mensaje de éxito/error -->
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
          class="mx-4 mt-2 p-4 bg-green-50 border-l-4 border-green-500 rounded-md flex items-start flex-shrink-0"
        >
          <svg
            class="w-5 h-5 text-green-500 mr-3 flex-shrink-0 mt-0.5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M5 13l4 4L19 7"
            />
          </svg>
          <div class="flex-1">
            <p class="text-sm font-medium text-green-800">{{ successMessage }}</p>
          </div>
          <button @click="successMessage = null" class="text-green-500 hover:text-green-700 ml-4">
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
          class="mx-4 mt-2 p-4 bg-red-50 border-l-4 border-red-500 rounded-md flex items-start flex-shrink-0"
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
            <p class="text-sm font-medium text-red-800">{{ errorMessage }}</p>
          </div>
          <button @click="errorMessage = null" class="text-red-500 hover:text-red-700 ml-4">
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

      <!-- Tabla de Alumnos con Scroll Horizontal -->
      <div
        class="flex-1 overflow-hidden bg-white shadow-md mx-4 my-2 rounded-lg border border-gray-200"
      >
        <div class="h-full overflow-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50 sticky top-0 z-20">
              <tr>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sticky left-0 bg-gray-50 z-30 border-r border-gray-200 min-w-[200px]"
                >
                  Alumno
                </th>
                <th
                  class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider min-w-[100px]"
                >
                  T. Grupal
                </th>
                <th
                  class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider min-w-[120px]"
                >
                  T. Individual
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider min-w-[180px]"
                >
                  Seguimiento 1
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider min-w-[180px]"
                >
                  Seguimiento 2
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider min-w-[180px]"
                >
                  Seguimiento 3
                </th>
                <th
                  class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider min-w-[180px]"
                >
                  Área Canalizada
                </th>
                <th
                  class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider min-w-[100px]"
                >
                  Mat. Aprob.
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider min-w-[180px]"
                >
                  Mat. No Aprob.
                </th>
                <th
                  class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider min-w-[120px]"
                >
                  Estado
                </th>
                <th
                  class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider sticky right-0 bg-gray-50 z-30 border-l border-gray-200 min-w-[120px]"
                >
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr
                v-for="alumno in alumnosFiltrados"
                :key="alumno.num_control"
                class="hover:bg-gray-50 transition-colors"
              >
                <!-- Columna Alumno (sticky) -->
                <td
                  class="px-6 py-4 whitespace-nowrap sticky left-0 bg-white hover:bg-gray-50 z-10 border-r border-gray-200"
                >
                  <div class="flex flex-col">
                    <span class="text-sm font-medium text-gray-900">{{ alumno.nombre }}</span>
                    <span class="text-xs text-gray-500">{{ alumno.num_control }}</span>
                  </div>
                </td>

                <!-- Tutoría Grupal -->
                <td class="px-4 py-4 whitespace-nowrap text-center">
                  <input
                    v-model.number="alumno.datos.tutoria_grupal"
                    type="number"
                    min="0"
                    max="16"
                    class="w-20 px-3 py-2 text-center border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-coral-500 focus:border-coral-500"
                  />
                </td>

                <!-- Tutoría Individual -->
                <td class="px-4 py-4 whitespace-nowrap text-center">
                  <input
                    v-model.number="alumno.datos.tutoria_individual"
                    type="number"
                    min="0"
                    max="5"
                    class="w-20 px-3 py-2 text-center border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-coral-500 focus:border-coral-500"
                  />
                </td>

                <!-- Seguimiento 1 -->
                <td class="px-4 py-4">
                  <input
                    v-model="alumno.datos.seguimiento_1"
                    type="text"
                    placeholder="Materias..."
                    class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-coral-500 focus:border-coral-500 text-sm"
                  />
                </td>

                <!-- Seguimiento 2 -->
                <td class="px-4 py-4">
                  <input
                    v-model="alumno.datos.seguimiento_2"
                    type="text"
                    placeholder="Materias..."
                    class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-coral-500 focus:border-coral-500 text-sm"
                  />
                </td>

                <!-- Seguimiento 3 -->
                <td class="px-4 py-4">
                  <input
                    v-model="alumno.datos.seguimiento_3"
                    type="text"
                    placeholder="Materias..."
                    class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-coral-500 focus:border-coral-500 text-sm"
                  />
                </td>

                <!-- Área Canalizada (Checkboxes) -->
                <td class="px-4 py-4">
                  <div class="flex flex-col gap-2 text-xs">
                    <label class="flex items-center">
                      <input
                        v-model="alumno.datos.jefatura_academica"
                        type="checkbox"
                        :true-value="1"
                        :false-value="0"
                        class="rounded border-gray-300 text-coral-600 focus:ring-coral-500 h-4 w-4"
                      />
                      <span class="ml-2 text-gray-700">Jef. Acad.</span>
                    </label>
                    <label class="flex items-center">
                      <input
                        v-model="alumno.datos.ciencias_basicas"
                        type="checkbox"
                        :true-value="1"
                        :false-value="0"
                        class="rounded border-gray-300 text-coral-600 focus:ring-coral-500 h-4 w-4"
                      />
                      <span class="ml-2 text-gray-700">C. Básicas</span>
                    </label>
                    <label class="flex items-center">
                      <input
                        v-model="alumno.datos.psicologia"
                        type="checkbox"
                        :true-value="1"
                        :false-value="0"
                        class="rounded border-gray-300 text-coral-600 focus:ring-coral-500 h-4 w-4"
                      />
                      <span class="ml-2 text-gray-700">Psicología</span>
                    </label>
                  </div>
                </td>

                <!-- Materias Aprobadas -->
                <td class="px-4 py-4 whitespace-nowrap text-center">
                  <input
                    v-model.number="alumno.datos.materias_aprobadas"
                    type="number"
                    min="0"
                    class="w-20 px-3 py-2 text-center border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-coral-500 focus:border-coral-500"
                  />
                </td>

                <!-- Materias No Aprobadas -->
                <td class="px-4 py-4">
                  <input
                    v-model="alumno.datos.materias_no_aprobadas"
                    type="text"
                    placeholder="Materias..."
                    class="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-coral-500 focus:border-coral-500 text-sm"
                  />
                </td>

                <!-- Estado -->
                <td class="px-4 py-4 whitespace-nowrap text-center">
                  <span
                    v-if="alumno.estado === 'guardado'"
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800"
                  >
                    <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fill-rule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                    Guardado
                  </span>
                  <span
                    v-else-if="alumno.estado === 'guardando'"
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                  >
                    <svg
                      class="animate-spin w-3 h-3 mr-1"
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
                    Guardando...
                  </span>
                  <span
                    v-else-if="alumno.estado === 'error'"
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800"
                  >
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                    Error
                  </span>
                  <span
                    v-else
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800"
                  >
                    Pendiente
                  </span>
                </td>

                <!-- Acciones (sticky) -->
                <td
                  class="px-4 py-4 whitespace-nowrap text-center sticky right-0 bg-white hover:bg-gray-50 z-10 border-l border-gray-200"
                >
                  <button
                    @click="guardarAlumno(alumno)"
                    :disabled="alumno.estado === 'guardando'"
                    class="px-3 py-2 bg-coral-600 text-white rounded hover:bg-coral-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-coral-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-xs font-medium"
                  >
                    Guardar
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Estado vacío -->
          <div
            v-if="alumnosFiltrados.length === 0 && !isLoadingMore"
            class="text-center py-12 px-4 bg-gray-50"
          >
            <svg
              class="mx-auto h-16 w-16 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
              />
            </svg>
            <h3 class="mt-4 text-lg font-medium text-gray-900">No se encontraron alumnos</h3>
            <p class="mt-2 text-sm text-gray-500">No hay alumnos que coincidan con tu búsqueda.</p>
          </div>
        </div>
      </div>

      <!-- Footer con información -->
      <div class="p-4 bg-white shadow text-sm text-gray-600 flex-shrink-0">
        <p>
          <strong>Total de alumnos:</strong> {{ totalAlumnos }} | <strong>Guardados:</strong>
          {{ alumnosGuardados }} | <strong>Pendientes:</strong> {{ alumnosPendientes }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import TutorService from '@/services/TutorService.js'

// ==================== PROPS ====================
const props = defineProps({
  tutorInfo: {
    type: Object,
    required: true,
  },
  tutorId: {
    type: Number,
    required: true,
  },
})

// ==================== EMITS ====================
const emit = defineEmits(['close', 'success'])

// ==================== STATE ====================
const searchQuery = ref('')
const isSaving = ref(false)
const isLoadingMore = ref(false)
const successMessage = ref(null)
const errorMessage = ref(null)
const alumnos = ref([])
const totalAlumnos = ref(0)

// ==================== COMPUTED ====================
const alumnosFiltrados = computed(() => {
  if (!searchQuery.value) return alumnos.value

  const query = searchQuery.value.toLowerCase()
  return alumnos.value.filter(
    (alumno) =>
      alumno.nombre.toLowerCase().includes(query) ||
      alumno.num_control.toLowerCase().includes(query),
  )
})

const alumnosGuardados = computed(() => {
  return alumnos.value.filter((a) => a.estado === 'guardado').length
})

const alumnosPendientes = computed(() => {
  return alumnos.value.filter((a) => a.estado === 'pendiente').length
})

// ==================== METHODS ====================
const cargarTodosLosAlumnos = async () => {
  isLoadingMore.value = true
  errorMessage.value = null

  try {
    // Hacemos una petición inicial para saber cuántos alumnos hay
    const responseInicial = await TutorService.getTutoriasPorTutor(props.tutorId, 1, 1, '')

    totalAlumnos.value = responseInicial.data.total_tutorias

    // Ahora hacemos una petición con size = total para traer todos
    const response = await TutorService.getTutoriasPorTutor(
      props.tutorId,
      1,
      totalAlumnos.value,
      '',
    )

    alumnos.value = response.data.tutorias.map((tutoria) => ({
      nombre: tutoria.alumno
        ? `${tutoria.alumno.nombre || ''} ${tutoria.alumno.apellido_p || ''} ${tutoria.alumno.apellido_m || ''}`.trim()
        : 'Alumno Desconocido',
      num_control: tutoria.alumno?.num_control || 'N/A',
      estado: 'pendiente',
      datos: {
        tutoria_grupal: 0,
        tutoria_individual: 0,
        seguimiento_1: '',
        seguimiento_2: '',
        seguimiento_3: '',
        jefatura_academica: 0,
        ciencias_basicas: 0,
        psicologia: 0,
        materias_aprobadas: 0,
        materias_no_aprobadas: '',
      },
    }))

    console.log(`Cargados ${alumnos.value.length} alumnos`)
  } catch (error) {
    console.error('Error al cargar alumnos:', error)
    errorMessage.value = 'No se pudieron cargar todos los alumnos. Intenta de nuevo.'
  } finally {
    isLoadingMore.value = false
  }
}

const guardarAlumno = async (alumno) => {
  alumno.estado = 'guardando'
  errorMessage.value = null

  try {
    const token = localStorage.getItem('accessToken')
    const response = await axios.post(
      'http://localhost:8000/api/reportes/integral',
      {
        num_control: alumno.num_control,
        ...alumno.datos,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )

    if (response.status === 201 || response.status === 200) {
      alumno.estado = 'guardado'
      successMessage.value = `Reporte de ${alumno.nombre} guardado exitosamente.`
      setTimeout(() => {
        successMessage.value = null
      }, 3000)
    }
  } catch (error) {
    console.error('Error al guardar reporte:', error)
    alumno.estado = 'error'
    errorMessage.value = `Error al guardar reporte de ${alumno.nombre}. ${error.response?.data?.detail || error.message}`
  }
}

const guardarTodo = async () => {
  isSaving.value = true
  errorMessage.value = null
  let errores = 0
  let exitosos = 0

  for (const alumno of alumnos.value) {
    if (alumno.estado !== 'guardado') {
      try {
        await guardarAlumno(alumno)
        exitosos++
        //eslint-disable-next-line
      } catch (error) {
        errores++
      }
    }
  }

  isSaving.value = false

  if (errores === 0) {
    successMessage.value = `¡Todos los reportes guardados exitosamente! (${exitosos} reportes)`
    setTimeout(() => {
      emit('success')
    }, 2000)
  } else {
    errorMessage.value = `Se guardaron ${exitosos} reportes, pero ${errores} tuvieron errores.`
  }
}

const closeModal = () => {
  emit('close')
}

// ==================== LIFECYCLE ====================
onMounted(async () => {
  await cargarTodosLosAlumnos()
})
</script>

<style scoped>
/* Colores personalizados coral */
.bg-coral-600 {
  background-color: #ff5242;
}
.bg-coral-700 {
  background-color: #ff3d2a;
}
.hover\:bg-coral-700:hover {
  background-color: #ff3d2a;
}
.text-coral-100 {
  color: #fff1f0;
}
.ring-coral-500 {
  --tw-ring-color: #ff6b5b;
}
.focus\:ring-coral-500:focus {
  --tw-ring-color: #ff6b5b;
}
.focus\:border-coral-500:focus {
  border-color: #ff6b5b;
}
.text-coral-600 {
  color: #ff5242;
}

/* Scrollbar personalizado */
.overflow-auto::-webkit-scrollbar {
  width: 12px;
  height: 12px;
}

.overflow-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.overflow-auto::-webkit-scrollbar-thumb {
  background: #ff6b5b;
  border-radius: 10px;
}

.overflow-auto::-webkit-scrollbar-thumb:hover {
  background: #ff5242;
}
</style>
