<template>
  <!-- ==================== CONTROL DE ETAPAS - REPORTE INTEGRAL ==================== -->
  <div class="mb-8 bg-white rounded-lg shadow-md p-6 border-l-4 border-indigo-500">
    <div class="flex items-center justify-between mb-4">
      <div>
        <h2 class="text-xl font-bold text-gray-900 flex items-center gap-2">
          <svg
            class="w-6 h-6 text-indigo-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"
            />
          </svg>
          Control de Etapas - Reporte Integral
        </h2>
        <p class="text-sm text-gray-600 mt-1">
          Controla qué campos pueden llenar los tutores en el Reporte Integral
        </p>
      </div>

      <!-- Etapa Actual -->
      <div v-if="!isLoadingEtapa" class="text-right">
        <p class="text-sm text-gray-600">Etapa Actual:</p>
        <div class="flex items-center gap-2 mt-1">
          <span
            :class="[
              'px-4 py-2 rounded-full font-bold text-lg',
              {
                'bg-gray-200 text-gray-700': reporteIntegralEtapa === 0,
                'bg-yellow-100 text-yellow-800': reporteIntegralEtapa === 1,
                'bg-blue-100 text-blue-800': reporteIntegralEtapa === 2,
                'bg-green-100 text-green-800': reporteIntegralEtapa === 3,
              },
            ]"
          >
            {{ reporteIntegralEtapa === 0 ? 'Bloqueado' : `Etapa ${reporteIntegralEtapa}` }}
          </span>
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
      <div v-if="successEtapa" class="mb-4 p-3 bg-green-50 border-l-4 border-green-500 rounded">
        <p class="text-sm text-green-800 font-medium">{{ successEtapa }}</p>
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
      <div v-if="errorEtapa" class="mb-4 p-3 bg-red-50 border-l-4 border-red-500 rounded">
        <p class="text-sm text-red-800 font-medium">{{ errorEtapa }}</p>
      </div>
    </Transition>

    <!-- Botones de Etapas -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <!-- Botón Etapa 1 -->
      <button
        @click="cambiarEtapa(1)"
        :disabled="isLoadingEtapa"
        :class="[
          'p-4 rounded-lg border-2 transition-all duration-200 text-left',
          reporteIntegralEtapa === 1
            ? 'border-yellow-500 bg-yellow-50 shadow-md'
            : 'border-gray-300 hover:border-yellow-400 hover:bg-yellow-50',
          isLoadingEtapa ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer',
        ]"
      >
        <div class="flex items-start gap-3">
          <div
            :class="[
              'flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg',
              reporteIntegralEtapa === 1 ? 'bg-yellow-500 text-white' : 'bg-gray-200 text-gray-600',
            ]"
          >
            1
          </div>
          <div class="flex-1">
            <h3 class="font-bold text-gray-900 mb-1">Etapa 1</h3>
            <p class="text-sm text-gray-600">Solo Seguimiento 1</p>
            <div class="mt-2 flex items-center gap-2">
              <svg class="w-4 h-4 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clip-rule="evenodd"
                />
              </svg>
              <span class="text-xs text-gray-600">seguimiento_1</span>
            </div>
          </div>
          <div v-if="reporteIntegralEtapa === 1" class="flex-shrink-0">
            <svg class="w-6 h-6 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
        </div>
      </button>

      <!-- Botón Etapa 2 -->
      <button
        @click="cambiarEtapa(2)"
        :disabled="isLoadingEtapa"
        :class="[
          'p-4 rounded-lg border-2 transition-all duration-200 text-left',
          reporteIntegralEtapa === 2
            ? 'border-blue-500 bg-blue-50 shadow-md'
            : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50',
          isLoadingEtapa ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer',
        ]"
      >
        <div class="flex items-start gap-3">
          <div
            :class="[
              'flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg',
              reporteIntegralEtapa === 2 ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-600',
            ]"
          >
            2
          </div>
          <div class="flex-1">
            <h3 class="font-bold text-gray-900 mb-1">Etapa 2</h3>
            <p class="text-sm text-gray-600">Seguimientos 1 y 2</p>
            <div class="mt-2 space-y-1">
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clip-rule="evenodd"
                  />
                </svg>
                <span class="text-xs text-gray-600">seguimiento_1, seguimiento_2</span>
              </div>
            </div>
          </div>
          <div v-if="reporteIntegralEtapa === 2" class="flex-shrink-0">
            <svg class="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
        </div>
      </button>

      <!-- Botón Etapa 3 -->
      <button
        @click="cambiarEtapa(3)"
        :disabled="isLoadingEtapa"
        :class="[
          'p-4 rounded-lg border-2 transition-all duration-200 text-left',
          reporteIntegralEtapa === 3
            ? 'border-green-500 bg-green-50 shadow-md'
            : 'border-gray-300 hover:border-green-400 hover:bg-green-50',
          isLoadingEtapa ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer',
        ]"
      >
        <div class="flex items-start gap-3">
          <div
            :class="[
              'flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg',
              reporteIntegralEtapa === 3 ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-600',
            ]"
          >
            3
          </div>
          <div class="flex-1">
            <h3 class="font-bold text-gray-900 mb-1">Etapa 3</h3>
            <p class="text-sm text-gray-600">Todos los campos</p>
            <div class="mt-2">
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clip-rule="evenodd"
                  />
                </svg>
                <span class="text-xs text-gray-600">Reporte completo</span>
              </div>
            </div>
          </div>
          <div v-if="reporteIntegralEtapa === 3" class="flex-shrink-0">
            <svg class="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
        </div>
      </button>
    </div>

    <!-- Loader -->
    <div v-if="isLoadingEtapa" class="mt-4 flex items-center justify-center">
      <svg
        class="animate-spin h-6 w-6 text-indigo-600"
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
      <span class="ml-2 text-sm text-gray-600">Actualizando etapa...</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

