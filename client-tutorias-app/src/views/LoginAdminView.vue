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

    <!-- Login Form - Responsive -->
    <div class="w-full lg:w-1/2 flex items-center justify-center p-4 sm:p-8 lg:p-12 relative z-10">
      <div
        class="w-full max-w-md lg:max-w-2xl bg-white/10 rounded-3xl p-6 sm:p-8 lg:p-12 shadow-lg backdrop-blur-md border border-white/20"
      >
        <!-- Back Link -->
        <RouterLink
          to="/"
          class="text-white mb-6 sm:mb-8 text-base sm:text-lg bg-[#0A3B76] inline-block px-2 py-1 rounded-lg font-bold hover:bg-[#082f5c] transition-colors"
        >
          <HomeLogo></HomeLogo>
        </RouterLink>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-6 sm:space-y-8">
          <!-- Título con ícono -->
          <div class="space-y-2">
            <div class="flex items-center gap-3 mb-4">
              <div
                class="h-12 w-12 sm:h-14 sm:w-14 bg-[#ABACAE] rounded-xl flex items-center justify-center"
              >
                <svg
                  class="w-6 h-6 sm:w-7 sm:h-7 text-[#0A3B76]"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                  />
                </svg>
              </div>
              <div>
                <h1 class="text-2xl sm:text-3xl font-bold text-slate-800">Administrador</h1>
                <p class="text-xs sm:text-sm text-slate-600">Panel de control del sistema</p>
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
              class="p-3 bg-red-50 border-l-4 border-red-500 rounded text-red-800 text-xs sm:text-sm font-medium"
            >
              {{ errorMessage }}
            </div>
          </Transition>

          <div class="space-y-4 sm:space-y-6">
            <div class="space-y-2">
              <label for="usuario" class="block text-base sm:text-lg font-medium text-slate-700">
                Usuario
              </label>
              <input
                id="usuario"
                v-model="usuario"
                type="text"
                required
                class="w-full px-4 sm:px-6 py-2.5 sm:py-3 text-base sm:text-lg rounded-lg bg-white/50 border border-white/30 focus:ring-2 focus:ring-[#0A3B76] focus:border-[#0A3B76] placeholder-gray-500 transition-all"
                placeholder="Ingresa tu usuario"
              />
            </div>

            <div class="space-y-2">
              <label for="password" class="block text-base sm:text-lg font-medium text-slate-700">
                Contraseña
              </label>
              <div class="relative">
                <input
                  id="password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  class="w-full px-4 sm:px-6 py-2.5 sm:py-3 text-base sm:text-lg rounded-lg bg-white/50 border border-white/30 focus:ring-2 focus:ring-[#0A3B76] focus:border-[#0A3B76] placeholder-gray-500 transition-all"
                  placeholder="Ingresa tu contraseña"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-3 sm:right-4 top-1/2 transform -translate-y-1/2 text-slate-500 text-lg sm:text-xl hover:text-slate-700 transition-colors"
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
            class="w-full bg-[#0A3B76] text-white rounded-lg px-4 sm:px-6 py-2.5 sm:py-3 text-base sm:text-lg font-medium hover:bg-[#082f5c] transition-all shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
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
        <div class="mt-4 sm:mt-6 p-3 sm:p-4 bg-[#ABACAE]/20 rounded-lg border border-[#ABACAE]">
          <div class="flex items-start gap-2">
            <svg
              class="w-4 h-4 sm:w-5 sm:h-5 text-[#0A3B76] flex-shrink-0 mt-0.5"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                clip-rule="evenodd"
              />
            </svg>
            <p class="text-xs sm:text-sm text-[#0A3B76]">
              Este acceso es exclusivo para el Super Administrador del sistema. Si eres parte de un
              departamento, utiliza el acceso correspondiente desde la página principal.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Side - Illustration (Hidden on mobile) -->
    <div class="hidden lg:flex lg:w-1/2 items-center justify-center relative z-10 rounded-3xl">
      <div class="relative w-4/5 h-4/5">
        <img
          src="/admin2.png"
          alt="Ilustración de espacio de trabajo"
          class="absolute inset-0 w-full h-full object-contain rounded-3xl z-10 animate-float-3"
        />
      </div>
    </div>
  </div>
</template>


<script setup>
import HomeLogo from '../components/icons/HomeLogo.vue'
import ShowEye from '@/components/icons/ShowEye.vue'
import HideEye from '@/components/icons/HideEye.vue'
import { ref } from 'vue'
import axios from 'axios'
import { RouterLink, useRouter } from 'vue-router'

// ==================== STATE ====================
const usuario = ref('')
const password = ref('')
const showPassword = ref(false)
const errorMessage = ref('')
const isLoading = ref(false)
const router = useRouter()

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

      const userRole = response.data.rol

      // ==================== VALIDACIÓN: SOLO SUPER_ADMIN ====================
      if (userRole !== 'super_admin') {
        errorMessage.value =
          '⚠️ Este login es solo para Super Administradores. Si eres de un departamento, usa el acceso departamental.'
        isLoading.value = false
        return
      }

      // Guardar Token y ROL
      localStorage.setItem('accessToken', response.data.access_token)
      localStorage.setItem('userRole', userRole)

      // Redirigir al dashboard de admin
      router.push('/admin/dashboard')
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

// ==================== ANIMATED CIRCLES ====================
const circles = [
  { color: 'bg-[#ABACAE]', size: 96, top: 10, left: 5 },
  { color: 'bg-[#ABACAE]', size: 64, top: 20, left: 80 },
  { color: 'bg-[#0A3B76]', size: 128, top: 70, left: 20 },
  { color: 'bg-[#ABACAE]', size: 80, top: 40, left: 95 },
  { color: 'bg-[#ABACAE]', size: 112, top: 85, left: 70 },
  { color: 'bg-[#ABACAE]', size: 48, top: 25, left: 30 },
  { color: 'bg-[#0A3B76]', size: 72, top: 60, left: 50 },
  { color: 'bg-[#ABACAE]', size: 56, top: 5, left: 90 },
  { color: 'bg-[#ABACAE]', size: 88, top: 80, left: 40 },
  { color: 'bg-[#ABACAE]', size: 40, top: 90, left: 10 },
  { color: 'bg-[#0A3B76]', size: 104, top: 15, left: 60 },
  { color: 'bg-[#ABACAE]', size: 68, top: 50, left: 85 },
]
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
