<template>
  <!-- ==================== CONTAINER AVISOS ALUMNO ==================== -->
  <div class="space-y-4">
    <!-- Header -->
    <div class="flex items-center gap-3 mb-4">
      <div class="w-12 h-12 bg-[#0A3B76] rounded-full flex items-center justify-center shadow-md">
        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
          />
        </svg>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-800">Avisos Importantes</h2>
        <p class="text-sm text-gray-600">Mantente informado sobre las últimas novedades</p>
      </div>
    </div>
  </div>

  <!-- ==================== LOADING ==================== -->
  <div v-if="isLoading" class="flex justify-center items-center py-12">
    <svg
      class="animate-spin h-8 w-8 text-lime-500"
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
    <span class="ml-3 text-gray-600">Cargando avisos...</span>
  </div>

  <!-- ==================== ERROR ==================== -->
  <div v-else-if="errorMessage" class="bg-red-50 border border-red-200 rounded-lg p-4 shadow-sm">
    <div class="flex items-center gap-2">
      <svg class="w-5 h-5 text-red-600" fill="currentColor" viewBox="0 0 20 20">
        <path
          fill-rule="evenodd"
          d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
          clip-rule="evenodd"
        />
      </svg>
      <p class="text-sm text-red-800 font-medium">{{ errorMessage }}</p>
    </div>
  </div>

  <!-- ==================== LISTA DE AVISOS ==================== -->
  <div v-else-if="avisos.length > 0" class="space-y-3">
    <TransitionGroup
      name="aviso"
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0 translate-y-4"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-for="aviso in avisos"
        :key="aviso.id"
        class="bg-gradient-to-br from-lime-50 to-lime-100 border border-lime-300 rounded-lg p-5 hover:border-lime-400 hover:shadow-lg transition-all duration-300 group"
      >
        <!-- Badge "Nuevo" si fue creado hace menos de 7 días -->
        <div class="flex items-start justify-between mb-3">
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-2 flex-wrap">
              <h3 class="text-lg font-bold text-gray-900">{{ aviso.titulo }}</h3>
              <span
                v-if="isNew(aviso.created_at)"
                class="px-2.5 py-1 text-xs font-bold bg-gradient-to-r from-lime-500 to-lime-600 text-white rounded-full shadow-md animate-pulse"
              >
                ✨ NUEVO
              </span>
            </div>
            <p class="text-sm text-gray-700 leading-relaxed">{{ aviso.descripcion }}</p>
          </div>
        </div>

        <!-- Link (si existe) -->
        <div
          v-if="aviso.link"
          class="mt-4 pt-4 border-t border-lime-200 group-hover:border-lime-300 transition-colors"
        >
          <a
            :href="aviso.link"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center gap-2 text-lime-700 hover:text-lime-800 text-sm font-semibold transition-colors duration-200 group/link"
          >
            <svg
              class="w-4 h-4 group-hover/link:rotate-12 transition-transform duration-200"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"
              />
            </svg>
            Ver más información
            <svg
              class="w-4 h-4 group-hover/link:translate-x-1 transition-transform duration-200"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 7l5 5m0 0l-5 5m5-5H6"
              />
            </svg>
          </a>
        </div>

        <!-- Fecha de publicación -->
        <div class="mt-4 flex items-center gap-2 text-xs text-gray-600">
          <svg class="w-4 h-4 text-lime-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <span class="font-medium">Publicado: {{ formatDate(aviso.created_at) }}</span>
        </div>
      </div>
    </TransitionGroup>
  </div>

  <!-- ==================== SIN AVISOS ==================== -->
  <div v-else class="bg-[#ABACAE] rounded-lg p-8 text-center">
    <div
      class="w-20 h-20 bg-[#0A3B76] rounded-full flex items-center justify-center mx-auto mb-4 shadow-md"
    >
      <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
        />
      </svg>
    </div>
    <p class="text-gray-800 font-semibold mb-2">No hay avisos disponibles en este momento</p>
    <p class="text-gray-600 text-sm">Vuelve más tarde para ver nuevas publicaciones</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { avisosAPI } from '@/api/avisos'

// ==================== STATE ====================
const avisos = ref([])
const isLoading = ref(false)
const errorMessage = ref(null)

// ==================== API CALLS ====================
const fetchAvisos = async () => {
  isLoading.value = true
  errorMessage.value = null

  try {
    const response = await avisosAPI.getActivos()

    avisos.value = response.data
    console.log('✅ Avisos activos cargados:', avisos.value.length)
  } catch (error) {
    console.error('❌ Error al cargar avisos:', error)

    if (error.response?.status === 401) {
      errorMessage.value = 'Tu sesión ha expirado. Por favor, inicia sesión nuevamente.'
    } else {
      errorMessage.value = 'No se pudieron cargar los avisos. Intenta recargar la página.'
    }
  } finally {
    isLoading.value = false
  }
}

// ==================== UTILITY FUNCTIONS ====================
const formatDate = (dateString) => {
  const date = new Date(dateString)
  const utcMinus6 = new Date(date.getTime() - 6 * 60 * 60 * 1000)
  return utcMinus6.toLocaleDateString('es-MX', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const isNew = (createdAt) => {
  const created = new Date(createdAt)
  const now = new Date()
  const diffDays = (now - created) / (1000 * 60 * 60 * 24)
  return diffDays <= 7 // Muestra "NUEVO" si tiene menos de 7 días
}

// ==================== LIFECYCLE ====================
onMounted(() => {
  fetchAvisos()
})
</script>

<style scoped>
/* Animaciones para TransitionGroup */
.aviso-move,
.aviso-enter-active,
.aviso-leave-active {
  transition: all 0.3s ease;
}

.aviso-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.aviso-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}

.aviso-leave-active {
  position: absolute;
}
</style>
