<template>
  <transition name="fade">
    <div
      v-if="show"
      class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-75 px-4"
    >
      <div
        class="bg-white rounded-lg shadow-2xl w-full max-w-lg mx-auto relative transform transition-all"
      >
        <!-- ==================== ESTADO: CARGANDO ==================== -->
        <div v-if="uploadState === 'uploading'" class="p-8 text-center">
          <div class="flex justify-center mb-4">
            <svg
              class="animate-spin h-16 w-16 text-blue-600"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              ircle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"
              />
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
          </div>
          <h3 class="text-xl font-bold text-gray-900 mb-2">Procesando archivo...</h3>
          <p class="text-gray-600">Por favor, espera un momento mientras procesamos los datos.</p>
        </div>

        <!-- ==================== ESTADO: ÉXITO ==================== -->
        <div v-else-if="uploadState === 'success'" class="p-8 text-center">
          <div class="flex justify-center mb-4">
            <div class="rounded-full bg-green-100 p-3">
              <svg class="h-16 w-16 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
          </div>
          <h3 class="text-2xl font-bold text-green-600 mb-2">¡Carga Exitosa!</h3>
          <p class="text-gray-700">
            La lista de alumnos ha sido actualizada correctamente en el sistema.
          </p>
          <button
            @click="closeModal"
            class="mt-6 w-full bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-medium shadow-md hover:shadow-lg transition-all duration-200"
          >
            Finalizar
          </button>
        </div>

        <!-- ==================== ESTADO: ERROR ==================== -->
        <div v-else-if="uploadState === 'error'" class="p-8 text-center">
          <div class="flex justify-center mb-4">
            <div class="rounded-full bg-red-100 p-3">
              <svg class="h-16 w-16 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
          </div>
          <h3 class="text-2xl font-bold text-red-600 mb-3">Error en la Carga</h3>
          <div class="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg mb-4">
            <p class="text-sm text-red-800">{{ errorMessage }}</p>
          </div>
          <button
            @click="uploadState = 'waiting'"
            class="w-full bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium shadow-md hover:shadow-lg transition-all duration-200"
          >
            Reintentar
          </button>
        </div>

        <!-- ==================== ESTADO: ESPERANDO ==================== -->
        <div v-else class="p-8">
          <!-- Botón cerrar -->
          <button
            @click="closeModal"
            class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors duration-200"
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

          <!-- Header -->
          <div class="text-center mb-6">
            <div class="flex justify-center mb-3">
              <div class="rounded-full bg-blue-100 p-3">
                <svg
                  class="h-8 w-8 text-blue-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                  />
                </svg>
              </div>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-2">Cargar Lista de Alumnos</h3>
            <p class="text-gray-600 text-sm">
              Selecciona o arrastra un archivo Excel con la información de los estudiantes
            </p>
          </div>

          <!-- Dropzone -->
          <label
            :class="dropzoneClasses"
            @dragover.prevent="isDragOver = true"
            @dragleave.prevent="isDragOver = false"
            @drop.prevent="handleDrop"
          >
            <div class="flex flex-col items-center justify-center pt-5 pb-6">
              <svg
                class="w-12 h-12 mb-3"
                :class="isDragOver ? 'text-blue-600' : 'text-gray-400'"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>

              <p v-if="!fileName" class="mb-2 text-sm text-gray-600">
                <span class="font-semibold text-blue-600">Haz clic para seleccionar</span>
                o arrastra y suelta
              </p>
              <p v-else class="mb-2 text-sm text-blue-700 font-semibold flex items-center gap-2">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clip-rule="evenodd"
                  />
                </svg>
                {{ fileName }}
              </p>
              <p class="text-xs text-gray-500">Solo archivos Excel (.xlsx, .xls)</p>
            </div>
            <input
              ref="fileInput"
              type="file"
              class="hidden"
              @change="handleFileChange"
              accept=".xlsx, .xls"
            />
          </label>

          <!-- Mensaje de error de archivo -->
          <transition
            enter-active-class="transition ease-out duration-200"
            enter-from-class="opacity-0 translate-y-1"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition ease-in duration-150"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
          >
            <div v-if="fileError" class="mt-4">
              <div class="bg-red-50 border-l-4 border-red-500 p-3 rounded-lg">
                <div class="flex items-center">
                  <svg class="w-5 h-5 text-red-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                      clip-rule="evenodd"
                    />
                  </svg>
                  <p class="text-red-800 text-sm font-medium">{{ fileError }}</p>
                </div>
              </div>
            </div>
          </transition>

          <!-- Botón de carga -->
          <div class="mt-6">
            <button
              @click="uploadFile"
              :disabled="!selectedFile"
              class="w-full bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-medium shadow-md hover:shadow-lg disabled:bg-gray-300 disabled:cursor-not-allowed disabled:shadow-none transition-all duration-200"
            >
              <span v-if="selectedFile">Cargar y Actualizar Datos</span>
              <span v-else>Selecciona un archivo para continuar</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { alumnosAPI } from '@/api/alumnos'
import { ref, computed } from 'vue'

// Props y Emits
defineProps({
  show: Boolean,
})
const emit = defineEmits(['close', 'upload-success'])

// Estados del componente
const uploadState = ref('waiting') // 'waiting', 'uploading', 'success', 'error'
const selectedFile = ref(null)
const isDragOver = ref(false)
const errorMessage = ref('')
const fileError = ref(null)

// Computed para mostrar el nombre del archivo
const fileName = computed(() => selectedFile.value?.name || '')

// Clases dinámicas para el área de drop
const dropzoneClasses = computed(() => [
  'flex',
  'flex-col',
  'items-center',
  'justify-center',
  'w-full',
  'h-48',
  'border-2',
  'border-dashed',
  'rounded-lg',
  'cursor-pointer',
  'transition-all',
  'duration-200',
  isDragOver.value
    ? 'border-blue-500 bg-blue-50 scale-[1.02]'
    : 'border-gray-300 bg-gray-50 hover:bg-gray-100 hover:border-gray-400',
])

function handleDrop(event) {
  handleFileChange(event)
  isDragOver.value = false
}

// Manejador cuando se selecciona un archivo (por clic o drop)
function handleFileChange(event) {
  const files = event.target.files || event.dataTransfer.files
  if (files.length > 0) {
    const file = files[0]
    if (
      file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
      file.type === 'application/vnd.ms-excel'
    ) {
      // Si el archivo es VÁLIDO
      selectedFile.value = file
      fileError.value = null
      uploadState.value = 'waiting'
    } else {
      // Si el archivo es INVÁLIDO
      selectedFile.value = null
      fileError.value = 'Tipo de archivo no válido. Por favor, selecciona un Excel (.xlsx, .xls).'
    }
  }
}

// Lógica de subida del archivo
async function uploadFile() {
  if (!selectedFile.value) return

  uploadState.value = 'uploading'
  errorMessage.value = ''
  try {
    await alumnosAPI.uploadExcel(selectedFile.value)
    uploadState.value = 'success'
    emit('upload-success')
  } catch (error) {
    console.error('Error en la carga:', error)
    errorMessage.value = error.response?.data?.message || 'Ocurrió un error al procesar el archivo.'
    uploadState.value = 'error'
  }
}

// Resetea el estado y cierra el modal
function closeModal() {
  selectedFile.value = null
  uploadState.value = 'waiting'
  isDragOver.value = false
  fileError.value = null
  emit('close')
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
