<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-white relative overflow-hidden">
    <!-- Animated Circles -->
    <div class="absolute inset-0 pointer-events-none overflow-hidden">
      <div
        v-for="(circle, index) in departamentoConfig.circles"
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

    <!-- Header -->
    <nav class="shadow-lg relative z-10" :class="departamentoConfig.headerBg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <img
              class="h-12 w-12 border-2 border-white rounded-full"
              src="/EscudoITSF.png"
              alt="Escudo ITSF"
            />
            <div class="ml-4">
              <div class="text-lg font-medium text-white">{{ departamentoConfig.titulo }}</div>
              <div class="text-sm" :class="departamentoConfig.headerSubtitle">
                {{ departamentoConfig.descripcion }}
              </div>
            </div>
          </div>
          <div class="flex items-center">
            <button
              @click="handleLogout"
              class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium transition duration-150 ease-in-out flex items-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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

    <!-- Main Content -->
    <main class="max-w-5xl mx-auto py-12 px-4 sm:px-6 lg:px-8 relative z-10">
      <!-- Título de Bienvenida -->
      <div class="text-center mb-12">
        <div class="flex items-center justify-center gap-4 mb-4">
          <div
            :class="[
              'h-16 w-16 rounded-2xl flex items-center justify-center shadow-lg',
              departamentoConfig.bgColor,
            ]"
          >
            <component
              :is="departamentoConfig.icon"
              :class="['h-8 w-8', departamentoConfig.iconColor]"
            ></component>
          </div>
        </div>
        <h1 class="text-4xl font-bold text-gray-900 mb-2">
          Bienvenido al {{ departamentoConfig.titulo }}
        </h1>
        <p class="text-lg text-gray-600">Descarga tus reportes institucionales</p>
      </div>

      <!-- Card de Descarga de Reporte -->
      <div
        class="bg-white rounded-2xl shadow-xl p-8 border-l-4"
        :class="departamentoConfig.borderColor"
      >
        <!-- Header del Card -->
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center gap-4">
            <div
              :class="[
                'h-14 w-14 rounded-xl flex items-center justify-center',
                departamentoConfig.bgColor,
              ]"
            >
              <svg
                class="w-7 h-7"
                :class="departamentoConfig.iconColor"
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
              <h2 class="text-2xl font-bold text-gray-900">
                {{ departamentoConfig.reporteTitulo }}
              </h2>
              <p class="text-sm text-gray-600">{{ departamentoConfig.reporteDescripcion }}</p>
            </div>
          </div>
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
            class="mb-6 p-4 bg-green-50 border-l-4 border-green-500 rounded"
          >
            <p class="text-sm text-green-800 font-medium">{{ successMessage }}</p>
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
          <div v-if="errorMessage" class="mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded">
            <p class="text-sm text-red-800 font-medium">{{ errorMessage }}</p>
          </div>
        </Transition>

        <!-- Formulario de Descarga -->
        <div class="space-y-6">
          <!-- Selector de Periodo -->
          <div>
            <label for="periodo" class="block text-sm font-bold text-gray-800 mb-3">
              Selecciona el Periodo Académico
            </label>
            <div class="relative">
              <input
                id="periodo"
                v-model="periodo"
                type="text"
                maxlength="5"
                placeholder="Ejemplo: 22025"
                :disabled="isDownloading"
                class="w-full px-5 py-4 text-lg border-2 border-gray-300 rounded-xl focus:outline-none focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed transition-all shadow-sm"
                :class="`focus:ring-2 focus:ring-${departamentoConfig.ringColor}`"
              />
              <div class="absolute right-4 top-1/2 transform -translate-y-1/2">
                <svg
                  class="w-6 h-6 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
              </div>
            </div>
            <p class="text-xs text-gray-500 mt-2 flex items-center gap-1">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                  clip-rule="evenodd"
                />
              </svg>
              Formato: 5 dígitos (Ej: 22025 = 2do semestre de 2025)
            </p>
          </div>

          <!-- Información del Reporte -->
          <div
            :class="[
              'p-4 rounded-xl border-2',
              departamentoConfig.infoBg,
              departamentoConfig.infoBorder,
            ]"
          >
            <div class="flex items-start gap-3">
              <svg
                class="w-5 h-5 flex-shrink-0 mt-0.5"
                :class="departamentoConfig.iconColor"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fill-rule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                  clip-rule="evenodd"
                />
              </svg>
              <div class="flex-1">
                <p class="text-sm font-bold" :class="departamentoConfig.infoText">
                  ℹ️ Información del Reporte
                </p>
                <p class="text-xs mt-1" :class="departamentoConfig.infoText">
                  {{ departamentoConfig.reporteInfo }}
                </p>
              </div>
            </div>
          </div>

          <!-- Botón de Descarga -->
          <button
            @click="descargarReporte"
            :disabled="isDownloading || !periodo || periodo.length !== 5"
            :class="[
              'w-full py-4 rounded-xl font-bold text-white text-lg focus:outline-none focus:ring-4 focus:ring-offset-2 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 disabled:transform-none flex items-center justify-center gap-3',
              isDownloading || !periodo || periodo.length !== 5
                ? 'bg-gray-400'
                : departamentoConfig.buttonColor,
            ]"
          >
            <svg
              v-if="isDownloading"
              class="animate-spin h-6 w-6 text-white"
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
            <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            {{ isDownloading ? 'Descargando Reporte...' : 'Descargar Reporte Excel' }}
          </button>
        </div>

        <!-- Footer del Card -->
        <div class="mt-8 pt-6 border-t border-gray-200">
          <div class="flex items-center justify-between text-sm text-gray-600">
            <div class="flex items-center gap-2">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                  clip-rule="evenodd"
                />
              </svg>
              <span>Última actualización: {{ new Date().toLocaleDateString('es-MX') }}</span>
            </div>
            <div class="flex items-center gap-2">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                <path
                  fill-rule="evenodd"
                  d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z"
                  clip-rule="evenodd"
                />
              </svg>
              <span>Formato: Excel (.xlsx)</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Card Informativa Adicional -->
      <div
        class="mt-8 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200"
      >
        <div class="flex items-start gap-4">
          <div class="flex-shrink-0">
            <svg
              class="w-8 h-8 text-blue-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-bold text-gray-900 mb-2">💡 Ayuda y Soporte</h3>
            <ul class="space-y-2 text-sm text-gray-700">
              <li class="flex items-center gap-2">
                <svg class="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clip-rule="evenodd"
                  />
                </svg>
                Verifica que el periodo sea correcto antes de descargar
              </li>
              <li class="flex items-center gap-2">
                <svg class="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clip-rule="evenodd"
                  />
                </svg>
                Si no hay datos disponibles, recibirás un mensaje de error
              </li>
              <li class="flex items-center gap-2">
                <svg class="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clip-rule="evenodd"
                  />
                </svg>
                Para problemas técnicos, contacta al administrador del sistema
              </li>
            </ul>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import PsicologiaLogo from '@/components/icons/PsicologiaLogo.vue'
