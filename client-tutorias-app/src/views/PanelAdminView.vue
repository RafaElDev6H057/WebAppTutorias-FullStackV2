<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-white relative overflow-hidden">

    <!-- CÍRCULOS ANIMADOS -->
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

    <!-- NAVBAR -->
    <nav class="bg-[#0A3B76] shadow-lg relative z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <img
              class="h-12 w-12 border-2 border-white rounded-full"
              src="/EscudoITSF.png"
              alt="Escudo ITSF"
            />
            <div class="ml-4">
              <div class="text-lg font-medium text-white">Administrador</div>
              <div class="text-sm text-[#ABACAE]">
                Instituto Tecnológico Superior de Fresnillo
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

    <!-- CONTENIDO -->
    <main class="max-w-[1400px] mx-auto py-6 sm:px-6 lg:px-8 relative z-10">
      <div class="px-4 py-6 sm:px-0">
        <h1 class="text-3xl font-bold text-gray-900 mb-6">Panel de Administración</h1>

        <!-- PESTAÑAS -->
        <div class="mb-8">
          <nav class="flex space-x-2 border-b border-gray-200" aria-label="Tabs">
            <button
              @click="activeTab = 'students'"
              :class="[
                'px-4 py-3 font-medium text-sm rounded-t-lg transition-colors duration-200',
                activeTab === 'students'
                  ? 'bg-blue-50 text-[#0A3B76] border-b-2 border-[#0A3B76]'
                  : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50',
              ]"
            >
              👨‍🎓 Estudiantes
            </button>

            <button
              @click="activeTab = 'tutors'"
              :class="[
                'px-4 py-3 font-medium text-sm rounded-t-lg transition-colors duration-200',
                activeTab === 'tutors'
                  ? 'bg-blue-50 text-[#0A3B76] border-b-2 border-[#0A3B76]'
                  : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50',
              ]"
            >
              👨‍🏫 Tutores
            </button>

            <button
              @click="activeTab = 'avisos'"
              :class="[
                'px-4 py-3 font-medium text-sm rounded-t-lg transition-colors duration-200',
                activeTab === 'avisos'
                  ? 'bg-blue-50 text-[#0A3B76] border-b-2 border-[#0A3B76]'
                  : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50',
              ]"
            >
              📢 Avisos
            </button>

            <button
              @click="activeTab = 'etapas'"
              :class="[
                'px-4 py-3 font-medium text-sm rounded-t-lg transition-colors duration-200',
                activeTab === 'etapas'
                  ? 'bg-blue-50 text-[#0A3B76] border-b-2 border-[#0A3B76]'
                  : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50',
              ]"
            >
              ⚙️ Etapas
            </button>

            <button
              @click="activeTab = 'plantillas'"
              :class="[
                'px-4 py-3 font-medium text-sm rounded-t-lg transition-colors duration-200',
                activeTab === 'plantillas'
                  ? 'bg-blue-50 text-[#0A3B76] border-b-2 border-[#0A3B76]'
                  : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50',
              ]"
            >
              📄 Plantillas
            </button>
          </nav>
        </div>

        <!-- PANELES -->
        <div v-if="activeTab === 'students'"><GestionAlumnos /></div>
        <div v-if="activeTab === 'tutors'"><GestionTutores /></div>
        <div v-if="activeTab === 'avisos'"><GestionAvisos /></div>
        <div v-if="activeTab === 'etapas'"><ConfiguracionEtapas /></div>
        <div v-if="activeTab === 'plantillas'"><GestionPlantillas /></div>
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

// Círculos actualizados a azul institucional
const circles = [
  { color: 'bg-[#0A3B76]', size: 120, top: 5, left: 5 },
  { color: 'bg-[#0A3B76]/80', size: 80, top: 20, left: 80 },
  { color: 'bg-[#0A3B76]/60', size: 150, top: 70, left: 20 },
  { color: 'bg-[#0A3B76]/50', size: 100, top: 40, left: 95 },
  { color: 'bg-[#0A3B76]/70', size: 130, top: 85, left: 70 },
]

const handleLogout = () => {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('admin')
  router.push('/')
}
</script>

<style scoped>
@keyframes float-1 {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(5deg); }
}

@keyframes float-2 {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-30px) rotate(-5deg); }
}

@keyframes float-3 {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-25px) rotate(3deg); }
}

.animate-float-1 { animation: float-1 6s ease-in-out infinite; }
.animate-float-2 { animation: float-2 8s ease-in-out infinite; }
.animate-float-3 { animation: float-3 7s ease-in-out infinite; }
</style>
