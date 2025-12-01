<template>
  <div class="min-h-screen bg-slate-100 flex relative overflow-hidden">
    <!-- Animated Circles -->
    <div class="absolute inset-0 pointer-events-none">
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
          animationDelay: `${index * 0.1}s`,
        }"
      ></div>
    </div>

    <!-- Left Side - Login Form -->
    <div class="w-1/2 flex items-center justify-center p-12 relative z-10">
      <div
        class="w-full max-w-2xl bg-white/10 rounded-3xl p-12 shadow-lg backdrop-blur-md border border-white/20"
      >
        <!-- Back Link -->
        <RouterLink
          to="/"
          :class="[
            'mb-8 text-lg inline-block px-2 py-1 rounded-lg font-bold transition-colors text-white',
            departamentoConfig.buttonColor,
          ]"
        >
          <HomeLogo></HomeLogo>
        </RouterLink>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-8">
          <!-- Título dinámico con ícono -->
          <div class="space-y-2">
            <div class="flex items-center gap-3">
              <div
                :class="[
                  'h-14 w-14 rounded-xl flex items-center justify-center',
                  departamentoConfig.bgColor,
                ]"
              >
                <component
                  :is="departamentoConfig.icon"
                  :class="['h-7 w-7', departamentoConfig.iconColor]"
                ></component>
              </div>
              <div>
                <h1 class="text-3xl font-bold text-slate-800">
                  {{ departamentoConfig.titulo }}
                </h1>
                <p class="text-sm text-slate-600">{{ departamentoConfig.descripcion }}</p>
              </div>
            </div>
          </div>

          <!-- Mostrar mensaje de error -->
          <Transition
            enter-active-class="transition ease-out duration-200"
            enter-from-class="opacity-0 translate-y-1"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition ease-in duration-150"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
          >
            <div
              v-if="errorMessage"
              class="p-3 bg-red-50 border-l-4 border-red-500 rounded text-red-800 text-sm font-medium"
            >
              {{ errorMessage }}
            </div>
          </Transition>

          <div class="space-y-6">
            <div class="space-y-2">
              <label for="usuario" class="block text-lg font-medium text-slate-700">
                Usuario
              </label>
              <input
                id="usuario"
                v-model="usuario"
                type="text"
                required
                class="w-full px-6 py-3 text-lg rounded-lg bg-white/50 border border-white/30 focus:ring-2 focus:border-transparent placeholder-gray-500 transition-all"
                :class="`focus:ring-${departamentoConfig.ringColor}`"
                placeholder="Ingresa tu usuario"
              />
            </div>

            <div class="space-y-2">
              <label for="password" class="block text-lg font-medium text-slate-700">
                Contraseña
              </label>
              <div class="relative">
                <input
                  id="password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  class="w-full px-6 py-3 text-lg rounded-lg bg-white/50 border border-white/30 focus:ring-2 focus:border-transparent placeholder-gray-500 transition-all"
                  :class="`focus:ring-${departamentoConfig.ringColor}`"
                  placeholder="Ingresa tu contraseña"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-4 top-1/2 transform -translate-y-1/2 text-slate-500 text-xl hover:text-slate-700 transition-colors"
                >
                  <span v-if="showPassword">
                    <ShowEye />
                  </span>
                  <span v-else>
                    <HideEye />
                  </span>
                </button>
              </div>
            </div>
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            :class="[
              'w-full text-white rounded-lg px-6 py-3 text-lg font-medium transition-all shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2',
              departamentoConfig.buttonColor,
            ]"
          >
            <svg
              v-if="isLoading"
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
            {{ isLoading ? 'Iniciando sesión...' : 'ENTRAR' }}
          </button>
        </form>

        <!-- Info adicional -->
        <div class="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <div class="flex items-start gap-2">
            <svg
              class="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                clip-rule="evenodd"
              />
            </svg>
            <p class="text-sm text-blue-800">
              Este acceso es exclusivo para el personal del departamento. Si tienes problemas para
              ingresar, contacta al administrador del sistema.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Side - Illustration -->
    <div class="w-1/2 flex items-center justify-center relative z-10 rounded-3xl">
      <div class="relative w-1/2 h-1/2">
        <img
          :src="departamentoConfig.imagen"
          :alt="`Ilustración de ${departamentoConfig.titulo}`"
          class="absolute inset-0 w-full h-full object-contain rounded-3xl z-10"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import HomeLogo from '../components/icons/HomeLogo.vue'
import ShowEye from '@/components/icons/ShowEye.vue'
import HideEye from '@/components/icons/HideEye.vue'
import PsicologiaLogo from '@/components/icons/PsicologiaLogo.vue'
import CienciasLogo from '@/components/icons/CienciasLogo.vue'
import JefaturaLogo from '@/components/icons/JefaturaLogo.vue'
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { RouterLink, useRouter, useRoute } from 'vue-router'

// ==================== ROUTER ====================
const router = useRouter()
const route = useRoute()

// ==================== STATE ====================
const usuario = ref('')
const password = ref('')
const showPassword = ref(false)
const errorMessage = ref('')
const isLoading = ref(false)

