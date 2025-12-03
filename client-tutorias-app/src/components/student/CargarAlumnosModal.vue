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
  'transition-colors',
  isDragOver.value
    ? 'border-indigo-500 bg-indigo-50'
    : 'border-gray-300 bg-gray-50 hover:bg-gray-100',
])

function handleDrop(event) {
  handleFileChange(event)
  isDragOver.value = false
}

// Función para abrir el selector de archivos al hacer clic
// const fileInput = ref(null)
// function triggerFileInput() {
//   fileInput.value.click()
// }

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
      fileError.value = null // <-- Limpiamos cualquier error anterior
      uploadState.value = 'waiting'
    } else {
      // Si el archivo es INVÁLIDO
      selectedFile.value = null // <-- Nos aseguramos de no guardar el archivo incorrecto
      fileError.value = 'Tipo de archivo no válido. Por favor, selecciona un Excel (.xlsx, .xls).' // <-- Establecemos el mensaje de error
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
    emit('upload-success') // Notificamos al padre del éxito
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
  fileError.value = null // <-- AÑADE ESTA LÍNEA
  emit('close')
}
</script>

<template>
  <transition name="fade">
    <div
      v-if="show"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
    >
      <div class="bg-white rounded-xl shadow-2xl w-full max-w-lg mx-auto p-8 relative">
        <div v-if="uploadState === 'uploading'" class="text-center">
          <h3 class="text-xl font-semibold mt-4">Procesando archivo...</h3>
          <p class="text-gray-600">Por favor, espera un momento.</p>
        </div>

        <div v-else-if="uploadState === 'success'" class="text-center">
          <h3 class="text-2xl font-bold text-green-600 mt-4">¡Éxito!</h3>
          <p class="text-gray-700 mt-2">La lista de alumnos ha sido actualizada correctamente.</p>
          <button
            @click="closeModal"
            class="mt-6 bg-green-600 text-white px-6 py-2 rounded-md hover:bg-green-700"
          >
            Finalizar
          </button>
        </div>

        <div v-else-if="uploadState === 'error'" class="text-center">
          [Image of a red error icon]

          <h3 class="text-2xl font-bold text-red-600 mt-4">Error en la carga</h3>
          <p class="text-gray-700 mt-2 bg-red-50 p-3 rounded-md">{{ errorMessage }}</p>
          <button
            @click="uploadState = 'waiting'"
            class="mt-6 bg-indigo-600 text-white px-6 py-2 rounded-md hover:bg-indigo-700"
          >
            Reintentar
          </button>
        </div>

        <div v-else>
          <button
            @click="closeModal"
            class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 text-2xl"
          >
            &times;
          </button>
          <h3 class="text-2xl font-semibold mb-2 text-center">Cargar nueva lista de alumnos</h3>
          <p class="text-gray-600 mb-6 text-center">
            Arrastra o selecciona un archivo Excel (.xlsx, .xls).
          </p>

          <label
            :class="dropzoneClasses"
            @dragover.prevent="isDragOver = true"
            @dragleave.prevent="isDragOver = false"
            @drop.prevent="handleDrop"
          >
            <div class="flex flex-col items-center justify-center pt-5 pb-6">
              <p v-if="!fileName" class="mb-2 text-sm text-gray-500">
                <span class="font-semibold">Haz clic para subir</span> o arrastra y suelta
              </p>
              <p v-else class="mb-2 text-sm text-indigo-700 font-semibold">{{ fileName }}</p>
              <p class="text-xs text-gray-500">Solo archivos Excel</p>
            </div>
            <input
              ref="fileInput"
              type="file"
              class="hidden"
              @change="handleFileChange"
              accept=".xlsx, .xls"
            />
          </label>
          <div v-if="fileError" class="mt-3 text-center">
            <p class="text-red-600 text-sm font-medium">{{ fileError }}</p>
          </div>

          <div class="mt-6 flex justify-end">
            <button
              @click="uploadFile"
              :disabled="!selectedFile"
              class="w-full bg-indigo-600 text-white px-6 py-3 rounded-md hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              Cargar y reemplazar datos
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

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
