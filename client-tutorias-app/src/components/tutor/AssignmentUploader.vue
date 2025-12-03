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
          class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full"
        >
          <!-- Header -->
          <div class="bg-[#0A3B76] px-6 py-5 border-b-2 border-[#083060]">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="rounded-full bg-white/10 p-2">
                  <svg
                    class="h-6 w-6 text-white"
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
                  <h2 id="modal-title" class="text-xl font-bold text-white">
                    Carga de Asignaciones de Tutorías
                  </h2>
                  <p class="text-gray-200 text-sm mt-0.5">
                    Procesamiento por lotes de archivos CSV
                  </p>
                </div>
              </div>
              <button
                @click="closeModal"
                :disabled="isProcessing"
                class="text-white hover:text-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
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
          </div>

          <div class="p-6 max-h-[calc(100vh-200px)] overflow-y-auto">
            <!-- Input de Archivos -->
            <div class="mb-6">
              <label for="csv-upload" class="block text-sm font-medium text-gray-700 mb-2">
                Seleccionar Archivos CSV
              </label>
              <div class="relative">
                <input
                  id="csv-upload"
                  ref="fileInputRef"
                  type="file"
                  multiple
                  accept=".csv"
                  @change="handleFileChange"
                  class="block w-full text-sm text-gray-600 file:mr-4 file:py-2.5 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 file:transition-colors file:cursor-pointer cursor-pointer border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#0A3B76] focus:border-[#0A3B76]"
                  :disabled="isProcessing"
                />
              </div>
              <div class="mt-2 flex items-start text-xs text-gray-500">
                <svg
                  class="w-4 h-4 mr-1.5 mt-0.5 flex-shrink-0"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fill-rule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                    clip-rule="evenodd"
                  />
                </svg>
                <span>Solo archivos .csv — Puede seleccionar múltiples archivos</span>
              </div>
            </div>

            <!-- Lista de Archivos Seleccionados -->
            <div v-if="selectedFiles.length > 0" class="mb-6">
              <div class="flex items-center justify-between mb-3">
                <h3 class="text-sm font-medium text-gray-700 flex items-center">
                  <svg class="w-5 h-5 mr-2 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                      clip-rule="evenodd"
                    />
                  </svg>
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
                    class="flex items-center text-sm text-gray-700 bg-white px-3 py-2 rounded-md shadow-sm"
                  >
                    <svg
                      class="w-5 h-5 mr-2 text-blue-600 flex-shrink-0"
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
                    <span class="truncate flex-1">{{ file.name }}</span>
                    <span class="ml-2 text-xs text-gray-500 flex-shrink-0 font-medium">
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
                class="flex-1 inline-flex justify-center items-center py-3 px-4 border border-transparent shadow-sm text-sm font-medium rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-all duration-200"
                :class="{
                  'bg-green-600 hover:bg-green-700 hover:shadow-md': canProcess,
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
                  ircle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                  stroke-width="4" />
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                <svg
                  v-else
                  class="-ml-1 mr-2 h-5 w-5"
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
                {{
                  isProcessing
                    ? 'Procesando...'
                    : `Procesar ${selectedFiles.length} Archivo${selectedFiles.length !== 1 ? 's' : ''}`
                }}
              </button>

              <button
                v-if="canReset || hasResults"
                @click="resetForm"
                :disabled="isProcessing"
                class="inline-flex justify-center items-center py-3 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg
                  class="-ml-1 mr-2 h-5 w-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
                Resetear
              </button>
            </div>

            <!-- Progreso y Logs -->
            <div v-if="isProcessing || hasResults" class="mt-6">
              <!-- Barra de Progreso -->
              <div v-if="isProcessing" class="mb-6">
                <div class="flex justify-between items-center mb-2">
                  <span class="text-sm font-medium text-gray-700">Progreso de procesamiento</span>
                  <span class="text-sm font-bold text-blue-600">{{ progressPercentage }}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-3 overflow-hidden shadow-inner">
                  <div
                    class="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full transition-all duration-300 ease-out"
                    :style="{ width: progressPercentage + '%' }"
                  ></div>
                </div>
                <p class="text-xs text-center text-gray-600 mt-2 font-medium">
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
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
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
                      'text-green-400 font-semibold': log.includes('✅') || log.includes('🏁'),
                      'text-red-400 font-semibold': log.includes('❌'),
                      'text-yellow-300': log.includes('⚠️'),
                      'text-blue-400': log.includes('⏳'),
                      'text-gray-600': log.includes('━'),
                      'text-gray-300':
                        !log.includes('✅') &&
                        !log.includes('❌') &&
                        !log.includes('⚠️') &&
                        !log.includes('⏳') &&
                        !log.includes('🏁') &&
                        !log.includes('━'),
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
                class="mx-auto h-16 w-16 text-gray-300"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                />
              </svg>
              <p class="mt-3 text-sm font-medium text-gray-900">No hay archivos seleccionados</p>
              <p class="text-xs text-gray-500 mt-1">
                Seleccione uno o más archivos CSV para comenzar el procesamiento
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

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

<style scoped>
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
