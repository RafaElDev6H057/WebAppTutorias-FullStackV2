<template>
  <div class="min-h-screen">
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
      <nav class="shadow-sm" style="background-color: white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between h-16">
            <div class="flex items-center">
              <img
                class="h-12 w-12 border-2 border-white rounded-full"
                src="/EscudoITSF.png"
                alt="Escudo ITSF"
              />
              <div class="ml-4">
                <div class="text-lg font-medium" style="color: #0a3b76">
                  {{
                    tutor?.nombre + ' ' + tutor?.apellido_p + ' ' + tutor?.apellido_m ||
                    'Nombre no disponible'
                  }}
                </div>
                <div class="text-sm" style="color: #0a3b76">{{ tutor?.correo }}</div>
              </div>
            </div>

            <div class="flex items-center gap-3">
              <!-- Dropdown de Acciones -->
              <div class="relative z-20" ref="dropdownRef">
                <button
                  @click="showDropdown = !showDropdown"
                  class="text-white px-4 py-2 rounded-md text-sm font-medium transition-colors inline-flex items-center gap-2"
                  style="background-color: #0a3b76"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
                    />
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                  </svg>
                  Acciones
                  <svg
                    class="w-4 h-4 transition-transform"
                    :class="showDropdown ? 'rotate-180' : ''"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M19 9l-7 7-7-7"
                    />
                  </svg>
                </button>

                <!-- Dropdown Menu -->
                <Transition
                  enter-active-class="transition ease-out duration-100"
                  enter-from-class="transform opacity-0 scale-95"
                  enter-to-class="transform opacity-100 scale-100"
                  leave-active-class="transition ease-in duration-75"
                  leave-from-class="transform opacity-100 scale-100"
                  leave-to-class="transform opacity-0 scale-95"
                >
                  <div
                    v-if="showDropdown"
                    class="absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5"
                  >
                    <div class="py-1">
                      <button
                        @click="handleOpenChangePasswordModal()"
                        class="w-full text-left px-4 py-2 text-sm hover:bg-gray-100 inline-flex items-center gap-2"
                        style="color: #0a3b76"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"
                          />
                        </svg>
                        Cambiar Contraseña
                      </button>

                      <button
                        @click="handleDescargarPDF()"
                        :disabled="loading || !studentsData.length"
                        class="w-full text-left px-4 py-2 text-sm hover:bg-gray-100 inline-flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                        style="color: #0a3b76"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                          />
                        </svg>
                        Descargar PDF
                      </button>
                    </div>
                  </div>
                </Transition>
              </div>

              <!-- Botón Cerrar Sesión -->
              <button
                @click="handleLogout"
                class="text-white px-4 py-2 rounded-md text-sm font-medium transition-colors inline-flex items-center gap-2"
                style="background-color: red"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                  />
                </svg>
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </nav>

      <!-- Contenido principal -->
      <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <BannerPasswordWarning
          :show="tutor?.requires_password_change"
          @change-password="openChangePasswordModal"
        />

        <!-- Encabezado y búsqueda -->
        <div class="px-4 py-6 sm:px-0">
          <div
            class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 mb-6"
          >
            <h1 class="text-3xl font-bold" style="color: #0a3b76">Dashboard del Tutor</h1>

            <div class="flex flex-col sm:flex-row gap-3 w-full lg:w-auto">
              <!-- Botón Crear Tutoría -->
              <button
                @click="abrirModalCrear"
                class="px-4 py-2 text-white rounded-md font-medium inline-flex items-center justify-center gap-2 transition-colors shadow-md hover:shadow-lg"
                style="background-color: #abacae"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 4v16m8-8H4"
                  />
                </svg>
                Crear Tutoría
              </button>

              <!-- Dropdown de Reportes -->
              <div class="relative" ref="reportesDropdownRef">
                <button
                  @click="showReportesDropdown = !showReportesDropdown"
                  class="w-full sm:w-auto px-4 py-2 bg-[#0A3B76] hover:bg-[#082e5a] text-white rounded-md font-medium inline-flex items-center justify-center gap-2 transition-colors shadow-md hover:shadow-lg"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                  Reportes
                  <svg
                    class="w-4 h-4 transition-transform"
                    :class="showReportesDropdown ? 'rotate-180' : ''"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M19 9l-7 7-7-7"
                    />
                  </svg>
                </button>

                <!-- Reportes Dropdown Menu -->
                <Transition
                  enter-active-class="transition ease-out duration-100"
                  enter-from-class="transform opacity-0 scale-95"
                  enter-to-class="transform opacity-100 scale-100"
                  leave-active-class="transition ease-in duration-75"
                  leave-from-class="transform opacity-100 scale-100"
                  leave-to-class="transform opacity-0 scale-95"
                >
                  <div
                    v-if="showReportesDropdown"
                    class="absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-10"
                  >
                    <div class="py-1">
                      <!-- Reporte Integral -->
                      <button
                        @click="handleOpenReporteIntegralMasivo()"
                        class="w-full text-left px-4 py-2 text-sm text-[#0A3B76] hover:bg-[#ABACAE]/20 inline-flex items-center gap-2"
                      >
                        <svg
                          class="w-4 h-4 text-[#0A3B76]"
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
                        Reporte Integral
                      </button>

                      <!-- Primer Reporte -->
                      <button
                        @click="handleMostrarModalPrimerReporte()"
                        class="w-full text-left px-4 py-2 text-sm text-[#0A3B76] hover:bg-[#ABACAE]/20 inline-flex items-center gap-2"
                      >
                        <svg
                          class="w-4 h-4 text-[#0A3B76]"
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
                        1° Reporte
                      </button>

                      <!-- Segundo Reporte -->
                      <button
                        @click="handleMostrarModalSegundoReporte()"
                        class="w-full text-left px-4 py-2 text-sm text-[#0A3B76] hover:bg-[#ABACAE]/20 inline-flex items-center gap-2"
                      >
                        <svg
                          class="w-4 h-4 text-[#0A3B76]"
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
                        2° Reporte
                      </button>
                    </div>
                  </div>
                </Transition>
              </div>

              <!-- Búsqueda -->
              <div class="w-full sm:w-64">
                <BaseSearchInput
                  v-model="searchQuery"
                  :disabled="loading"
                  placeholder="Buscar estudiante..."
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Mensaje de Error -->
        <Transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="opacity-0 translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <div
            v-if="error"
            class="mx-4 mb-4 p-4 bg-red-50 border-l-4 border-red-500 rounded-md flex items-start"
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
              <p class="text-sm font-medium text-red-800">{{ error }}</p>
            </div>
            <button @click="error = null" class="text-red-500 hover:text-red-700 ml-4">
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

        <!-- Tabla de Alumnos Tutorados (COMPONENTE) -->
        <TablaAlumnosTutorados
          :students="students"
          :loading="loading"
          :search-query="searchQuery"
          :current-page="currentPage"
          :total-pages="totalPages"
          :total-items="totalItems"
          :items-per-page="itemsPerPage"
          @view-details="viewDetails"
          @delete-tutoria="abrirModalEliminar"
          @prev-page="prevPage"
          @next-page="nextPage"
          @go-to-page="goToPage"
        />

        <!-- Modal de detalles del estudiante -->
        <ModalDetallesEstudiante :show="showModal" :student="selectedStudent" @close="closeModal" />

        <!-- Modal de Cambio de Contraseña -->
        <ModalCambiarPassword
          :show="showChangePasswordModal"
          user-type="tutor"
          :requires-password-change="tutor?.requires_password_change"
          :current-email="tutor?.correo"
          @close="showChangePasswordModal = false"
          @success="handlePasswordChanged"
        />

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
              class="relative top-20 mx-auto p-5 border w-11/12 max-w-5xl shadow-lg rounded-md bg-white"
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
                <ReporteIndividual1 @cerrar="mostrarModalPrimerReporte = false" />
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
              class="relative top-20 mx-auto p-5 border w-11/12 max-w-5xl shadow-lg rounded-md bg-white"
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
                <ReporteIndividual2 @cerrar="mostrarModalSegundoReporte = false" />
              </div>
            </div>
          </div>
        </Transition>
      </main>
    </div>

    <!-- Modal Reporte Integral Masivo -->
    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="showReporteIntegralMasivo" class="fixed inset-0 z-[9999]">
        <ReporteIntegralMasivo
          :tutor-info="{
            nombre: tutor?.nombre + ' ' + tutor?.apellido_p + ' ' + tutor?.apellido_m,
            departamento: 'Sistemas Computacionales',
            periodo: '22025',
            carrera: 'Ingeniería en Sistemas',
          }"
          :tutor-id="tutor?.id_tutor"
          @close="closeReporteIntegralMasivo"
          @success="handleReporteIntegralSuccess"
        />
      </div>
    </Transition>

    <!-- Modal Crear Tutoría (COMPONENTE) -->
    <ModalCrearTutoria
      :show="showModalCrearTutoria"
      :tutor-id="tutor?.id_tutor"
      @close="showModalCrearTutoria = false"
      @success="handleTutoriaCreada"
    />

    <!-- Modal Eliminar Tutoría (COMPONENTE) -->
    <ModalEliminarTutoria
      :show="showModalEliminarTutoria"
      :tutoria="tutoriaAEliminar"
      :tutor-email="tutor?.correo"
      @close="showModalEliminarTutoria = false"
      @success="handleTutoriaEliminada"
    />
  </div>
