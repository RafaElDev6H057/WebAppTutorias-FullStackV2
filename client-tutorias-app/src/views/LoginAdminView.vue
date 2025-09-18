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
          class="text-white mb-8 text-lg bg-blue-600 inline-block px-2 py-1 rounded-lg font-bold hover:bg-blue-700 transition-colors"
        >
          <HomeLogo></HomeLogo>
        </RouterLink>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-8">
          <h1 class="text-4xl font-bold text-slate-800 mb-10">INICIAR SESIÓN</h1>

          <!-- Mostrar mensaje de error -->
          <p v-if="errorMessage" class="text-red-500 text-sm font-medium">
            {{ errorMessage }}
          </p>

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
                class="w-full px-6 py-3 text-lg rounded-lg bg-white/50 border border-white/30 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 placeholder-gray-500"
                placeholder="Usuario"
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
                  class="w-full px-6 py-3 text-lg rounded-lg bg-white/50 border border-white/30 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 placeholder-gray-500"
                  placeholder="Contraseña"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-4 top-1/2 transform -translate-y-1/2 text-slate-500 text-xl"
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
            class="w-full bg-blue-600 text-white rounded-lg px-6 py-3 text-lg font-medium hover:bg-blue-700 transition-colors shadow-md hover:shadow-lg"
          >
            ENTRAR
          </button>
        </form>
      </div>
    </div>

    <!-- Right Side - Illustration -->
    <div class="w-1/2 flex items-center justify-center relative z-10 rounded-3xl">
      <div class="relative w-4/5 h-4/5">
        <div
          class="absolute inset-0 bg-gradient-to-br from-blue-500 to-slate-700 rounded-full opacity-55 blur-2xl"
        ></div>
        <div
          class="absolute inset-4 bg-gradient-to-tr from-blue-600 to-slate-800 rounded-full opacity-55 blur-xl"
        ></div>
        <img
          src="/admin_image_login.png"
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

const usuario = ref('')
const password = ref('')
const showPassword = ref(false)
const errorMessage = ref('')
const router = useRouter()

const handleSubmit = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/administradores/login', {
      usuario: usuario.value,
      contraseña: password.value,
    })

    if (response.status === 200) {
      console.log('Inicio de sesión exitoso:', response.data)
      localStorage.setItem('administrador', JSON.stringify(response.data))
      router.push('/login_admin/dashboard')
    } else {
      errorMessage.value = response.data.message || 'Credenciales incorrectas'
    }
  } catch (error) {
    console.error('Error en la solicitud:', error)
    errorMessage.value = 'Credenciales incorrectas.'
  }
}

const circles = [
  { color: 'bg-blue-500', size: 96, top: 10, left: 5 },
  { color: 'bg-slate-200', size: 64, top: 20, left: 80 },
  { color: 'bg-blue-600', size: 128, top: 70, left: 20 },
  { color: 'bg-slate-300', size: 80, top: 40, left: 95 },
  { color: 'bg-blue-500', size: 112, top: 85, left: 70 },
  { color: 'bg-slate-200', size: 48, top: 25, left: 30 },
  { color: 'bg-blue-600', size: 72, top: 60, left: 50 },
  { color: 'bg-slate-300', size: 56, top: 5, left: 90 },
  { color: 'bg-blue-500', size: 88, top: 80, left: 40 },
  { color: 'bg-slate-200', size: 40, top: 90, left: 10 },
  { color: 'bg-blue-600', size: 104, top: 15, left: 60 },
  { color: 'bg-slate-300', size: 68, top: 50, left: 85 },
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
