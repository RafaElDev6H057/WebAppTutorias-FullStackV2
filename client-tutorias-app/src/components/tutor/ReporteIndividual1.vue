<template>
  <div class="bg-white rounded-lg shadow-lg">
    <!-- ==================== VISTA: SUB-PANEL (Lista de Reportes) ==================== -->
    <div v-if="vistaActual === 'lista'">
      <!-- Header -->
      <div class="bg-gradient-to-r from-orange-500 to-orange-600 px-6 py-4 rounded-t-lg">
        <h2 class="text-2xl font-bold text-white">Reporte Individual 1</h2>
        <p class="text-orange-100 text-sm mt-1">Gestiona tus reportes generales</p>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="flex justify-center items-center py-12">
        <svg
          class="animate-spin h-10 w-10 text-orange-500"
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
        <span class="ml-3 text-gray-600">Cargando reportes...</span>
      </div>

      <!-- Mensajes -->
      <div v-if="!isLoading" class="p-6">
        <!-- Success Message -->
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
            class="mb-4 p-3 bg-green-50 border-l-4 border-green-500 rounded-md"
          >
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <svg
                  class="w-5 h-5 text-green-500 mr-2"
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
                <p class="text-sm text-green-800 font-medium">{{ successMessage }}</p>
              </div>
              <button @click="successMessage = null" class="text-green-500 hover:text-green-700">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
        </Transition>

        <!-- Error Message -->
        <Transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="opacity-0 translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <div v-if="errorMessage" class="mb-4 p-3 bg-red-50 border-l-4 border-red-500 rounded-md">
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <svg
                  class="w-5 h-5 text-red-500 mr-2"
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
                <p class="text-sm text-red-800 font-medium">{{ errorMessage }}</p>
              </div>
              <button @click="errorMessage = null" class="text-red-500 hover:text-red-700">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
        </Transition>

        <!-- Botón Crear Nuevo Reporte -->
        <div class="mb-6">
          <button
            @click="crearNuevoReporte"
            class="w-full sm:w-auto px-6 py-3 bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white rounded-lg font-medium transition-all flex items-center justify-center gap-2 shadow-md hover:shadow-lg"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 4v16m8-8H4"
              />
            </svg>
            Crear Nuevo Reporte
          </button>
        </div>

        <!-- Lista de Reportes -->
        <div v-if="reportes.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div
            v-for="reporte in reportes"
            :key="reporte.id"
            class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow bg-gradient-to-br from-white to-orange-50"
          >
            <div class="flex items-start justify-between mb-3">
              <div class="flex-1">
                <h3 class="font-bold text-gray-900 text-lg mb-1">
                  {{ reporte.nombre_proyecto }}
                </h3>
                <p class="text-sm text-gray-600">Periodo: {{ reporte.periodo }}</p>
              </div>
              <div
                class="flex-shrink-0 ml-3 px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-xs font-semibold"
              >
                {{ reporte.porcentaje_avance }}%
              </div>
            </div>

            <div class="space-y-2 mb-4">
              <div class="flex items-center text-xs text-gray-500">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
                Creado: {{ formatDate(reporte.created_at) }}
              </div>
              <div
                v-if="reporte.updated_at !== reporte.created_at"
                class="flex items-center text-xs text-gray-500"
              >
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
                Actualizado: {{ formatDate(reporte.updated_at) }}
              </div>
            </div>

            <!-- Acciones -->
            <div class="flex gap-2">
              <button
                @click="descargarPDF(reporte)"
                :disabled="isDownloadingPDF[reporte.id]"
                class="flex-1 px-3 py-2 bg-green-500 hover:bg-green-600 text-white rounded-md text-sm font-medium transition-colors flex items-center justify-center gap-1 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg
                  v-if="isDownloadingPDF[reporte.id]"
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
                {{ isDownloadingPDF[reporte.id] ? 'Descargando...' : 'PDF' }}
              </button>
              <button
                @click="editarReporte(reporte)"
                class="flex-1 px-3 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md text-sm font-medium transition-colors flex items-center justify-center gap-1"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                  />
                </svg>
                Editar
              </button>
              <button
                @click="confirmarEliminar(reporte)"
                class="flex-1 px-3 py-2 bg-red-500 hover:bg-red-600 text-white rounded-md text-sm font-medium transition-colors flex items-center justify-center gap-1"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                  />
                </svg>
                Eliminar
              </button>
            </div>
          </div>
        </div>

        <!-- Sin Reportes -->
        <div v-else class="text-center py-12">
          <svg
            class="w-20 h-20 text-gray-400 mx-auto mb-4"
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
          <p class="text-gray-600 text-lg mb-2">No tienes reportes aún</p>
          <p class="text-gray-500 text-sm">Crea tu primer reporte para comenzar</p>
        </div>
      </div>
    </div>

    <!-- ==================== VISTA: FORMULARIO (Crear/Editar) ==================== -->
    <div v-else-if="vistaActual === 'formulario'">
      <!-- Header -->
      <div class="bg-gradient-to-r from-orange-500 to-orange-600 px-6 py-4 rounded-t-lg">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-2xl font-bold text-white">
              {{ modoFormulario === 'crear' ? 'Crear Reporte' : 'Editar Reporte' }}
            </h2>
            <p class="text-orange-100 text-sm mt-1">
              {{
                modoFormulario === 'crear'
                  ? 'Completa los campos del nuevo reporte'
                  : 'Actualiza la información del reporte'
              }}
            </p>
          </div>
          <button
            @click="cancelarFormulario"
            class="text-white hover:text-orange-100 transition-colors"
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
      </div>

      <!-- Formulario -->
      <form @submit.prevent="guardarReporte" class="p-6 space-y-4 max-h-[70vh] overflow-y-auto">
        <!-- Nombre del Tutor (readonly) -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"> Nombre del Tutor </label>
          <input
            v-model="formulario.nombre_tutor"
            type="text"
            readonly
            class="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-100 text-gray-600 cursor-not-allowed"
          />
        </div>

        <!-- Periodo -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Periodo <span class="text-red-500">*</span>
          </label>
          <input
            v-model="formulario.periodo"
            type="text"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
            placeholder="Ej: Enero - Junio 2025"
          />
        </div>

        <!-- Nombre del Proyecto -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Nombre del Proyecto <span class="text-red-500">*</span>
          </label>
          <input
            v-model="formulario.nombre_proyecto"
            type="text"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
            placeholder="Nombre del proyecto"
          />
        </div>

        <!-- Porcentaje de Avance -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Porcentaje de Avance (%) <span class="text-red-500">*</span>
          </label>
          <div class="flex items-center gap-3">
            <input
              v-model.number="formulario.porcentaje_avance"
              type="range"
              min="0"
              max="100"
              step="10"
              class="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-orange-500"
            />
            <input
              v-model.number="formulario.porcentaje_avance"
              type="number"
              min="0"
              step="10"
              max="100"
              required
              class="w-20 px-3 py-2 border border-gray-300 rounded-md text-center focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
            />
          </div>
        </div>

        <!-- Objetivo -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Objetivo <span class="text-red-500">*</span>
          </label>
          <textarea
            v-model="formulario.objetivo"
            required
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
            placeholder="Describe el objetivo del proyecto"
          ></textarea>
        </div>

        <!-- Descripción -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Descripción <span class="text-red-500">*</span>
          </label>
          <textarea
            v-model="formulario.descripcion"
            required
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
            placeholder="Descripción del proyecto"
          ></textarea>
        </div>

        <!-- Metas -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Metas <span class="text-red-500">*</span>
          </label>
          <textarea
            v-model="formulario.metas"
            required
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
            placeholder="Metas a alcanzar"
          ></textarea>
        </div>

        <!-- Actividades -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Actividades <span class="text-red-500">*</span>
          </label>
          <textarea
            v-model="formulario.actividades"
            required
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
            placeholder="Actividades realizadas"
          ></textarea>
        </div>

        <!-- Documentos Anexados -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Documentos Anexados <span class="text-red-500">*</span>
          </label>
          <textarea
            v-model="formulario.documentos_anexados"
            required
            rows="2"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
            placeholder="Lista de documentos anexados"
          ></textarea>
        </div>

        <!-- Conclusiones -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Conclusiones <span class="text-red-500">*</span>
          </label>
          <textarea
            v-model="formulario.conclusiones"
            required
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
            placeholder="Conclusiones del proyecto"
          ></textarea>
        </div>

        <!-- Observaciones -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"> Observaciones </label>
          <textarea
            v-model="formulario.observaciones"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
            placeholder="Observaciones adicionales (opcional)"
          ></textarea>
        </div>

        <!-- Botones -->
        <div class="flex gap-3 pt-4 border-t">
          <button
            type="button"
            @click="cancelarFormulario"
            class="flex-1 px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors font-medium"
          >
            Cancelar
          </button>
          <button
            type="submit"
            :disabled="isGuardando"
            class="flex-1 px-4 py-2 bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white rounded-md font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <svg
              v-if="isGuardando"
              class="animate-spin h-5 w-5"
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
            {{
              isGuardando
                ? 'Guardando...'
                : modoFormulario === 'crear'
                  ? 'Crear Reporte'
                  : 'Actualizar Reporte'
            }}
          </button>
        </div>
      </form>
    </div>

    <!-- ==================== MODAL CONFIRMAR ELIMINACIÓN ==================== -->
    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="mostrarModalEliminar"
        class="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center z-50 p-4"
      >
        <div class="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
          <div class="flex items-center gap-3 mb-4">
            <div
              class="flex-shrink-0 w-12 h-12 rounded-full bg-red-100 flex items-center justify-center"
            >
              <svg
                class="w-6 h-6 text-red-600"
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
            <div>
              <h3 class="text-lg font-bold text-gray-900">Eliminar Reporte</h3>
              <p class="text-sm text-gray-600">Esta acción no se puede deshacer</p>
            </div>
          </div>

          <p class="text-sm text-gray-700 mb-6">
            ¿Estás seguro de que deseas eliminar el reporte "<strong>{{
              reporteAEliminar?.nombre_proyecto
            }}</strong
            >"?
          </p>

          <div class="flex gap-3">
            <button
              @click="cancelarEliminar"
              :disabled="isEliminando"
              class="flex-1 px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors font-medium disabled:opacity-50"
            >
              Cancelar
            </button>
            <button
              @click="eliminarReporte"
              :disabled="isEliminando"
              class="flex-1 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              <svg
                v-if="isEliminando"
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
              {{ isEliminando ? 'Eliminando...' : 'Eliminar' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// ==================== PROPS & EMITS ====================
defineEmits(['cerrar'])

// ==================== STATE ====================
const vistaActual = ref('lista') // 'lista' | 'formulario'
const modoFormulario = ref('crear') // 'crear' | 'editar'
const reportes = ref([])
const tutorData = ref(null)
const isLoading = ref(false)
const isGuardando = ref(false)
const isEliminando = ref(false)
const isDownloadingPDF = ref({})
const successMessage = ref(null)
const errorMessage = ref(null)
const mostrarModalEliminar = ref(false)
const reporteAEliminar = ref(null)
const reporteEditando = ref(null)

const formulario = ref({
  nombre_tutor: '',
  periodo: '',
  nombre_proyecto: '',
  porcentaje_avance: 0,
  objetivo: '',
  descripcion: '',
  metas: '',
  actividades: '',
  documentos_anexados: '',
  conclusiones: '',
  observaciones: '',
})

// ==================== API CALLS ====================
const fetchTutorData = async () => {
  try {
    const token = localStorage.getItem('accessToken')
    const response = await axios.get('http://localhost:8000/api/tutores/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    tutorData.value = response.data
    console.log('✅ Datos del tutor cargados:', tutorData.value)
  } catch (error) {
    console.error('❌ Error al cargar datos del tutor:', error)
    errorMessage.value = 'No se pudieron cargar tus datos. Intenta de nuevo.'
  }
}

const fetchReportes = async () => {
  isLoading.value = true
  errorMessage.value = null

  try {
    const token = localStorage.getItem('accessToken')
    const response = await axios.get('http://localhost:8000/api/reportes/general-1/tutor', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    reportes.value = response.data
    console.log('✅ Reportes cargados:', reportes.value)

    // Si no hay reportes, mostrar formulario directamente
    if (reportes.value.length === 0) {
      await crearNuevoReporte()
    }
  } catch (error) {
    console.error('❌ Error al cargar reportes:', error)
    errorMessage.value = 'No se pudieron cargar los reportes. Intenta de nuevo.'
  } finally {
    isLoading.value = false
  }
}

const guardarReporte = async () => {
  isGuardando.value = true
  errorMessage.value = null
  successMessage.value = null

  try {
    const token = localStorage.getItem('accessToken')
    const payload = {
      nombre_tutor: formulario.value.nombre_tutor,
      periodo: formulario.value.periodo,
      nombre_proyecto: formulario.value.nombre_proyecto,
      porcentaje_avance: formulario.value.porcentaje_avance,
      objetivo: formulario.value.objetivo,
      descripcion: formulario.value.descripcion,
      metas: formulario.value.metas,
      actividades: formulario.value.actividades,
      documentos_anexados: formulario.value.documentos_anexados,
      conclusiones: formulario.value.conclusiones,
      observaciones: formulario.value.observaciones,
    }

    if (modoFormulario.value === 'crear') {
      await axios.post('http://localhost:8000/api/reportes/general-1', payload, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      successMessage.value = '✅ Reporte creado exitosamente'
    } else {
      await axios.put(
        `http://localhost:8000/api/reportes/general-1/${reporteEditando.value.id}`,
        payload,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      )
      successMessage.value = '✅ Reporte actualizado exitosamente'
    }

    await fetchReportes()
    vistaActual.value = 'lista'

    setTimeout(() => {
      successMessage.value = null
    }, 3000)
  } catch (error) {
    console.error('❌ Error al guardar reporte:', error)
    errorMessage.value = `No se pudo ${modoFormulario.value === 'crear' ? 'crear' : 'actualizar'} el reporte. Intenta de nuevo.`
  } finally {
    isGuardando.value = false
  }
}

const eliminarReporte = async () => {
  if (!reporteAEliminar.value) return

  isEliminando.value = true

  try {
    const token = localStorage.getItem('accessToken')
    await axios.delete(
      `http://localhost:8000/api/reportes/general-1/${reporteAEliminar.value.id}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )

    successMessage.value = '✅ Reporte eliminado exitosamente'
    await fetchReportes()
    cancelarEliminar()

    setTimeout(() => {
      successMessage.value = null
    }, 3000)
  } catch (error) {
    console.error('❌ Error al eliminar reporte:', error)
    errorMessage.value = 'No se pudo eliminar el reporte. Intenta de nuevo.'
    cancelarEliminar()
  } finally {
    isEliminando.value = false
  }
}

// ==================== NUEVA FUNCIÓN: DESCARGAR PDF ====================
const descargarPDF = async (reporte) => {
  isDownloadingPDF.value[reporte.id] = true
  errorMessage.value = null

  try {
    const token = localStorage.getItem('accessToken')
    const response = await axios.get(
      `http://localhost:8000/api/reportes/general-1/${reporte.id}/pdf`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        responseType: 'blob', // IMPORTANTE: para recibir el PDF como blob
      },
    )

    // Crear un URL temporal para el blob
    const blob = new Blob([response.data], { type: 'application/pdf' })
    const url = window.URL.createObjectURL(blob)

    // Crear un link temporal y hacer click para descargar
    const link = document.createElement('a')
    link.href = url
    link.download = `Reporte_${reporte.nombre_proyecto.replace(/\s+/g, '_')}_${reporte.id}.pdf`
    document.body.appendChild(link)
    link.click()

    // Limpiar
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    successMessage.value = '✅ PDF descargado exitosamente'
    setTimeout(() => {
      successMessage.value = null
    }, 3000)

    console.log('✅ PDF descargado:', reporte.nombre_proyecto)
  } catch (error) {
    console.error('❌ Error al descargar PDF:', error)
    errorMessage.value = 'No se pudo descargar el PDF. Intenta de nuevo.'
  } finally {
    isDownloadingPDF.value[reporte.id] = false
  }
}
// ==================== HANDLERS ====================
const crearNuevoReporte = async () => {
  // Si no tenemos los datos del tutor, obtenerlos primero
  if (!tutorData.value) {
    await fetchTutorData()
  }

  modoFormulario.value = 'crear'
  reporteEditando.value = null

  formulario.value = {
    nombre_tutor: tutorData.value
      ? `${tutorData.value.nombre} ${tutorData.value.apellido_p} ${tutorData.value.apellido_m}`.trim()
      : '',
    periodo: '',
    nombre_proyecto: '',
    porcentaje_avance: 0,
    objetivo: '',
    descripcion: '',
    metas: '',
    actividades: '',
    documentos_anexados: '',
    conclusiones: '',
    observaciones: '',
  }

  vistaActual.value = 'formulario'
}

const editarReporte = (reporte) => {
  modoFormulario.value = 'editar'
  reporteEditando.value = reporte

  formulario.value = {
    nombre_tutor: reporte.nombre_tutor,
    periodo: reporte.periodo,
    nombre_proyecto: reporte.nombre_proyecto,
    porcentaje_avance: reporte.porcentaje_avance,
    objetivo: reporte.objetivo,
    descripcion: reporte.descripcion,
    metas: reporte.metas,
    actividades: reporte.actividades,
    documentos_anexados: reporte.documentos_anexados,
    conclusiones: reporte.conclusiones,
    observaciones: reporte.observaciones,
  }

  vistaActual.value = 'formulario'
}

const cancelarFormulario = () => {
  vistaActual.value = 'lista'
  reporteEditando.value = null
}

const confirmarEliminar = (reporte) => {
  reporteAEliminar.value = reporte
  mostrarModalEliminar.value = true
}

const cancelarEliminar = () => {
  mostrarModalEliminar.value = false
  reporteAEliminar.value = null
}

// ==================== UTILITY FUNCTIONS ====================
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-MX', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// ==================== LIFECYCLE ====================
onMounted(async () => {
  await fetchTutorData()
  await fetchReportes()
})
</script>