</template>

<script setup>
import { tutoresAPI } from '@/api/tutores'
import { tutoriasAPI } from '@/api/tutorias'
import { reportesAPI } from '@/api/reportes'
import { ref, computed, onMounted, watch, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import ReporteIntegralMasivo from '@/components/ReporteIntegralMasivo.vue'
import BaseSearchInput from '@/components/ui/BaseSearchInput.vue'
import ReporteIndividual1 from '@/components/tutor/ReporteIndividual1.vue'
import ReporteIndividual2 from '@/components/tutor/ReporteIndividual2.vue'
import TablaAlumnosTutorados from '@/components/tutor/TablaAlumnosTutorados.vue'
import ModalCrearTutoria from '@/components/tutor/ModalCrearTutoria.vue'
import ModalEliminarTutoria from '@/components/tutor/ModalEliminarTutoria.vue'
import ModalCambiarPassword from '@/components/shared/ModalCambiarPassword.vue'
import ModalDetallesEstudiante from '@/components/tutor/ModalDetallesEstudiante.vue'
import BannerPasswordWarning from '@/components/shared/BannerPasswordWarning.vue'

// ==================== ROUTER ====================
const router = useRouter()

// ==================== STATE ====================
const tutor = ref(null)
const studentsData = ref([])
const selectedStudent = ref(null)
const totalItems = ref(0)
let debounceTimer = null

// ==================== UI STATE ====================
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = ref(5)
const loading = ref(false)
const error = ref(null)
const showDropdown = ref(false)
const showReportesDropdown = ref(false)
const dropdownRef = ref(null)
const reportesDropdownRef = ref(null)

// ==================== MODALS STATE ====================
const showModal = ref(false)
const mostrarModalPrimerReporte = ref(false)
const mostrarModalSegundoReporte = ref(false)
const showChangePasswordModal = ref(false)
const showReporteIntegralMasivo = ref(false)
const showModalCrearTutoria = ref(false)
const showModalEliminarTutoria = ref(false)
const tutoriaAEliminar = ref(null)

// ==================== PASSWORD CHANGE STATE ====================
const passwordForm = ref({
  correo: '',
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})
const passwordChangeError = ref(null)
const passwordChangeSuccess = ref(false)

// ==================== CONSTANTS ====================
const circles = [
  { color: 'bg-[#0A3B76]', size: 96, top: 10, left: 5 }, // Azul principal
  { color: 'bg-[#C5C6C8]', size: 64, top: 20, left: 80 }, // Gris claro
  { color: 'bg-[#0C4A99]', size: 128, top: 70, left: 20 }, // Azul más vivo
  { color: 'bg-[#E3E3E4]', size: 80, top: 40, left: 95 }, // Gris muy claro
  { color: 'bg-[#082C54]', size: 112, top: 85, left: 70 }, // Azul oscuro
  { color: 'bg-[#D0D1D3]', size: 48, top: 25, left: 30 }, // Gris suave
  { color: 'bg-[#0A3B76]', size: 72, top: 60, left: 50 }, // Azul principal
  { color: 'bg-[#C5C6C8]', size: 56, top: 5, left: 90 }, // Gris claro
  { color: 'bg-[#C5C6C8]', size: 88, top: 80, left: 40 }, // Gris claro
  { color: 'bg-[#D0D1D3]', size: 40, top: 90, left: 10 }, // Gris suave
  { color: 'bg-[#0C4A99]', size: 104, top: 15, left: 60 }, // Azul vivo
  { color: 'bg-[#E3E3E4]', size: 68, top: 50, left: 85 }, // Gris muy claro
]

// ==================== COMPUTED ====================
const students = computed(() => {
  return studentsData.value
})

const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value))

