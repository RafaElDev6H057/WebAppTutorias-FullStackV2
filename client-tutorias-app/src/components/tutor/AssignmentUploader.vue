<script setup>
import { tutoriasAPI } from '@/api/tutorias'
import { ref, computed } from 'vue'

// --- Props y Emits ---
defineProps({
  show: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close', 'success'])

// --- Estado Reactivo ---
const selectedFiles = ref([])
const processingLog = ref([])
const isProcessing = ref(false)
const totalFilesToProcess = ref(0)
const filesProcessed = ref(0)
const fileInputRef = ref(null)

// --- Computadas ---
const canProcess = computed(() => selectedFiles.value.length > 0 && !isProcessing.value)
const canReset = computed(() => selectedFiles.value.length > 0 && !isProcessing.value)
const progressPercentage = computed(() => {
  if (totalFilesToProcess.value === 0) return 0
  return Math.round((filesProcessed.value / totalFilesToProcess.value) * 100)
})

const hasResults = computed(() => processingLog.value.length > 0)

// --- Manejadores de Eventos ---
const handleFileChange = (event) => {
  selectedFiles.value = Array.from(event.target.files)
  processingLog.value = []
  filesProcessed.value = 0
  totalFilesToProcess.value = selectedFiles.value.length
}

// --- Función de reseteo ---
const resetForm = () => {
  selectedFiles.value = []
  processingLog.value = []
  filesProcessed.value = 0
  totalFilesToProcess.value = 0
  if (fileInputRef.value) {
    fileInputRef.value.value = ''
  }
}

// --- Función para cerrar el modal ---
const closeModal = () => {
  if (!isProcessing.value) {
    resetForm()
    emit('close')
  }
}

// --- Lógica Principal: Procesar Archivos ---
const processFiles = async () => {
  if (!canProcess.value) return

  isProcessing.value = true
  processingLog.value = [`🏁 Iniciando procesamiento de ${totalFilesToProcess.value} archivos...`]
  filesProcessed.value = 0

  for (const file of selectedFiles.value) {
    processingLog.value.push(`⏳ Procesando ${file.name}...`)

    try {
      const response = await tutoriasAPI.uploadAssignment(file)

      processingLog.value.push(`✅ ${file.name}: Procesado correctamente`)
      processingLog.value.push(
        `   → Asignaciones creadas: ${response.data.nuevas_tutorias_creadas || 0}`,
      )
      processingLog.value.push(
        `   → Alumnos no encontrados: ${response.data.alumnos_no_encontrados || 0}`,
      )
      processingLog.value.push(
        `   → Filas ignoradas/duplicadas: ${response.data.filas_csv_ignoradas || 0}`,
      )

      if (
        response.data.detalles_saltados_o_errores &&
        response.data.detalles_saltados_o_errores.length > 0
      ) {
        processingLog.value.push(`   ⚠️ Detalles:`)
        response.data.detalles_saltados_o_errores.forEach((detail) => {
          processingLog.value.push(`      • ${detail}`)
        })
      }
    } catch (error) {
      console.error(`Error procesando ${file.name}:`, error)

      const errorDetail = error.response?.data?.detail || error.message || 'Error desconocido.'
      processingLog.value.push(`❌ ${file.name}: Error - ${errorDetail}`)
    } finally {
      filesProcessed.value++
    }

    processingLog.value.push(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
  }

  processingLog.value.push(
    `🏁 Procesamiento completado. ${filesProcessed.value}/${totalFilesToProcess.value} archivos procesados.`,
  )
  isProcessing.value = false

  // Emitir evento de éxito para que el padre pueda recargar datos si es necesario
  emit('success')
}
</script>

<template>
  <!-- Modal Overlay -->
  <Transition name="modal">
    <div
      v-if="show"
      class="fixed inset-0 z-50 overflow-y-auto"
      aria-labelledby="modal-title"
      role="dialog"
      aria-modal="true"
    >
      <!-- Background overlay -->
      <div
        class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0"
      >
        <div
          class="fixed inset-0 bg-gray-900 bg-opacity-75 transition-opacity"
          aria-hidden="true"
          @click="closeModal"
        ></div>

        <!-- Center modal -->
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true"
          >&#8203;</span
        >

        <!-- Modal panel -->
        <div
          class="inline-block align-bottom bg-white rounded-xl text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full"
        >
          <!-- Header -->
          <div
            class="bg-gradient-to-r from-purple-600 to-purple-700 px-6 py-5 flex items-center justify-between"
          >
            <div>
              <h2 id="modal-title" class="text-2xl font-semibold text-white">
                Carga de Asignaciones de Tutorías
              </h2>
              <p class="text-blue-100 text-sm mt-1">Procesamiento por lotes de archivos CSV</p>
            </div>
            <button
              @click="closeModal"
              :disabled="isProcessing"
              class="text-white hover:text-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg
                class="h-6 w-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                ></path>
              </svg>
            </button>
          </div>

          <div class="p-6 max-h-[calc(100vh-200px)] overflow-y-auto">
            <!-- Input de Archivos -->
            <div class="mb-6">
              <label for="csv-upload" class="block text-sm font-medium text-gray-700 mb-2">
                Archivos CSV
              </label>
              <div class="relative">
                <input
                  id="csv-upload"
                  ref="fileInputRef"
                  type="file"
                  multiple
                  accept=".csv"
                  @change="handleFileChange"
                  class="block w-full text-sm text-gray-600 file:mr-4 file:py-2.5 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-purple-700 hover:file:bg-blue-100 file:transition-colors file:cursor-pointer cursor-pointer border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  :disabled="isProcessing"
                />
              </div>
              <p class="mt-2 text-xs text-gray-500 flex items-center">
                <svg
                  class="w-4 h-4 mr-1"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  ></path>
                </svg>
                Solo archivos .csv — Puede seleccionar múltiples archivos
              </p>
            </div>

            <!-- Lista de Archivos Seleccionados -->
            <div v-if="selectedFiles.length > 0" class="mb-6">
              <div class="flex items-center justify-between mb-3">
                <h3 class="text-sm font-medium text-gray-700">
                  Archivos seleccionados ({{ selectedFiles.length }})
                </h3>
              </div>
              <div
                class="bg-gray-50 border border-gray-200 rounded-lg p-4 max-h-40 overflow-y-auto"
              >
                <ul class="space-y-2">
                  <li
                    v-for="file in selectedFiles"
                    :key="file.name"
                    class="flex items-center text-sm text-gray-700"
                  >
                    <svg
                      class="w-5 h-5 mr-2 text-purple-500 flex-shrink-0"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                      ></path>
                    </svg>
                    <span class="truncate">{{ file.name }}</span>
                    <span class="ml-auto text-xs text-gray-500 flex-shrink-0">
                      {{ (file.size / 1024).toFixed(1) }} KB
                    </span>
                  </li>
                </ul>
              </div>
            </div>

            <!-- Botones de Acción -->
            <div class="flex gap-3 mb-6">
              <button
                @click="processFiles"
                :disabled="!canProcess"
                class="flex-1 inline-flex justify-center items-center py-2.5 px-4 border border-transparent shadow-sm text-sm font-medium rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200"
                :class="{
                  'bg-purple-600 hover:bg-purple-700 hover:shadow-md': canProcess,
                  'bg-gray-300 cursor-not-allowed': !canProcess,
                }"
              >
                <svg
                  v-if="isProcessing"
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
                  ></circle>
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                <svg
                  v-else
                  class="-ml-1 mr-2 h-5 w-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                  ></path>
                </svg>
                {{ isProcessing ? 'Procesando...' : `Procesar Archivos` }}
              </button>

              <button
                v-if="canReset || hasResults"
                @click="resetForm"
                :disabled="isProcessing"
                class="inline-flex justify-center items-center py-2.5 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg
                  class="-ml-1 mr-2 h-5 w-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  ></path>
                </svg>
                Resetear
              </button>
            </div>

            <!-- Progreso y Logs -->
            <div v-if="isProcessing || hasResults" class="mt-6">
              <!-- Barra de Progreso -->
              <div v-if="isProcessing" class="mb-6">
                <div class="flex justify-between items-center mb-2">
                  <span class="text-sm font-medium text-gray-700">Progreso</span>
                  <span class="text-sm font-medium text-gray-700">{{ progressPercentage }}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                  <div
                    class="bg-gradient-to-r from-purple-500 to-purple-600 h-3 rounded-full transition-all duration-300 ease-out shadow-sm"
                    :style="{ width: progressPercentage + '%' }"
                  ></div>
                </div>
                <p class="text-xs text-center text-gray-600 mt-2">
                  {{ filesProcessed }} de {{ totalFilesToProcess }} archivos procesados
                </p>
              </div>

              <!-- Área de Logs -->
              <div>
                <h3 class="text-sm font-medium text-gray-700 mb-3 flex items-center">
                  <svg
                    class="w-5 h-5 mr-2 text-gray-500"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    ></path>
                  </svg>
                  Registro de procesamiento
                </h3>
                <div
                  class="bg-gray-900 rounded-lg p-4 text-xs font-mono max-h-80 overflow-y-auto shadow-inner border border-gray-700"
                >
                  <div
                    v-for="(log, index) in processingLog"
                    :key="index"
                    :class="{
                      'text-green-400': log.startsWith('✅') || log.startsWith('🏁'),
                      'text-red-400': log.startsWith('❌'),
                      'text-yellow-300': log.startsWith('⚠️'),
                      'text-blue-400': log.startsWith('⏳'),
                      'text-gray-500': log.startsWith('━'),
                      'text-gray-300':
                        !log.startsWith('✅') &&
                        !log.startsWith('❌') &&
                        !log.startsWith('⚠️') &&
                        !log.startsWith('⏳') &&
                        !log.startsWith('🏁') &&
                        !log.startsWith('━'),
                    }"
                    class="whitespace-pre-wrap break-words leading-relaxed py-0.5"
                  >
                    {{ log }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Mensaje cuando no hay archivos seleccionados -->
            <div
              v-if="!selectedFiles.length && !hasResults"
              class="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300"
            >
              <svg
                class="mx-auto h-12 w-12 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                ></path>
              </svg>
              <p class="mt-2 text-sm text-gray-600">No hay archivos seleccionados</p>
              <p class="text-xs text-gray-500 mt-1">
                Seleccione uno o más archivos CSV para comenzar
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
/* Scroll personalizado para el área de logs */
/* .overflow-y-auto::-webkit-scrollbar {
  width: 8px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
} */

/* Transiciones del modal */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .inline-block,
.modal-leave-active .inline-block {
  transition: all 0.3s ease;
}

.modal-enter-from .inline-block,
.modal-leave-to .inline-block {
  opacity: 0;
  transform: scale(0.95) translateY(-20px);
}
</style>
