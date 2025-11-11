<template>
  <!-- Modal Eliminar Tutoría con Confirmación -->
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
          <!-- Header con icono de advertencia -->
          <div class="flex items-start mb-6">
            <div class="flex-shrink-0 bg-red-100 rounded-full p-3 mr-4">
              <svg
                class="w-8 h-8 text-red-600"
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
            </div>
            <div class="flex-1">
              <h2 class="text-xl font-bold text-gray-900 mb-2">⚠️ Confirmar Eliminación</h2>
              <p class="text-sm text-gray-600">
                Esta acción es <strong class="text-red-600">permanente e irreversible</strong>
              </p>
            </div>
            <button
              @click="cerrarModal"
              :disabled="isDeleting"
              class="text-gray-400 hover:text-gray-600 transition-colors disabled:opacity-50 -mt-1"
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

          <!-- Información del alumno -->
          <div v-if="tutoria" class="mb-6 p-4 bg-gray-50 border-l-4 border-red-500 rounded">
            <p class="text-sm text-gray-700 mb-2">Estás a punto de eliminar la tutoría de:</p>
            <div class="font-bold text-gray-900 text-lg">
              {{ tutoria.name }}
            </div>
            <div class="text-sm text-gray-600 mt-1">No. Control: {{ tutoria.controlNumber }}</div>
            <div class="text-sm text-gray-600">
              Semestre: {{ tutoria.semester }}° - Periodo:
              {{ tutoria.tutorialPeriod }}
            </div>
          </div>

          <!-- Advertencia -->
          <div class="mb-4 p-3 bg-yellow-50 border-l-4 border-yellow-400 rounded">
            <div class="flex items-start">
              <svg
                class="w-5 h-5 text-yellow-400 mr-2 flex-shrink-0 mt-0.5"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fill-rule="evenodd"
                  d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                  clip-rule="evenodd"
                />
              </svg>
              <div class="text-sm text-yellow-800">
                <strong>Importante:</strong> Se eliminarán todos los datos relacionados con esta
                tutoría, incluyendo reportes y seguimientos.
              </div>
            </div>
          </div>

          <!-- Input de confirmación de correo -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              🔒 Para confirmar, escribe tu correo electrónico
            </label>
            <input
              v-model="correoConfirmacion"
              type="email"
              :disabled="isDeleting"
              placeholder="tu.correo@example.com"
              class="w-full px-3 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 disabled:bg-gray-100 disabled:cursor-not-allowed transition-all"
              @keyup.enter="eliminarTutoria"
            />
            <p class="text-xs text-gray-500 mt-1">
              Tu correo: <strong class="text-gray-700">{{ tutorEmail }}</strong>
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
              v-if="errorModalEliminar"
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
                <p class="text-sm text-red-800 font-medium">{{ errorModalEliminar }}</p>
              </div>
            </div>
          </Transition>

          <!-- Botones -->
          <div class="flex gap-3 pt-4 border-t">
            <button
              @click="cerrarModal"
              :disabled="isDeleting"
              class="flex-1 px-4 py-2 border-2 border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              Cancelar
            </button>
            <button
              @click="eliminarTutoria"
              :disabled="
                isDeleting ||
                !correoConfirmacion ||
                correoConfirmacion.trim().toLowerCase() !== tutorEmail?.trim().toLowerCase()
              "
              class="flex-1 px-4 py-2 rounded-lg font-bold text-white focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:cursor-not-allowed transition-all inline-flex justify-center items-center shadow-md hover:shadow-lg"
              :class="
                isDeleting ||
                !correoConfirmacion ||
                correoConfirmacion.trim().toLowerCase() !== tutorEmail?.trim().toLowerCase()
                  ? 'bg-gray-400'
                  : 'bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 focus:ring-red-500'
              "
            >
              <svg
                v-if="isDeleting"
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
              <svg
                v-else
                class="w-5 h-5 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
              {{ isDeleting ? 'Eliminando...' : 'Eliminar Tutoría' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

// ==================== PROPS ====================
const props = defineProps({
  show: {
    type: Boolean,
    required: true,
  },
  tutoria: {
    type: Object,
    default: null,
  },
  tutorEmail: {
    type: String,
    required: true,
  },
})

// ==================== EMITS ====================
const emit = defineEmits(['close', 'success'])

// ==================== STATE ====================
const correoConfirmacion = ref('')
const errorModalEliminar = ref(null)
const isDeleting = ref(false)

// ==================== METHODS ====================
const eliminarTutoria = async () => {
  errorModalEliminar.value = null

  // Validar que el correo coincida
  if (correoConfirmacion.value.trim().toLowerCase() !== props.tutorEmail.trim().toLowerCase()) {
    errorModalEliminar.value = 'El correo ingresado no coincide con tu correo registrado'
    return
  }

  if (!props.tutoria?.tutoringId) {
    errorModalEliminar.value = 'No se puede eliminar esta tutoría. ID no disponible.'
    return
  }

  isDeleting.value = true

  try {
    const token = localStorage.getItem('accessToken')
    const response = await axios.delete(
      `http://localhost:8000/api/tutorias/${props.tutoria.tutoringId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )

    if (response.status === 200 || response.status === 204) {
      // Mostrar mensaje de éxito
      alert(`Tutoría de ${props.tutoria.name} eliminada exitosamente`)

      cerrarModal()
      emit('success')
    }
  } catch (err) {
    console.error('Error al eliminar tutoría:', err)

    if (err.response?.status === 404) {
      errorModalEliminar.value = 'La tutoría no fue encontrada. Puede que ya haya sido eliminada.'
    } else if (err.response?.status === 403) {
      errorModalEliminar.value = 'No tienes permisos para eliminar esta tutoría.'
    } else if (err.response?.data?.detail) {
      errorModalEliminar.value = err.response.data.detail
    } else {
      errorModalEliminar.value = 'Error al eliminar la tutoría. Intenta de nuevo.'
    }
  } finally {
    isDeleting.value = false
  }
}

const cerrarModal = () => {
  if (!isDeleting.value) {
    correoConfirmacion.value = ''
    errorModalEliminar.value = null
    emit('close')
  }
}
</script>