// ==================== CLICK OUTSIDE HANDLER ====================
const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    showDropdown.value = false
  }
  if (reportesDropdownRef.value && !reportesDropdownRef.value.contains(event.target)) {
    showReportesDropdown.value = false
  }
}

// ==================== API CALLS ====================
const fetchCurrentTutor = async () => {
  try {
    const response = await tutoresAPI.getMe()

    if (response.status === 200) {
      tutor.value = response.data
      console.log('Tutor cargado:', tutor.value)

      passwordForm.value.correo = tutor.value.correo

      await fetchAssignedStudents(currentPage.value)
    }
  } catch (err) {
    console.error('Error al obtener datos del tutor:', err)

    if (err.response && (err.response.status === 401 || err.response.status === 403)) {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('userRole')
      router.push('/login_tutor')
    }
  }
}

const fetchAssignedStudents = async (page) => {
  if (!tutor.value || tutor.value.id_tutor === null) {
    error.value = 'Datos del tutor no disponibles.'
    return
  }

  // loading.value = true
  error.value = null

  try {
    const response = await tutoriasAPI.getByTutor(
      tutor.value.id_tutor,
      page,
      itemsPerPage.value,
      searchQuery.value,
    )
    console.log(response.data)

    totalItems.value = response.data.total_tutorias

    studentsData.value = response.data.tutorias.map((tutoria) => ({
      id: tutoria.alumno?.id_alumno || null,
      name: tutoria.alumno
        ? `${tutoria.alumno.nombre || ''} ${tutoria.alumno.apellido_p || ''} ${tutoria.alumno.apellido_m || ''}`.trim()
        : 'Alumno Desconocido',
      controlNumber: tutoria.alumno?.num_control || 'N/A',
      semester: tutoria.semestre,
      status: tutoria.alumno?.estado || 'N/A',
      tutorialPeriod: tutoria.periodo,
      tutoringId: tutoria.id_tutoria,
      nombre: tutoria.alumno
        ? `${tutoria.alumno.nombre || ''} ${tutoria.alumno.apellido_p || ''} ${tutoria.alumno.apellido_m || ''}`.trim()
        : 'Alumno Desconocido',
      num_control: tutoria.alumno?.num_control || 'N/A',
    }))
  } catch (err) {
    console.error('Error al obtener las tutorías asignadas:', err)
    if (
      err.response &&
      err.response.status === 400 &&
      err.response.data.detail?.includes('string_too_short')
    ) {
      error.value = 'Favor de ingresar mínimo 3 caracteres a buscar.'
    } else if (err.response?.status !== 401 && err.response?.status !== 403) {
      error.value = 'No se pudo cargar la lista de alumnos asignados.'
    }
    studentsData.value = []
    totalItems.value = 0
  } finally {
    loading.value = false
  }
}