import CienciasLogo from '@/components/icons/CienciasLogo.vue'
import JefaturaLogo from '@/components/icons/JefaturaLogo.vue'

// ==================== ROUTER ====================
const router = useRouter()

// ==================== STATE ====================
const periodo = ref('22025')
const isDownloading = ref(false)
const successMessage = ref(null)
const errorMessage = ref(null)
const userRole = ref(null)

// ==================== CONFIGURACIÓN POR DEPARTAMENTO ====================
const departamentosConfig = {
  psicologia: {
    titulo: 'Departamento de Psicología',
    descripcion: 'Área de Desarrollo Estudiantil',
    icon: PsicologiaLogo,
    bgColor: 'bg-teal-100',
    iconColor: 'text-teal-600',
    buttonColor: 'bg-teal-600 hover:bg-teal-700 focus:ring-teal-500',
    ringColor: 'teal-500',
    headerBg: 'bg-teal-600',
    headerSubtitle: 'text-teal-200',
    borderColor: 'border-teal-500',
    infoBg: 'bg-teal-50',
    infoBorder: 'border-teal-200',
    infoText: 'text-teal-800',
    reporteTitulo: 'Reporte de Psicología',
    reporteDescripcion: 'Consolidado de atención psicológica estudiantil',
    reporteInfo:
      'Este reporte contiene información consolidada de las sesiones y seguimientos del área de psicología para el periodo seleccionado.',
    endpoint: '/api/canalizaciones/psicologia',
    circles: [
      { color: 'bg-teal-300', size: 96, top: 10, left: 5 },
      { color: 'bg-cyan-200', size: 64, top: 20, left: 85 },
      { color: 'bg-teal-400', size: 128, top: 70, left: 15 },
      { color: 'bg-cyan-300', size: 80, top: 40, left: 90 },
      { color: 'bg-teal-200', size: 112, top: 85, left: 60 },
    ],
  },
  ciencias_basicas: {
    titulo: 'Departamento de Ciencias Básicas',
    descripcion: 'Coordinación Académica',
    icon: CienciasLogo,
    bgColor: 'bg-indigo-100',
    iconColor: 'text-indigo-600',
    buttonColor: 'bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500',
    ringColor: 'indigo-500',
    headerBg: 'bg-indigo-600',
    headerSubtitle: 'text-indigo-200',
    borderColor: 'border-indigo-500',
    infoBg: 'bg-indigo-50',
    infoBorder: 'border-indigo-200',
    infoText: 'text-indigo-800',
    reporteTitulo: 'Reporte de Ciencias Básicas',
    reporteDescripcion: 'Consolidado académico del departamento',
    reporteInfo:
      'Este reporte contiene información consolidada del desempeño académico y actividades del departamento de Ciencias Básicas.',
    endpoint: '/api/canalizaciones/ciencias-basicas',
    circles: [
      { color: 'bg-indigo-300', size: 96, top: 10, left: 5 },
      { color: 'bg-purple-200', size: 64, top: 20, left: 85 },
      { color: 'bg-indigo-400', size: 128, top: 70, left: 15 },
      { color: 'bg-purple-300', size: 80, top: 40, left: 90 },
      { color: 'bg-indigo-200', size: 112, top: 85, left: 60 },
    ],
  },
  jefatura_academica: {
    titulo: 'Jefatura Académica',
    descripcion: 'Coordinación y Supervisión',
    icon: JefaturaLogo,
    bgColor: 'bg-rose-100',
    iconColor: 'text-rose-600',
    buttonColor: 'bg-rose-600 hover:bg-rose-700 focus:ring-rose-500',
    ringColor: 'rose-500',
    headerBg: 'bg-rose-600',
    headerSubtitle: 'text-rose-200',
    borderColor: 'border-rose-500',
    infoBg: 'bg-rose-50',
    infoBorder: 'border-rose-200',
    infoText: 'text-rose-800',
    reporteTitulo: 'Reporte de Jefatura Académica',
    reporteDescripcion: 'Consolidado de gestión académica institucional',
    reporteInfo:
      'Este reporte contiene información consolidada de la gestión académica, coordinación y supervisión institucional.',
    endpoint: '/api/canalizaciones/jefatura-academica',
    circles: [
      { color: 'bg-rose-300', size: 96, top: 10, left: 5 },
      { color: 'bg-pink-200', size: 64, top: 20, left: 85 },
      { color: 'bg-rose-400', size: 128, top: 70, left: 15 },
      { color: 'bg-pink-300', size: 80, top: 40, left: 90 },
      { color: 'bg-rose-200', size: 112, top: 85, left: 60 },
    ],
  },
}

