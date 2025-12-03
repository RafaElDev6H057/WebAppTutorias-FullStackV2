<template>
  <!-- Modal Crear Tutoría -->
  <Transition
    enter-active-class="transition ease-out duration-300"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition ease-in duration-200"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div v-if="show" class="fixed inset-0 z-[9999] overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen p-4">
        <div class="fixed inset-0 bg-black opacity-50" @click="cerrarModal"></div>

        <div class="relative bg-white rounded-lg shadow-xl max-w-md w-full p-6 z-10">
          <!-- Header -->
          <div class="flex justify-between items-center mb-6 border-b pb-3">
            <h2 class="text-2xl font-bold text-gray-900">Crear Nueva Tutoría</h2>
            <button
              @click="cerrarModal"
              :disabled="isCreating"
              class="text-gray-400 hover:text-gray-600 transition-colors disabled:opacity-50"
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

          <!-- Búsqueda de Alumno -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              🔍 Buscar Alumno <span class="text-red-500">*</span>
            </label>
            <input
              v-model="searchAlumnoQuery"
              @input="buscarAlumnos"
              type="text"
              :disabled="isCreating"
              placeholder="Nombre, apellido o número de control..."
              class="w-full px-3 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-coral-500 focus:border-coral-500 disabled:bg-gray-100 disabled:cursor-not-allowed transition-all"
            />
            <p class="text-xs text-gray-500 mt-1">Mínimo 3 caracteres</p>

            <!-- Dropdown de resultados -->
            <Transition
              enter-active-class="transition ease-out duration-200"
              enter-from-class="opacity-0 translate-y-1"
              enter-to-class="opacity-100 translate-y-0"
              leave-active-class="transition ease-in duration-150"
              leave-from-class="opacity-100"
              leave-to-class="opacity-0"
            >
              <div
                v-if="alumnosEncontrados.length > 0 && !alumnoSeleccionado"
                class="mt-2 max-h-48 overflow-y-auto border-2 border-gray-200 rounded-lg shadow-lg bg-white"
              >
                <div
                  v-for="alumno in alumnosEncontrados"
                  :key="alumno.id_alumno"
                  @click="seleccionarAlumno(alumno)"
                  class="p-3 hover:bg-blue-50 cursor-pointer border-b border-gray-100 last:border-b-0 transition-colors"
                >
                  <div class="font-medium text-gray-900">
                    {{ alumno.nombre }} {{ alumno.apellido_p }} {{ alumno.apellido_m }}
                  </div>
                  <div class="text-sm text-gray-500">
                    {{ alumno.num_control }} - {{ alumno.carrera }}
                  </div>
                </div>
              </div>
            </Transition>

            <!-- Alumno seleccionado -->
            <Transition
              enter-active-class="transition ease-out duration-200"
              enter-from-class="opacity-0 scale-95"
              enter-to-class="opacity-100 scale-100"
              leave-active-class="transition ease-in duration-150"
              leave-from-class="opacity-100"
              leave-to-class="opacity-0"
            >
              <div
                v-if="alumnoSeleccionado"
                class="mt-2 p-3 bg-green-50 border-2 border-green-300 rounded-lg flex items-start justify-between"
              >
                <div class="flex items-start">
                  <svg
                    class="w-5 h-5 text-green-500 mr-2 flex-shrink-0 mt-0.5"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                      clip-rule="evenodd"
                    />
                  </svg>
                  <div>
                    <div class="font-medium text-green-900">
                      {{ alumnoSeleccionado.nombre }} {{ alumnoSeleccionado.apellido_p }}
                      {{ alumnoSeleccionado.apellido_m }}
                    </div>
                    <div class="text-sm text-green-700">{{ alumnoSeleccionado.num_control }}</div>
                  </div>
                </div>
                <button
                  @click="clearAlumnoSelection"
                  :disabled="isCreating"
                  class="text-green-600 hover:text-green-800 disabled:opacity-50"
                >
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
          </div>

          <!-- Semestre -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              📚 Semestre <span class="text-red-500">*</span>
            </label>
            <select
              v-model="semestreSeleccionado"
              :disabled="isCreating"
              class="w-full px-3 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-coral-500 focus:border-coral-500 disabled:bg-gray-100 disabled:cursor-not-allowed transition-all"
            >
              <option value="">Seleccionar semestre...</option>
              <option v-for="sem in 9" :key="sem" :value="sem">{{ sem }}° Semestre</option>
            </select>
          </div>

          <!-- Periodo -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              📅 Periodo <span class="text-red-500">*</span>
            </label>
            <input
              v-model="periodoInput"
              @input="validarPeriodoInput"
              type="text"
              maxlength="5"
              :disabled="isCreating"
              placeholder="22025"
              class="w-full px-3 py-2 border-2 rounded-lg focus:outline-none focus:ring-2 transition-all disabled:bg-gray-100 disabled:cursor-not-allowed"
              :class="
                errorPeriodo
                  ? 'border-red-500 focus:ring-red-500 focus:border-red-500'
                  : 'border-gray-300 focus:ring-coral-500 focus:border-coral-500'
              "
            />
            <p v-if="errorPeriodo" class="text-red-500 text-xs mt-1 flex items-center">
              <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                  clip-rule="evenodd"
                />
              </svg>
              {{ errorPeriodo }}
            </p>
            <p class="text-gray-500 text-xs mt-1">
              Debe empezar con "2" y tener 5 dígitos. Ej: 22025
            </p>
          </div>

          <!-- Mensajes de error -->
          <Transition
            enter-active-class="transition ease-out duration-200"
            enter-from-class="opacity-0 translate-y-1"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition ease-in duration-150"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
          >
            <div
              v-if="errorModalCrear"
              class="mb-4 p-3 bg-red-50 border-l-4 border-red-500 rounded"
            >
              <div class="flex items-start">
                <svg
                  class="w-5 h-5 text-red-500 mr-2 flex-shrink-0"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clip-rule="evenodd"
                  />
                </svg>
                <p class="text-sm text-red-800 font-medium">{{ errorModalCrear }}</p>
              </div>
            </div>
          </Transition>

          <!-- Botones -->
          <div class="flex gap-3 pt-4 border-t">
            <button
              @click="cerrarModal"
              :disabled="isCreating"
              class="flex-1 px-4 py-2 border-2 border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              Cancelar
            </button>
            <button
              @click="crearTutoria"
              :disabled="
                isCreating ||
                !alumnoSeleccionado ||
                !semestreSeleccionado ||
                errorPeriodo ||
                periodoInput.length !== 5
              "
              class="flex-1 px-4 py-2 rounded-lg font-bold text-white focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:cursor-not-allowed transition-all inline-flex justify-center items-center shadow-md hover:shadow-lg"
              :class="
                isCreating ||
                !alumnoSeleccionado ||
                !semestreSeleccionado ||
                errorPeriodo ||
                periodoInput.length !== 5
                  ? 'bg-gray-400'
                  : 'bg-gradient-to-r from-orange-600 to-orange-700 hover:from-orange-700 hover:to-orange-800 focus:ring-orange-500'
              "
            >
              <svg
                v-if="isCreating"
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
              {{ isCreating ? 'Creando...' : 'Crear Tutoría' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { alumnosAPI } from '@/api/alumnos'
import { ref } from 'vue'
import axios from 'axios'

// ==================== PROPS ====================
const props = defineProps({
  show: {
    type: Boolean,
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
const searchAlumnoQuery = ref('')
const alumnosEncontrados = ref([])
const alumnoSeleccionado = ref(null)
const semestreSeleccionado = ref('')
const periodoInput = ref('')
const errorPeriodo = ref(null)
const errorModalCrear = ref(null)
const isCreating = ref(false)

let debounceTimerAlumnos = null

// ==================== METHODS ====================
const buscarAlumnos = async () => {
  clearTimeout(debounceTimerAlumnos)

  if (searchAlumnoQuery.value.length < 3) {
    alumnosEncontrados.value = []
    return
  }

  debounceTimerAlumnos = setTimeout(async () => {
    try {
      const response = await alumnosAPI.getAll(1, 100, searchAlumnoQuery.value)

      alumnosEncontrados.value = response.data.alumnos || response.data
    } catch (error) {
      console.error('Error al buscar alumnos:', error)
      alumnosEncontrados.value = []
    }
  }, 300)
}

const seleccionarAlumno = (alumno) => {
  alumnoSeleccionado.value = alumno
  alumnosEncontrados.value = []
  searchAlumnoQuery.value = `${alumno.nombre} ${alumno.apellido_p} ${alumno.apellido_m}`
}

const clearAlumnoSelection = () => {
  alumnoSeleccionado.value = null
  searchAlumnoQuery.value = ''
}

const validarPeriodoInput = () => {
  errorPeriodo.value = null

  if (periodoInput.value.length === 0) {
    return
  }

  // Solo números
  if (!/^\d+$/.test(periodoInput.value)) {
    errorPeriodo.value = 'El periodo debe contener solo números'
    return
  }

  // Si ya tiene 5 caracteres, validar completo
  if (periodoInput.value.length === 5) {
    if (!periodoInput.value.startsWith('2')) {
      errorPeriodo.value = 'El periodo debe empezar con "2"'
    }
  } else if (periodoInput.value.length > 5) {
    periodoInput.value = periodoInput.value.slice(0, 5)
  }
}

const crearTutoria = async () => {
  errorModalCrear.value = null

  // Validaciones
  if (!alumnoSeleccionado.value) {
    errorModalCrear.value = 'Debes seleccionar un alumno'
    return
  }

  if (!semestreSeleccionado.value) {
    errorModalCrear.value = 'Debes seleccionar un semestre'
    return
  }

  if (periodoInput.value.length !== 5) {
    errorModalCrear.value = 'El periodo debe tener exactamente 5 dígitos'
    return
  }

  if (!periodoInput.value.startsWith('2')) {
    errorModalCrear.value = 'El periodo debe empezar con "2"'
    return
  }

  if (errorPeriodo.value) {
    return
  }

  isCreating.value = true

  try {
    const token = localStorage.getItem('accessToken')
    const response = await axios.post(
      'http://localhost:8000/api/tutorias/',
      {
        periodo: periodoInput.value,
        estado: 'pendiente',
        observaciones: null,
        semestre: parseInt(semestreSeleccionado.value),
        alumno_id: alumnoSeleccionado.value.id_alumno,
        tutor_id: props.tutorId,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )

    if (response.status === 201 || response.status === 200) {
      errorModalCrear.value = null

      // Mostrar mensaje de éxito temporal
      const nombreCompleto = `${alumnoSeleccionado.value.nombre} ${alumnoSeleccionado.value.apellido_p}`
      alert(`Tutoría creada exitosamente para ${nombreCompleto}`)

      cerrarModal()
      emit('success')
    }
  } catch (err) {
    console.error('Error al crear tutoría:', err)

    if (err.response?.data?.detail) {
      errorModalCrear.value = err.response.data.detail
    } else if (err.response?.status === 400) {
      errorModalCrear.value = 'Datos inválidos. Verifica la información.'
    } else if (err.response?.status === 409) {
      errorModalCrear.value = 'Este alumno ya tiene una tutoría asignada para este semestre.'
    } else {
      errorModalCrear.value = 'Error al crear la tutoría. Intenta de nuevo.'
    }
  } finally {
    isCreating.value = false
  }
}

const cerrarModal = () => {
  if (!isCreating.value) {
    searchAlumnoQuery.value = ''
    alumnosEncontrados.value = []
    alumnoSeleccionado.value = null
    semestreSeleccionado.value = ''
    periodoInput.value = ''
    errorPeriodo.value = null
    errorModalCrear.value = null
    emit('close')
  }
}
</script>

<style scoped>
.focus\:ring-coral-500:focus {
  --tw-ring-color: #ff6b5b;
}

.focus\:border-coral-500:focus {
  border-color: #ff6b5b;
}
</style>
