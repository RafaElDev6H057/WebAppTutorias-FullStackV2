<template>
  <div class="space-y-8">
    <!-- ==================== CONTROL DE ETAPAS - REPORTE INTEGRAL ==================== -->
    <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-indigo-500">
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
                reporteIntegralEtapa === 1
                  ? 'bg-yellow-500 text-white'
                  : 'bg-gray-200 text-gray-600',
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
                reporteIntegralEtapa === 3
                  ? 'bg-green-500 text-white'
                  : 'bg-gray-200 text-gray-600',
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

    <!-- ==================== DESCARGA DE ANEXO 3 ==================== -->
    <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-emerald-500">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h2 class="text-xl font-bold text-gray-900 flex items-center gap-2">
            <svg
              class="w-6 h-6 text-emerald-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            Descarga de Reportes - ANEXO 3
          </h2>
          <p class="text-sm text-gray-600 mt-1">
            Descarga el archivo Excel del ANEXO 3 para el periodo seleccionado
          </p>
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
        <div v-if="successAnexo" class="mb-4 p-3 bg-green-50 border-l-4 border-green-500 rounded">
          <p class="text-sm text-green-800 font-medium">{{ successAnexo }}</p>
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
        <div v-if="errorAnexo" class="mb-4 p-3 bg-red-50 border-l-4 border-red-500 rounded">
          <p class="text-sm text-red-800 font-medium">{{ errorAnexo }}</p>
        </div>
      </Transition>

      <!-- Selector de Periodo -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="periodo" class="block text-sm font-medium text-gray-700 mb-2">
            Periodo Académico
          </label>
          <input
            id="periodo"
            v-model="periodoAnexo"
            type="text"
            maxlength="5"
            placeholder="22025"
            :disabled="isDownloadingAnexo"
            class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 disabled:bg-gray-100 disabled:cursor-not-allowed transition-all"
          />
          <p class="text-xs text-gray-500 mt-1">Formato: 22025 (5 dígitos)</p>
        </div>

        <div class="flex items-center">
          <button
            @click="descargarAnexo3"
            :disabled="isDownloadingAnexo || !periodoAnexo || periodoAnexo.length !== 5"
            class="w-full px-6 py-2 rounded-lg font-bold text-white focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:cursor-not-allowed transition-all inline-flex justify-center items-center shadow-md hover:shadow-lg mt-2"
            :class="
              isDownloadingAnexo || !periodoAnexo || periodoAnexo.length !== 5
                ? 'bg-gray-400'
                : 'bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-700 hover:to-emerald-800 focus:ring-emerald-500'
            "
          >
            <svg
              v-if="isDownloadingAnexo"
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
            <svg v-else class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            {{ isDownloadingAnexo ? 'Descargando...' : 'Descargar ANEXO 3 (Excel)' }}
          </button>
        </div>
      </div>

      <!-- Información adicional -->
      <div class="mt-4 p-4 bg-emerald-50 rounded-lg border border-emerald-200">
        <div class="flex items-start gap-3">
          <svg
            class="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5"
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
            <p class="text-sm text-emerald-800 font-medium">Información del Reporte</p>
            <p class="text-xs text-emerald-700 mt-1">
              El ANEXO 3 contiene toda la información consolidada de las tutorías del periodo
              seleccionado. El archivo se descargará en formato Excel (.xlsx).
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

// ==================== ROUTER ====================
const router = useRouter()

// ==================== STATE - ETAPAS ====================
const reporteIntegralEtapa = ref(null)
const isLoadingEtapa = ref(false)
const errorEtapa = ref(null)
const successEtapa = ref(null)

// ==================== STATE - ANEXO 3 ====================
const periodoAnexo = ref('22025')
const isDownloadingAnexo = ref(false)
const errorAnexo = ref(null)
const successAnexo = ref(null)

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

const descargarAnexo3 = async () => {
  // Validar periodo
  if (!periodoAnexo.value || periodoAnexo.value.length !== 5) {
    errorAnexo.value = 'El periodo debe tener exactamente 5 dígitos'
    return
  }

  isDownloadingAnexo.value = true
  errorAnexo.value = null
  successAnexo.value = null

  try {
    const token = localStorage.getItem('accessToken')

    if (!token) {
      console.log('No hay token, redirigiendo al login...')
      router.push('/login_admin')
      return
    }

    const response = await axios.get(
      `http://localhost:8000/api/reportes/anexo-3/excel/${periodoAnexo.value}`,
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
    link.download = `ANEXO_3_${periodoAnexo.value}.xlsx`
    document.body.appendChild(link)
    link.click()

    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    successAnexo.value = '✅ ANEXO 3 descargado exitosamente'
    console.log('✅ ANEXO 3 descargado:', periodoAnexo.value)

    setTimeout(() => {
      successAnexo.value = null
    }, 3000)
  } catch (error) {
    console.error('❌ Error al descargar ANEXO 3:', error)

    if (error.response?.status === 404) {
      errorAnexo.value = 'No se encontraron datos para el periodo especificado'
    } else if (error.response?.status === 400) {
      errorAnexo.value = 'Periodo inválido. Verifica el formato.'
    } else {
      errorAnexo.value = 'Error al descargar el archivo. Intenta de nuevo.'
    }
  } finally {
    isDownloadingAnexo.value = false
  }
}

// ==================== LIFECYCLE HOOKS ====================
onMounted(async () => {
  await fetchConfiguracion()
})
</script>
