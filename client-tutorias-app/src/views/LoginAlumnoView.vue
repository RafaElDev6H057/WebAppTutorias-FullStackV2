<template>
  <div class="min-h-screen bg-gray-900 flex relative overflow-hidden">
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
      <div class="w-full max-w-2xl bg-gray-800/50 rounded-3xl p-12 shadow-lg backdrop-blur-sm">
        <!-- Back Link -->
        <RouterLink
          to="/"
          class="text-white mb-8 text-lg bg-purple-600 inline-block px-2 py-1 rounded-lg font-bold"
        >
          <HomeLogo></HomeLogo>
        </RouterLink>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-8">
          <h1 class="text-4xl font-bold text-white mb-10">INICIAR SESIÓN</h1>

          <!-- Mostrar mensaje de error -->
          <p v-if="errorMessage" class="text-red-500 text-sm font-medium">
            {{ errorMessage }}
          </p>

          <div class="space-y-6">
            <div class="space-y-2">
              <label for="usuario" class="block text-lg font-medium text-gray-300">
                Num. de Control
              </label>
              <input
                id="usuario"
                v-model="usuario"
                type="text"
                required
                class="w-full px-6 py-3 text-lg rounded-lg bg-gray-700 border-0 text-white placeholder-gray-400 focus:ring-2 focus:ring-purple-500"
                placeholder="Número de Control"
              />
            </div>

            <div class="space-y-2">
              <label for="password" class="block text-lg font-medium text-gray-300">
                Contraseña
              </label>
              <div class="relative">
                <input
                  id="password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  class="w-full px-6 py-3 text-lg rounded-lg bg-gray-700 border-0 text-white placeholder-gray-400 focus:ring-2 focus:ring-purple-500"
                  placeholder="Contraseña"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 text-xl"
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
            class="w-full bg-purple-600 text-white rounded-lg px-6 py-3 text-lg font-medium hover:bg-purple-700 transition-colors"
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
          class="absolute inset-0 bg-gradient-to-br from-purple-600 to-purple-900 rounded-full opacity-20 blur-2xl"
        ></div>
        <div
          class="absolute inset-4 bg-gradient-to-tr from-purple-400 to-purple-600 rounded-full opacity-20 blur-xl"
        ></div>
        <img
          src="/login_alumno-removebg.png"
          alt="Ilustración de tutor trabajando"
          class="absolute inset-0 w-full h-full object-contain rounded-3xl z-10 animate-float-1"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import HomeLogo from '@/components/icons/HomeLogo.vue'
import ShowEye from '@/components/icons/ShowEye.vue'
import HideEye from '@/components/icons/HideEye.vue'
import { ref } from 'vue'
import axios from 'axios' // Importa Axios para realizar la solicitud HTTP
import { useRouter } from 'vue-router' // Para redirigir al dashboard

// Estados del formulario
const usuario = ref('')
const password = ref('')
const showPassword = ref(false)

// Estado para manejar errores
const errorMessage = ref('')

// Router para manejar redirección
const router = useRouter()

// Lógica del inicio de sesión
const handleSubmit = async () => {
  try {
    // 1. Preparamos los datos en el formato 'form-data'
    const formData = new URLSearchParams()
    formData.append('username', usuario.value)
    formData.append('password', password.value)

    // 2. Hacemos la petición POST
    const response = await axios.post('http://localhost:8000/api/alumnos/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })

    // 3. Si el login es exitoso, la respuesta contendrá el token
    if (response.status === 200 && response.data.access_token) {
      console.log('Inicio de sesión exitoso:', response.data)

      // 4. Guardamos el TOKEN en localStorage, no los datos del usuario
      localStorage.setItem('accessToken', response.data.access_token)

      // (Opcional) Puedes guardar otros datos si los necesitas, pero el token es lo crucial
      localStorage.setItem('userRole', 'alumno')

      router.push('/login_alumno/dashboard')
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
// const handleSubmit = async () => {
//   try {
//     // Llama al endpoint de login en el backend

//     const response = await axios.post('http://localhost:8000/api/alumnos/login', {
//       num_control: usuario.value,
//       contraseña: password.value,
//     })

//     // Verifica si la respuesta fue exitosa
//     if (response.status === 200) {
//       // console.log('Inicio de sesión exitoso:', response.data)

//       // Opcional: guarda el token o datos del usuario en el almacenamiento local
//       localStorage.setItem('alumno', JSON.stringify(response.data))

//       // Redirige al dashboard
//       router.push('/login_alumno/dashboard')
//     } else {
//       // Maneja errores como credenciales inválidas
//       errorMessage.value = response.data.message || 'Credenciales incorrectas'
//     }
//   } catch (error) {
//     // console.error('Error en la solicitud:', error.response.data.message)
//     errorMessage.value = error.response.data.message || 'Credenciales incorrectas'
//   }
// }

const circles = [
  { color: 'bg-purple-600', size: 96, top: 10, left: 5 },
  { color: 'bg-purple-300', size: 64, top: 20, left: 80 },
  { color: 'bg-purple-500', size: 128, top: 70, left: 20 },
  { color: 'bg-white', size: 80, top: 40, left: 95 },
  { color: 'bg-purple-400', size: 112, top: 85, left: 70 },
  { color: 'bg-purple-200', size: 48, top: 25, left: 30 },
  { color: 'bg-purple-700', size: 72, top: 60, left: 50 },
  { color: 'bg-purple-100', size: 56, top: 5, left: 90 },
  { color: 'bg-purple-800', size: 88, top: 80, left: 40 },
  { color: 'bg-white', size: 40, top: 90, left: 10 },
  { color: 'bg-purple-500', size: 104, top: 15, left: 60 },
  { color: 'bg-purple-300', size: 68, top: 50, left: 85 },
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