// ==================== COMPUTED ====================
const departamentoConfig = computed(() => {
  return departamentosConfig[userRole.value] || departamentosConfig.psicologia
})

// ==================== LIFECYCLE ====================
onMounted(() => {
  // Verificar autenticación
  const token = localStorage.getItem('accessToken')
  const role = localStorage.getItem('userRole')

  if (!token || !role) {
    console.log('No hay token o rol, redirigiendo...')
    router.push('/')
    return
  }

  userRole.value = role

  // Validar que el rol sea válido para departamentos
  if (!['psicologia', 'ciencias_basicas', 'jefatura_academica'].includes(role)) {
    console.error('Rol no válido para esta vista:', role)
    router.push('/')
  }
})

// ==================== HANDLERS ====================
const descargarReporte = async () => {
  // Validar periodo
  if (!periodo.value || periodo.value.length !== 5) {
    errorMessage.value = 'El periodo debe tener exactamente 5 dígitos'
    return
  }

  isDownloading.value = true
  errorMessage.value = null
  successMessage.value = null

  try {
    const token = localStorage.getItem('accessToken')

    if (!token) {
      console.log('No hay token, redirigiendo...')
      router.push('/')
      return
    }

    const response = await axios.get(
      `http://localhost:8000${departamentoConfig.value.endpoint}/${periodo.value}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        responseType: 'blob',
      },
    )

    // Crear el blob y descargar
    const blob = new Blob([response.data], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    })
    const url = window.URL.createObjectURL(blob)

    const link = document.createElement('a')
    link.href = url
    link.download = `Reporte_${userRole.value}_${periodo.value}.xlsx`
    document.body.appendChild(link)
    link.click()

    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    successMessage.value = '✅ Reporte descargado exitosamente'
    console.log('✅ Reporte descargado:', periodo.value)

    setTimeout(() => {
      successMessage.value = null
    }, 5000)
  } catch (error) {
    console.error('❌ Error al descargar reporte:', error)

    if (error.response?.status === 404) {
      errorMessage.value = 'No se encontraron datos para el periodo especificado'
    } else if (error.response?.status === 400) {
      errorMessage.value = 'Periodo inválido. Verifica el formato.'
    } else if (error.response?.status === 401 || error.response?.status === 403) {
      errorMessage.value = 'Sesión expirada. Por favor inicia sesión nuevamente.'
      setTimeout(() => {
        handleLogout()
      }, 2000)
    } else {
      errorMessage.value = 'Error al descargar el archivo. Intenta de nuevo.'
    }
  } finally {
    isDownloading.value = false
  }
}

const handleLogout = () => {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('userRole')
  router.push('/')
}
</script>

<style scoped>
@keyframes float-1 {
  0%,
  100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(5deg);
  }
}

@keyframes float-2 {
  0%,
  100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-30px) rotate(-5deg);
  }
}

@keyframes float-3 {
  0%,
  100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-25px) rotate(3deg);
  }
}

.animate-float-1 {
  animation: float-1 6s ease-in-out infinite;
}

.animate-float-2 {
  animation: float-2 8s ease-in-out infinite;
}

.animate-float-3 {
  animation: float-3 7s ease-in-out infinite;
}
</style>
