<template>
  <div class="min-h-screen bg-slate-50 flex relative overflow-hidden">
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
      <div class="w-full max-w-2xl bg-gray-200/80 rounded-3xl p-12 shadow-lg backdrop-blur-sm">
        <!-- Back Link -->
        <RouterLink
          to="/"
          class="text-white mb-8 text-lg bg-orange-500 inline-block px-2 py-1 rounded-lg font-bold"
        >
          <HomeLogo></HomeLogo>
        </RouterLink>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-8">
          <h1 class="text-4xl font-bold text-gray-800 mb-10">INICIAR SESIÓN</h1>

          <!-- Mostrar mensaje de error -->
          <p v-if="errorMessage" class="text-red-500 text-sm font-medium">
            {{ errorMessage }}
          </p>
          <div class="space-y-6">
            <div class="space-y-2">
              <label for="correo" class="block text-lg font-medium text-gray-700"> Correo </label>
              <input
                id="correo"
                v-model="correo"
                type="email"
                required
                class="w-full px-6 py-3 text-lg rounded-lg bg-white border-0 text-gray-800 placeholder-gray-400 focus:ring-2 focus:ring-coral-400"
                placeholder="Correo electrónico"
              />
            </div>

            <div class="space-y-2">
              <label for="password" class="block text-lg font-medium text-gray-700">
                Contraseña
              </label>
              <div class="relative">
                <input
                  id="password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  class="w-full px-6 py-3 text-lg rounded-lg bg-white border-0 text-gray-800 placeholder-gray-400 focus:ring-2 focus:ring-coral-400"
                  placeholder="Contraseña"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500 text-xl"
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
            class="w-full bg-orange-500 text-white rounded-lg px-6 py-3 text-lg font-medium hover:bg-navy-700 transition-colors"
          >
            ENTRAR
          </button>
        </form>
      </div>
    </div>

    <!-- Right Side - Illustration -->
    <div class="w-1/2 flex items-center justify-center relative z-10">
      <div class="relative w-4/5 h-4/5">
        <div
          class="absolute inset-0 bg-gradient-to-br from-coral-400 to-coral-600 rounded-full opacity-75 blur-2xl"
        ></div>
        <div
          class="absolute inset-4 bg-gradient-to-tr from-navy-400 to-coral-300 rounded-full opacity-75 blur-xl"
        ></div>
        <img
          src="/tutores.png"
          alt="Ilustración de administrador trabajando"
          class="absolute inset-0 w-full h-full object-contain rounded-3xl z-10 animate-float-3"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import HomeLogo from '../components/icons/HomeLogo.vue'
import ShowEye from '@/components/icons/ShowEye.vue'
import HideEye from '@/components/icons/HideEye.vue'
import { useRouter } from 'vue-router' // Para redirigir al dashboard
import axios from 'axios' // Importa Axios para realizar la solicitud HTTP

const correo = ref('')
const password = ref('')
const showPassword = ref(false)

// Estado para manejar errores
const errorMessage = ref('')

// Router para manejar redirección
const router = useRouter()

const handleSubmit = async () => {
  try {
    // 1. Preparamos los datos en el formato 'form-data'
    const formData = new URLSearchParams()
    formData.append('username', correo.value) // El endpoint probablemente espera 'username'
    formData.append('password', password.value)

    // 2. Hacemos la petición POST
    const response = await axios.post('http://localhost:8000/api/tutores/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })

    // 3. Si el login es exitoso, la respuesta contendrá el token
    if (response.status === 200 && response.data.access_token) {
      console.log('Inicio de sesión exitoso:', response.data)

      // 4. Guardamos el TOKEN en localStorage, no los datos del usuario
      localStorage.setItem('accessToken', response.data.access_token)

      // (Opcional) Si necesitas diferenciar el rol
      localStorage.setItem('userRole', 'tutor')

      // (Opcional) Si el backend devuelve datos del tutor, puedes guardarlos
      // if (response.data.tutor) {
      //   localStorage.setItem('tutorData', JSON.stringify(response.data.tutor))
      // }

      router.push('/login_tutor/dashboard')
    }
  } catch (error) {
    console.error('Error en la solicitud:', error)
    if (error.response && error.response.data && error.response.data.detail) {
      errorMessage.value = error.response.data.detail
    } else {
      errorMessage.value = 'Error de conexión o credenciales incorrectas.'
    }
  }
}

// Definimos colores personalizados para los círculos
const circles = [
  { color: 'bg-orange-500', size: 96, top: 10, left: 5 },    // Naranja principal
  { color: 'bg-orange-300', size: 64, top: 20, left: 80 },   // Naranja suave
  { color: 'bg-amber-400', size: 128, top: 70, left: 20 },   // Dorado cálido
  { color: 'bg-amber-100', size: 80, top: 40, left: 95 },     // Gris muy claro
  { color: 'bg-orange-600', size: 112, top: 85, left: 70 },  // Naranja intenso
  { color: 'bg-amber-200', size: 48, top: 25, left: 30 },    // Amarillo crema
  { color: 'bg-orange-400', size: 72, top: 60, left: 50 },   // Naranja medio
  { color: 'bg-amber-200', size: 56, top: 5, left: 90 },      // Gris claro
  { color: 'bg-orange-300', size: 88, top: 80, left: 40 },   // Naranja suave
  { color: 'bg-amber-300', size: 40, top: 90, left: 10 },    // Dorado suave
  { color: 'bg-orange-500', size: 104, top: 15, left: 60 },  // Naranja principal
  { color: 'bg-amber-100', size: 68, top: 50, left: 85 },     // Gris muy claro
];

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

/* Colores personalizados */
.bg-coral-300 {
  background-color: #ffa07a;
}
.bg-coral-400 {
  background-color: #ff7f50;
}
.bg-coral-500 {
  background-color: #ff6347;
}
.bg-coral-600 {
  background-color: #ff4500;
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
.bg-navy-700 {
  background-color: #0f131a;
}

.bg-brown-200 {
  background-color: #bc8f8f;
}
.bg-brown-300 {
  background-color: #a0522d;
}
.bg-brown-400 {
  background-color: #8b4513;
}
</style>