// ==================== CONFIGURACIÓN POR DEPARTAMENTO ====================
const departamentosConfig = {
  psicologia: {
    titulo: 'Departamento de Psicología',
    descripcion: 'Área de Desarrollo Estudiantil',
    icon: PsicologiaLogo,
    bgColor: 'bg-teal-100',
    iconColor: 'text-teal-600',
    buttonColor: 'bg-teal-600 hover:bg-teal-700',
    ringColor: 'teal-500',
    imagen: '/EscudoITSF.png', // Puedes cambiar la imagen
    rol: 'psicologia',
    circles: [
      { color: 'bg-teal-300', size: 96, top: 10, left: 5 },
      { color: 'bg-cyan-200', size: 64, top: 20, left: 80 },
      { color: 'bg-teal-400', size: 128, top: 70, left: 20 },
      { color: 'bg-gray-100', size: 80, top: 40, left: 95 },
      { color: 'bg-cyan-300', size: 112, top: 85, left: 70 },
      { color: 'bg-gray-200', size: 48, top: 25, left: 30 },
      { color: 'bg-teal-500', size: 72, top: 60, left: 50 },
      { color: 'bg-cyan-100', size: 56, top: 5, left: 90 },
      { color: 'bg-gray-300', size: 88, top: 80, left: 40 },
      { color: 'bg-teal-200', size: 40, top: 90, left: 10 },
      { color: 'bg-cyan-400', size: 104, top: 15, left: 60 },
      { color: 'bg-gray-100', size: 68, top: 50, left: 85 },
    ],
  },
  ciencias: {
    titulo: 'Departamento de Ciencias Básicas',
    descripcion: 'Coordinación Académica',
    icon: CienciasLogo,
    bgColor: 'bg-indigo-100',
    iconColor: 'text-indigo-600',
    buttonColor: 'bg-indigo-600 hover:bg-indigo-700',
    ringColor: 'indigo-500',
    imagen: '/EscudoITSF.png', // Puedes cambiar la imagen
    rol: 'ciencias_basicas',
    circles: [
      { color: 'bg-indigo-300', size: 96, top: 10, left: 5 },
      { color: 'bg-purple-200', size: 64, top: 20, left: 80 },
      { color: 'bg-indigo-400', size: 128, top: 70, left: 20 },
      { color: 'bg-gray-100', size: 80, top: 40, left: 95 },
      { color: 'bg-purple-300', size: 112, top: 85, left: 70 },
      { color: 'bg-gray-200', size: 48, top: 25, left: 30 },
      { color: 'bg-indigo-500', size: 72, top: 60, left: 50 },
      { color: 'bg-purple-100', size: 56, top: 5, left: 90 },
      { color: 'bg-gray-300', size: 88, top: 80, left: 40 },
      { color: 'bg-indigo-200', size: 40, top: 90, left: 10 },
      { color: 'bg-purple-400', size: 104, top: 15, left: 60 },
      { color: 'bg-gray-100', size: 68, top: 50, left: 85 },
    ],
  },
  jefatura: {
    titulo: 'Jefatura Académica',
    descripcion: 'Coordinación y Supervisión',
    icon: JefaturaLogo,
    bgColor: 'bg-rose-100',
    iconColor: 'text-rose-600',
    buttonColor: 'bg-rose-600 hover:bg-rose-700',
    ringColor: 'rose-500',
    imagen: '/EscudoITSF.png', // Puedes cambiar la imagen
    rol: 'jefatura_academica',
    circles: [
      { color: 'bg-rose-300', size: 96, top: 10, left: 5 },
      { color: 'bg-pink-200', size: 64, top: 20, left: 80 },
      { color: 'bg-rose-400', size: 128, top: 70, left: 20 },
      { color: 'bg-gray-100', size: 80, top: 40, left: 95 },
      { color: 'bg-pink-300', size: 112, top: 85, left: 70 },
      { color: 'bg-gray-200', size: 48, top: 25, left: 30 },
      { color: 'bg-rose-500', size: 72, top: 60, left: 50 },
      { color: 'bg-pink-100', size: 56, top: 5, left: 90 },
      { color: 'bg-gray-300', size: 88, top: 80, left: 40 },
      { color: 'bg-rose-200', size: 40, top: 90, left: 10 },
      { color: 'bg-pink-400', size: 104, top: 15, left: 60 },
      { color: 'bg-gray-100', size: 68, top: 50, left: 85 },
    ],
  },
}

// ==================== COMPUTED ====================
const departamento = computed(() => route.params.departamento)

const departamentoConfig = computed(() => {
  return departamentosConfig[departamento.value] || departamentosConfig.psicologia
})

const circles = computed(() => departamentoConfig.value.circles)

// ==================== VALIDACIÓN ====================
onMounted(() => {
  // Validar que el departamento exista
  if (!departamentosConfig[departamento.value]) {
    console.error('Departamento no válido:', departamento.value)
    router.push('/')
  }
})

// ==================== LOGIN HANDLER ====================
const handleSubmit = async () => {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const formData = new URLSearchParams()
    formData.append('username', usuario.value)
    formData.append('password', password.value)

    const response = await axios.post('http://localhost:8000/api/administradores/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })

    if (response.status === 200 && response.data.access_token) {
      console.log('✅ Inicio de sesión exitoso:', response.data)

      // Validar que el rol coincida con el departamento
      const expectedRol = departamentoConfig.value.rol
      const actualRol = response.data.rol

      if (actualRol !== expectedRol) {
        errorMessage.value = `Este usuario no tiene permisos para acceder a ${departamentoConfig.value.titulo}`
        isLoading.value = false
        return
      }

      // Guardar Token y ROL
      localStorage.setItem('accessToken', response.data.access_token)
      localStorage.setItem('userRole', actualRol)

      // Redirigir a la vista de descargas del departamento
      router.push('/departamento/descargas')
    }
  } catch (error) {
    console.error('❌ Error en la solicitud:', error)
    if (error.response && error.response.data && error.response.data.detail) {
      errorMessage.value = error.response.data.detail
    } else {
      errorMessage.value = 'Error de conexión o credenciales incorrectas.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
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
  animation: float-1 3s ease-in-out infinite;
}

.animate-float-2 {
  animation: float-2 4s ease-in-out infinite;
}

.animate-float-3 {
  animation: float-3 5s ease-in-out infinite;
}
</style>