// ==================== PASSWORD CHANGE HANDLERS ====================
const openChangePasswordModal = () => {
  showChangePasswordModal.value = true
  passwordChangeError.value = null
  passwordChangeSuccess.value = false
  passwordForm.value = {
    correo: tutor.value?.correo || '',
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  }
}

// ==================== TUTORÍA HANDLERS ====================
const handleTutoriaCreada = async () => {
  showModalCrearTutoria.value = false
  await fetchAssignedStudents(currentPage.value)
}

const abrirModalCrear = () => {
  showModalCrearTutoria.value = true
}

const abrirModalEliminar = (student) => {
  tutoriaAEliminar.value = student
  showModalEliminarTutoria.value = true
}

const handleTutoriaEliminada = async () => {
  showModalEliminarTutoria.value = false
  tutoriaAEliminar.value = null
  await fetchAssignedStudents(1)
}

// ==================== SEARCH WATCHER ====================
watch(searchQuery, () => {
  clearTimeout(debounceTimer)

  debounceTimer = setTimeout(() => {
    currentPage.value = 1
    fetchAssignedStudents()
  }, 500)
})

// ==================== MODAL HANDLERS ====================
const viewDetails = async (student) => {
  try {
    const tutoringResponse = await tutoriasAPI.getByAlumno(student.tutoringId)

    selectedStudent.value = {
      ...tutoringResponse.data.alumno,
      tutoring: tutoringResponse.data,
    }
    showModal.value = true
  } catch (err) {
    console.error('Error fetching student details:', err)
    error.value = 'No se pudieron cargar los detalles del estudiante.'
  }
}

