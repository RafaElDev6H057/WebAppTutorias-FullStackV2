<template>
  <div class="space-y-6">
    <!-- ==================== GESTIÓN DE PLANTILLA - REPORTE INTEGRAL ==================== -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div class="mb-6">
        <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          Gestión de Plantilla - Reporte Integral
        </h2>
        <p class="text-sm text-gray-600 mt-1">
          Administra la plantilla PDF utilizada para el Reporte Integral de Tutorías
        </p>
      </div>

      <!-- Mensajes de éxito/error -->
      <Transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="opacity-0 translate-y-1"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="successMessage"
          class="mb-4 p-4 bg-green-50 border-l-4 border-green-500 rounded-lg shadow-sm"
        >
          <div class="flex items-center">
            <svg class="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clip-rule="evenodd"
              />
            </svg>
            <p class="text-sm text-green-800 font-medium">{{ successMessage }}</p>
          </div>
        </div>
      </Transition>

      <Transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="opacity-0 translate-y-1"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="errorMessage"
          class="mb-4 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg shadow-sm"
        >
          <div class="flex items-center">
            <svg class="w-5 h-5 text-red-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clip-rule="evenodd"
              />
            </svg>
            <p class="text-sm text-red-800 font-medium">{{ errorMessage }}</p>
          </div>
        </div>
      </Transition>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- ==================== SUBIR NUEVA PLANTILLA ==================== -->
        <div class="p-6 bg-blue-50 rounded-lg border-2 border-blue-200 shadow-sm">
          <div class="flex items-center gap-3 mb-4">
            <div class="p-3 bg-blue-500 rounded-lg shadow-md">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900">Subir Nueva Plantilla</h3>
              <p class="text-sm text-gray-600">Reemplaza la plantilla actual</p>
            </div>
          </div>

          <!-- Área de carga de archivo -->
          <div class="mb-4">
            <label
              for="file-upload"
              class="flex flex-col items-center justify-center w-full h-40 px-4 transition bg-white border-2 border-blue-300 border-dashed rounded-lg appearance-none cursor-pointer hover:border-blue-500 hover:bg-blue-50 focus:outline-none"
              :class="isUploading ? 'opacity-50 cursor-not-allowed' : ''"
            >
              <div class="flex flex-col items-center justify-center pt-5 pb-6">
                <svg
                  class="w-12 h-12 mb-3 text-blue-500"
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
                <p class="mb-2 text-sm text-gray-700 font-medium">
                  <span class="font-bold text-blue-600">Click para seleccionar</span> o arrastra el
                  archivo
                </p>
                <p class="text-xs text-gray-500">Solo archivos PDF (MAX. 10MB)</p>
              </div>
              <input
                id="file-upload"
                type="file"
                accept=".pdf"
                @change="handleFileChange"
                :disabled="isUploading"
                class="hidden"
              />
            </label>
          </div>

          <!-- Archivo seleccionado -->
          <Transition
            enter-active-class="transition ease-out duration-200"
            enter-from-class="opacity-0 scale-95"
            enter-to-class="opacity-100 scale-100"
            leave-active-class="transition ease-in duration-150"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
          >
            <div
              v-if="selectedFile"
              class="mb-4 p-4 bg-white border-2 border-blue-300 rounded-lg flex items-center justify-between shadow-sm"
            >
              <div class="flex items-center gap-3">
                <div class="p-2 bg-blue-100 rounded-lg">
                  <svg
                    class="w-6 h-6 text-blue-600"
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
                </div>
                <div>
                  <p class="text-sm font-bold text-gray-900">{{ selectedFile.name }}</p>
                  <p class="text-xs text-gray-600 font-medium">
                    {{ formatFileSize(selectedFile.size) }}
                  </p>
                </div>
              </div>
              <button
                @click="clearFile"
                :disabled="isUploading"
                class="text-red-600 hover:text-red-800 disabled:opacity-50 p-2 hover:bg-red-50 rounded-lg transition-colors"
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

          <!-- Botón subir -->
          <button
            @click="uploadTemplate"
            :disabled="!selectedFile || isUploading"
            class="w-full px-4 py-3 rounded-lg font-bold text-white focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:cursor-not-allowed transition-all inline-flex justify-center items-center shadow-md hover:shadow-lg"
            :class="
              !selectedFile || isUploading
                ? 'bg-gray-400'
                : 'bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 focus:ring-blue-500'
            "
          >
            <svg
              v-if="isUploading"
              class="animate-spin -ml-1 mr-2 h-5 w-5 text-white"
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
              />
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            <svg v-else class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
            {{ isUploading ? 'Subiendo Plantilla...' : 'Subir Plantilla' }}
          </button>
        </div>

        <!-- ==================== RESETEAR PLANTILLA ==================== -->
        <div class="p-6 bg-orange-50 rounded-lg border-2 border-orange-200 shadow-sm">
          <div class="flex items-center gap-3 mb-4">
            <div class="p-3 bg-orange-500 rounded-lg shadow-md">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900">Restaurar Plantilla Original</h3>
              <p class="text-sm text-gray-600">Volver a la plantilla por defecto</p>
            </div>
          </div>

          <div class="mb-4 p-4 bg-orange-100 rounded-lg border-2 border-orange-300">
            <div class="flex items-start gap-3">
              <svg
                class="w-6 h-6 text-orange-600 flex-shrink-0 mt-0.5"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fill-rule="evenodd"
                  d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                  clip-rule="evenodd"
                />
              </svg>
              <div class="flex-1">
                <p class="text-sm text-orange-900 font-bold mb-1">Advertencia Importante</p>
                <p class="text-sm text-orange-800 leading-relaxed">
                  Esta acción reemplazará la plantilla actual con la plantilla original del sistema.
                  Esta operación no se puede deshacer.
                </p>
              </div>
            </div>
          </div>

          <div class="space-y-3 mb-6">
            <div class="flex items-start gap-2 bg-white p-3 rounded-lg border border-orange-200">
              <svg
                class="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5"
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
              <p class="text-sm text-gray-700 font-medium">Se restaurará el formato original</p>
            </div>
            <div class="flex items-start gap-2 bg-white p-3 rounded-lg border border-orange-200">
              <svg
                class="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5"
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
              <p class="text-sm text-gray-700 font-medium">Todos los campos estarán disponibles</p>
            </div>
          </div>

          <button
            @click="confirmReset"
            :disabled="isResetting"
            class="w-full px-4 py-3 rounded-lg font-bold text-white focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:cursor-not-allowed transition-all inline-flex justify-center items-center shadow-md hover:shadow-lg"
            :class="
              isResetting
                ? 'bg-gray-400'
                : 'bg-gradient-to-r from-orange-600 to-orange-700 hover:from-orange-700 hover:to-orange-800 focus:ring-orange-500'
            "
          >
            <svg
              v-if="isResetting"
              class="animate-spin -ml-1 mr-2 h-5 w-5 text-white"
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
              />
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            <svg v-else class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              />
            </svg>
            {{ isResetting ? 'Restaurando...' : 'Restaurar Plantilla Original' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { configuracionesAPI } from '@/api/configuraciones'

// ==================== STATE ====================
const selectedFile = ref(null)
const isUploading = ref(false)
const isResetting = ref(false)
const successMessage = ref(null)
const errorMessage = ref(null)

// ==================== FILE HANDLERS ====================
const handleFileChange = (event) => {
  const file = event.target.files[0]

  if (!file) return

  // Validar que sea PDF
  if (file.type !== 'application/pdf') {
    errorMessage.value = 'Solo se permiten archivos PDF'
    event.target.value = ''
    return
  }

  // Validar tamaño (10MB max)
  const maxSize = 10 * 1024 * 1024 // 10MB
  if (file.size > maxSize) {
    errorMessage.value = 'El archivo no debe superar los 10MB'
    event.target.value = ''
    return
  }

  selectedFile.value = file
  errorMessage.value = null
}

const clearFile = () => {
  selectedFile.value = null
  const fileInput = document.getElementById('file-upload')
  if (fileInput) fileInput.value = ''
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
}

// ==================== API CALLS ====================
const uploadTemplate = async () => {
  if (!selectedFile.value) return

  isUploading.value = true
  errorMessage.value = null
  successMessage.value = null

  try {
    const response = await configuracionesAPI.updatePlantillaIntegral(selectedFile.value)

    if (response.status === 200) {
      successMessage.value = '✅ Plantilla actualizada exitosamente'
      clearFile()

      setTimeout(() => {
        successMessage.value = null
      }, 5000)
    }
  } catch (error) {
    console.error('❌ Error al subir plantilla:', error)

    if (error.response?.status === 400) {
      errorMessage.value = 'Archivo inválido. Verifica que sea un PDF válido.'
    } else if (error.response?.status === 413) {
      errorMessage.value = 'El archivo es demasiado grande.'
    } else {
      errorMessage.value = 'Error al subir la plantilla. Intenta de nuevo.'
    }
  } finally {
    isUploading.value = false
  }
}

const confirmReset = () => {
  if (
    confirm(
      '¿Estás seguro de que deseas restaurar la plantilla original? Esta acción no se puede deshacer.',
    )
  ) {
    resetTemplate()
  }
}

const resetTemplate = async () => {
  isResetting.value = true
  errorMessage.value = null
  successMessage.value = null

  try {
    const response = await configuracionesAPI.resetPlantillaIntegral()

    if (response.status === 200) {
      successMessage.value = '✅ Plantilla restaurada exitosamente al formato original'

      setTimeout(() => {
        successMessage.value = null
      }, 5000)
    }
  } catch (error) {
    console.error('❌ Error al resetear plantilla:', error)
    errorMessage.value = 'Error al restaurar la plantilla. Intenta de nuevo.'
  } finally {
    isResetting.value = false
  }
}
</script>
