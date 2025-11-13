<template>
  <!-- Modal de Cambio de Contraseña -->
  <Transition
    enter-active-class="transition ease-out duration-300"
    enter-from-class="opacity-0 scale-95"
    enter-to-class="opacity-100 scale-100"
    leave-active-class="transition ease-in duration-200"
    leave-from-class="opacity-100 scale-100"
    leave-to-class="opacity-0 scale-95"
  >
    <div
      v-if="show"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
    >
      <div
        class="relative top-20 mx-auto p-5 border w-11/12 max-w-md shadow-lg rounded-md bg-white"
      >
        <div class="flex justify-between items-center mb-4 border-b pb-3">
          <h2 class="text-xl font-semibold text-gray-900">Cambiar Contraseña</h2>
          <button
            @click="cerrarModal"
            :disabled="isChangingPassword"
            class="text-gray-500 hover:text-gray-700 disabled:opacity-50"
          >
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        <!-- Mensaje de advertencia para primera vez -->
        <div
          v-if="requiresPasswordChange"
          class="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md"
        >
          <p class="text-sm text-yellow-800">
            <strong>Importante:</strong> Esta es tu primera vez cambiando la contraseña. Por favor,
            elige una contraseña segura.
          </p>
        </div>

        <!-- Mensaje de éxito -->
        <Transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="opacity-0 translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition ease-in duration-150"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <div
            v-if="passwordChangeSuccess"
            class="mb-4 p-3 bg-green-50 border-l-4 border-green-400 rounded-md"
          >
            <div class="flex items-center">
              <svg
                class="w-5 h-5 text-green-400 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M5 13l4 4L19 7"
                />
              </svg>
              <p class="text-sm text-green-800 font-medium">¡Contraseña cambiada exitosamente!</p>
            </div>
          </div>
        </Transition>

        <!-- Mensaje de error -->
        <Transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="opacity-0 translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition ease-in duration-150"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <div
            v-if="passwordChangeError"
            class="mb-4 p-3 bg-red-50 border-l-4 border-red-400 rounded-md"
          >
            <div class="flex items-start">
              <svg
                class="w-5 h-5 text-red-400 mr-2 flex-shrink-0 mt-0.5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <p class="text-sm text-red-800">{{ passwordChangeError }}</p>
            </div>
          </div>
        </Transition>

        <!-- Formulario -->
        <form @submit.prevent="handleChangePassword" class="space-y-4">
          <!-- Campo de Correo (solo para primera vez) -->
          <div v-if="requiresPasswordChange">
            <label for="correo" class="block text-sm font-medium text-gray-700 mb-1">
              Correo Electrónico
            </label>
            <input
              id="correo"
              v-model="passwordFormInternal.correo"
              type="email"
              required
              :disabled="isChangingPassword"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
              placeholder="tu.correo@example.com"
            />
          </div>

          <!-- Contraseña Actual -->
          <div>
            <label for="current-password" class="block text-sm font-medium text-gray-700 mb-1">
              Contraseña Actual
            </label>
            <div class="relative">
              <input
                id="current-password"
                v-model="passwordFormInternal.currentPassword"
                :type="showCurrentPassword ? 'text' : 'password'"
                required
                :disabled="isChangingPassword"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                placeholder="- - - - - - - - "
              />
              <button
                type="button"
                @click="showCurrentPassword = !showCurrentPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
              >
                <svg
                  v-if="!showCurrentPassword"
                  class="h-5 w-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                  />
                </svg>
                <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                  />
                </svg>
              </button>
            </div>
          </div>

          <!-- Nueva Contraseña -->
          <div>
            <label for="new-password" class="block text-sm font-medium text-gray-700 mb-1">
              Nueva Contraseña
            </label>
            <div class="relative">
              <input
                id="new-password"
                v-model="passwordFormInternal.newPassword"
                :type="showNewPassword ? 'text' : 'password'"
                required
                minlength="8"
                :disabled="isChangingPassword"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                placeholder="- - - - - - - - "
              />
              <button
                type="button"
                @click="showNewPassword = !showNewPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
              >
                <svg
                  v-if="!showNewPassword"
                  class="h-5 w-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                  />
                </svg>
                <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                  />
                </svg>
              </button>
            </div>
            <p class="mt-1 text-xs text-gray-500">Mínimo 8 caracteres</p>
          </div>

          <!-- Confirmar Nueva Contraseña -->
          <div>
            <label for="confirm-password" class="block text-sm font-medium text-gray-700 mb-1">
              Confirmar Nueva Contraseña
            </label>
            <div class="relative">
              <input
                id="confirm-password"
                v-model="passwordFormInternal.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                required
                minlength="8"
                :disabled="isChangingPassword"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                placeholder="- - - - - - - - "
              />
              <button
                type="button"
                @click="showConfirmPassword = !showConfirmPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
              >
                <svg
                  v-if="!showConfirmPassword"
                  class="h-5 w-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                  />
                </svg>
                <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                  />
                </svg>
              </button>
            </div>
          </div>

          <!-- Botones -->
          <div class="flex gap-3 pt-4">
            <button
              type="button"
              @click="cerrarModal"
              :disabled="isChangingPassword"
              class="flex-1 px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Cancelar
            </button>
            <button
              type="submit"
              :disabled="isChangingPassword"
              class="flex-1 px-4 py-2 bg-blue-600 border border-transparent rounded-md text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors inline-flex justify-center items-center"
            >
              <svg
                v-if="isChangingPassword"
                class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
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
              {{ isChangingPassword ? 'Cambiando...' : 'Cambiar Contraseña' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'

// ==================== PROPS ====================
const props = defineProps({
  show: {
    type: Boolean,
    required: true,
  },
  userType: {
    type: String,
    required: true,
    validator: (value) => ['tutor', 'alumno'].includes(value),
  },
  requiresPasswordChange: {
    type: Boolean,
    default: false,
  },
  currentEmail: {
    type: String,
    default: '',
  },
})

// ==================== EMITS ====================
const emit = defineEmits(['close', 'success'])

// ==================== STATE ====================
const passwordFormInternal = ref({
  correo: '',
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})

const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)
const isChangingPassword = ref(false)
const passwordChangeError = ref(null)
const passwordChangeSuccess = ref(false)

// ==================== WATCHERS ====================
watch(
  () => props.show,
  (newVal) => {
    if (newVal) {
      // Reset form cuando se abre el modal
      passwordFormInternal.value = {
        correo: props.currentEmail,
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
      }
      showCurrentPassword.value = false
      showNewPassword.value = false
      showConfirmPassword.value = false
      passwordChangeError.value = null
      passwordChangeSuccess.value = false
    }
  },
)

// ==================== METHODS ====================
const handleChangePassword = async () => {
  passwordChangeError.value = null
  passwordChangeSuccess.value = false

  // Validaciones
  if (passwordFormInternal.value.newPassword !== passwordFormInternal.value.confirmPassword) {
    passwordChangeError.value = 'Las contraseñas no coinciden.'
    return
  }

  if (passwordFormInternal.value.newPassword.length < 8) {
    passwordChangeError.value = 'La nueva contraseña debe tener al menos 8 caracteres.'
    return
  }

  if (props.requiresPasswordChange && !passwordFormInternal.value.correo) {
    passwordChangeError.value = 'El correo es requerido.'
    return
  }

  isChangingPassword.value = true

  try {
    const token = localStorage.getItem('accessToken')

    // Determinar endpoint según tipo de usuario y si es primera vez
    let endpoint = ''
    let requestData = {}

    if (props.requiresPasswordChange) {
      // Primera vez - sin token
      endpoint = `http://localhost:8000/api/${props.userType === 'tutor' ? 'tutores' : 'alumnos'}/set-password`
      requestData = {
        correo: passwordFormInternal.value.correo,
        contraseña_actual: passwordFormInternal.value.currentPassword,
        nueva_contraseña: passwordFormInternal.value.newPassword,
      }
    } else {
      // Cambio normal - con token
      endpoint = `http://localhost:8000/api/${props.userType === 'tutor' ? 'tutores' : 'alumnos'}/change-password`
      requestData = {
        contraseña_actual: passwordFormInternal.value.currentPassword,
        nueva_contraseña: passwordFormInternal.value.newPassword,
      }
    }

    const config = props.requiresPasswordChange
      ? {}
      : {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }

    const response = props.requiresPasswordChange
      ? await axios.post(endpoint, requestData)
      : await axios.put(endpoint, requestData, config)

    if (response.status === 200) {
      passwordChangeSuccess.value = true

      setTimeout(() => {
        cerrarModal()
        emit('success')
      }, 2000)
    }
  } catch (err) {
    console.error('Error al cambiar la contraseña:', err)

    if (err.response?.data?.detail) {
      passwordChangeError.value = err.response.data.detail
    } else if (err.response?.status === 400) {
      passwordChangeError.value = 'Contraseña actual incorrecta.'
    } else if (err.response?.status === 401) {
      passwordChangeError.value = 'No tienes autorización para realizar esta acción.'
    } else {
      passwordChangeError.value = 'Error al cambiar la contraseña. Intenta de nuevo.'
    }
  } finally {
    isChangingPassword.value = false
  }
}

const cerrarModal = () => {
  if (!isChangingPassword.value) {
    emit('close')
  }
}
</script>