// ==================== ROUTER ====================
const router = useRouter()

// ==================== STATE ====================
const reporteIntegralEtapa = ref(null)
const isLoadingEtapa = ref(false)
const errorEtapa = ref(null)
const successEtapa = ref(null)

// ==================== API CALLS ====================
const fetchConfiguracion = async () => {
  isLoadingEtapa.value = true
  errorEtapa.value = null

  try {
    const token = localStorage.getItem('accessToken')

    if (!token) {
      console.log('No hay token, redirigiendo al login...')
      router.push('/login_admin')
      return
    }

    const response = await axios.get('http://localhost:8000/api/configuracion/', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (response.status === 200) {
      reporteIntegralEtapa.value = response.data.reporte_integral_etapa
      console.log('✅ Configuración cargada:', response.data)
    }
  } catch (error) {
    console.error('❌ Error al cargar configuración:', error)
    errorEtapa.value = 'No se pudo cargar la configuración'
  } finally {
    isLoadingEtapa.value = false
  }
}

const cambiarEtapa = async (nuevaEtapa) => {
  isLoadingEtapa.value = true
  errorEtapa.value = null
  successEtapa.value = null

  try {
    const token = localStorage.getItem('accessToken')

    if (!token) {
      console.log('No hay token, redirigiendo al login...')
      router.push('/login_admin')
      return
    }

    const response = await axios.put(
      'http://localhost:8000/api/configuracion/',
      {
        reporte_integral_etapa: nuevaEtapa,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )

    if (response.status === 200) {
      reporteIntegralEtapa.value = nuevaEtapa
      successEtapa.value = `✅ Etapa cambiada exitosamente a: Etapa ${nuevaEtapa}`
      console.log('✅ Etapa actualizada:', nuevaEtapa)

      setTimeout(() => {
        successEtapa.value = null
      }, 3000)
    }
  } catch (error) {
    console.error('❌ Error al cambiar etapa:', error)
    errorEtapa.value = 'No se pudo cambiar la etapa. Intenta de nuevo.'
  } finally {
    isLoadingEtapa.value = false
  }
}

// ==================== LIFECYCLE HOOKS ====================
onMounted(async () => {
  await fetchConfiguracion()
})
</script>
