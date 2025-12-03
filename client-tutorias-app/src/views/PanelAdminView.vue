<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-white relative overflow-hidden">
    <!-- CÍRCULOS ANIMADOS (Azul institucional con opacidades) -->
    <div class="absolute inset-0 pointer-events-none overflow-hidden">
      <div
        v-for="(circle, index) in circles"
        :key="index"
        :class="['absolute rounded-full', circle.color, `animate-float-${(index % 3) + 1}`]"
        :style="{
          top: `${circle.top}%`,
          left: `${circle.left}%`,
          width: `${circle.size}px`,
          height: `${circle.size}px`,
          animationDelay: `${index * 0.2}s`,
        }"
      ></div>
    </div>

    <!-- NAVBAR -->
    <nav class="bg-[#0A3B76] shadow-xl relative z-10 border-b-2 border-[#083060]">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <!-- Left Section -->
          <div class="flex items-center">
            <img
              class="h-12 w-12 border-2 border-white rounded-full shadow-md"
              src="/EscudoITSF.png"
              alt="Escudo ITSF"
            />
            <div class="ml-4">
              <div class="text-lg font-bold text-white">Panel de Administración</div>
              <div class="text-sm text-gray-300">Instituto Tecnológico Superior de Fresnillo</div>
            </div>
          </div>

          <!-- Right Section -->
          <div class="flex items-center">
            <button
              @click="handleLogout"
              class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ease-in-out flex items-center gap-2 shadow-md hover:shadow-lg"
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

    <!-- CONTENIDO -->
    <main class="max-w-[1400px] mx-auto py-6 sm:px-6 lg:px-8 relative z-10">
      <div class="px-4 py-6 sm:px-0">
        <!-- Header -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900 mb-2">Panel de Administración</h1>
          <p class="text-gray-600">Gestiona estudiantes, tutores y configuraciones del sistema</p>
        </div>

        <!-- PESTAÑAS -->
        <div class="mb-8">
          <nav
            class="flex space-x-1 bg-white rounded-lg shadow-sm p-1 border border-gray-200"
            aria-label="Tabs"
          >
            <button
              @click="activeTab = 'students'"
              :class="[
                'flex-1 px-4 py-3 font-medium text-sm rounded-md transition-all duration-200 flex items-center justify-center gap-2',
                activeTab === 'students'
                  ? 'bg-[#0A3B76] text-white shadow-md'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
              ]"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
                />
              </svg>
              Estudiantes
            </button>

            <button
              @click="activeTab = 'tutors'"
              :class="[
                'flex-1 px-4 py-3 font-medium text-sm rounded-md transition-all duration-200 flex items-center justify-center gap-2',
                activeTab === 'tutors'
                  ? 'bg-[#0A3B76] text-white shadow-md'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
              ]"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                />
              </svg>
              Tutores
            </button>

            <button
              @click="activeTab = 'avisos'"
              :class="[
                'flex-1 px-4 py-3 font-medium text-sm rounded-md transition-all duration-200 flex items-center justify-center gap-2',
                activeTab === 'avisos'
                  ? 'bg-[#0A3B76] text-white shadow-md'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
              ]"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                />
              </svg>
              Avisos
            </button>

            <button
              @click="activeTab = 'etapas'"
              :class="[
                'flex-1 px-4 py-3 font-medium text-sm rounded-md transition-all duration-200 flex items-center justify-center gap-2',
                activeTab === 'etapas'
                  ? 'bg-[#0A3B76] text-white shadow-md'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
              ]"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
              Etapas
            </button>

            <button
              @click="activeTab = 'plantillas'"
              :class="[
                'flex-1 px-4 py-3 font-medium text-sm rounded-md transition-all duration-200 flex items-center justify-center gap-2',
                activeTab === 'plantillas'
                  ? 'bg-[#0A3B76] text-white shadow-md'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50',
              ]"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              Plantillas
            </button>
          </nav>
        </div>

        <!-- PANELES -->
        <Transition
          enter-active-class="transition ease-out duration-200"
          enter-from-class="opacity-0 translate-y-4"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition ease-in duration-150"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
          mode="out-in"
        >
          <div v-if="activeTab === 'students'"><GestionAlumnos /></div>
          <div v-else-if="activeTab === 'tutors'"><GestionTutores /></div>
          <div v-else-if="activeTab === 'avisos'"><GestionAvisos /></div>
          <div v-else-if="activeTab === 'etapas'"><ConfiguracionEtapas /></div>
          <div v-else-if="activeTab === 'plantillas'"><GestionPlantillas /></div>
        </Transition>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import GestionAlumnos from '@/components/admin/GestionAlumnos.vue'
import GestionTutores from '@/components/admin/GestionTutores.vue'
import GestionAvisos from '@/components/admin/GestionAvisos.vue'
import ConfiguracionEtapas from '@/components/admin/ConfiguracionEtapas.vue'
import GestionPlantillas from '@/components/admin/GestionPlantillas.vue'

const router = useRouter()
const activeTab = ref('students')

// Círculos azul institucional con opacidades graduales
const circles = [
  { color: 'bg-[#0A3B76]/20', size: 120, top: 5, left: 5 },
  { color: 'bg-[#0A3B76]/15', size: 80, top: 20, left: 85 },
  { color: 'bg-[#0A3B76]/10', size: 150, top: 70, left: 15 },
  { color: 'bg-[#0A3B76]/8', size: 100, top: 40, left: 90 },
  { color: 'bg-[#0A3B76]/12', size: 130, top: 85, left: 65 },
]

const handleLogout = () => {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('admin')
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