const closeModal = () => {
  showModal.value = false
  selectedStudent.value = null
}

const openReporteIntegralMasivo = () => {
  showReporteIntegralMasivo.value = true
}

const closeReporteIntegralMasivo = () => {
  showReporteIntegralMasivo.value = false
}

const handleReporteIntegralSuccess = () => {
  closeReporteIntegralMasivo()
}

const handlePasswordChanged = async () => {
  showChangePasswordModal.value = false

  if (tutor.value) {
    tutor.value.requires_password_change = false
  }
}

const handleOpenChangePasswordModal = () => {
  openChangePasswordModal()
  showDropdown.value = false
}

const handleDescargarPDF = () => {
  descargarPDFReporteIntegral()
  showDropdown.value = false
}

const handleOpenReporteIntegralMasivo = () => {
  openReporteIntegralMasivo()
  showDropdown.value = false
}

const handleMostrarModalPrimerReporte = () => {
  mostrarModalPrimerReporte.value = true
  showReportesDropdown.value = false
}

const handleMostrarModalSegundoReporte = () => {
  mostrarModalSegundoReporte.value = true
  showReportesDropdown.value = false
}

// ==================== PAGINATION ====================
const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    fetchAssignedStudents(currentPage.value)
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    fetchAssignedStudents(currentPage.value)
  }
}

const goToPage = (page) => {
  currentPage.value = page
  fetchAssignedStudents(page)
}

// ==================== AUTH ====================
const handleLogout = () => {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('userRole')
  router.push('/')
}

// ==================== DESCARGA PDF ====================
const descargarPDFReporteIntegral = async () => {
  try {
    loading.value = true

    const periodo = studentsData.value?.tutorialPeriod || '22025'

    const response = await reportesAPI.downloadIntegralPDF(tutor.value.id_tutor, periodo)

    const blob = new Blob([response.data], { type: 'application/pdf' })
    const url = window.URL.createObjectURL(blob)

    const link = document.createElement('a')
    link.href = url
    link.download = `Reporte_Integral_${tutor.value.nombre}_${periodo}.pdf`
    document.body.appendChild(link)
    link.click()

    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    console.log('✅ PDF descargado exitosamente')
  } catch (err) {
    console.error('Error al descargar PDF:', err)
    if (err.response?.status === 404) {
      error.value = 'No se encontraron reportes integrales para descargar.'
    } else {
      error.value = 'Error al generar el PDF. Intenta de nuevo.'
    }
  } finally {
    loading.value = false
  }
}

// ==================== LIFECYCLE ====================
onMounted(async () => {
  await fetchCurrentTutor()
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style>
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

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
</style>
