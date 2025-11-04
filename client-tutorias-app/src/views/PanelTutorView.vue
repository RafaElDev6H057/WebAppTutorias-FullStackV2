<template>
  <div class="min-h-screen bg-gray-100 relative overflow-hidden">
    <!-- Animated Circles -->
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

    <!-- Dashboard content -->
    <div class="relative z-10">
      <!-- Barra de navegación -->
      <nav class="bg-white shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between h-16">
            <div class="flex items-center">
              <img
                class="h-12 w-12 border-2 border-white"
                src="/EscudoITSF.png"
                alt="Escudo ITSF"
              />
              <div class="ml-4">
                <div class="text-lg font-medium text-gray-900">
                  {{
                    tutor?.nombre + ' ' + tutor?.apellido_p + ' ' + tutor?.apellido_m ||
                    'Nombre no disponible'
                  }}
                </div>
                <div class="text-sm text-gray-500">{{ tutor?.correo }}</div>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <button
                @click="openChangePasswordModal"
                class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Cambiar Contraseña
              </button>
              <button
                @click="descargarPDFReporteIntegral"
                :disabled="loading || !studentsData.length"
                class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed inline-flex items-center gap-2"
              >
                <svg
                  v-if="loading"
                  class="animate-spin h-4 w-4"
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
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
                {{ loading ? 'Generando...' : 'Descargar PDF' }}
              </button>
              <button
                @click="handleLogout"
                class="bg-coral-500 hover:bg-coral-600 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </nav>

      <!-- Contenido principal -->
      <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <!-- Banner de Advertencia de Contraseña Insegura -->
        <Transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="opacity-0 translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <div
            v-if="tutor?.requires_password_change"
            class="mx-4 mb-6 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded-md"
          >
            <div class="flex items-start">
              <svg
                class="w-6 h-6 text-yellow-400 mr-3 flex-shrink-0"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
              <div class="flex-1">
                <h3 class="text-sm font-medium text-yellow-800">Contraseña Insegura</h3>
                <p class="mt-1 text-sm text-yellow-700">
                  Tu contraseña actual no está protegida adecuadamente. Por seguridad, te
                  recomendamos cambiarla lo antes posible.
                </p>
                <button
                  @click="openChangePasswordModal"
                  class="mt-3 text-sm font-medium text-yellow-800 hover:text-yellow-900 underline"
                >
                  Cambiar contraseña ahora →
                </button>
              </div>
            </div>
          </div>
        </Transition>

        <!-- Encabezado y búsqueda -->
        <div
          class="px-4 py-6 sm:px-0 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-x-6"
        >
          <div class="flex items-center justify-between w-full mb-4 sm:mb-0 gap-4">
            <h1 class="text-3xl font-bold text-gray-900">Dashboard del Tutor</h1>
            <button
              @click="abrirModalCrear"
              class="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-md font-medium inline-flex items-center gap-2 transition-colors shadow-md hover:shadow-lg"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 4v16m8-8H4"
                />
              </svg>
              Crear Tutoría
            </button>
          </div>
          <button
            @click="openReporteIntegralMasivo"
            class="w-44 px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition-colors font-medium"
          >
            Reporte Integral
          </button>
          <button
            @click="mostrarModalPrimerReporte = true"
            class="w-44 px-4 py-2 bg-coral-600 text-white rounded-md hover:bg-orange-600 transition-colors font-medium"
          >
            1° Reporte
          </button>
          <button
            @click="mostrarModalSegundoReporte = true"
            class="w-44 px-4 py-2 bg-coral-600 text-white rounded-md hover:bg-orange-600 transition-colors font-medium"
          >
            2° Reporte
          </button>
          <div class="w-full sm:w-64">
            <BaseSearchInput
              v-model="searchQuery"
              :disabled="loading"
              placeholder="Buscar estudiante..."
            />
          </div>
        </div>

        <!-- Mensaje de Error -->
        <Transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="opacity-0 translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <div
            v-if="error"
            class="mx-4 mb-4 p-4 bg-red-50 border-l-4 border-red-500 rounded-md flex items-start"
          >
            <svg
              class="w-5 h-5 text-red-500 mr-3 flex-shrink-0 mt-0.5"
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
            <div class="flex-1">
              <p class="text-sm font-medium text-red-800">{{ error }}</p>
            </div>
            <button @click="error = null" class="text-red-500 hover:text-red-700 ml-4">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </Transition>

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
            v-if="showChangePasswordModal"
            class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
          >
            <div
              class="relative top-20 mx-auto p-5 border w-11/12 max-w-md shadow-lg rounded-md bg-white"
            >
              <div class="flex justify-between items-center mb-4 border-b pb-3">
                <h2 class="text-xl font-semibold text-gray-900">Cambiar Contraseña</h2>
                <button
                  @click="closeChangePasswordModal"
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
                v-if="tutor?.requires_password_change"
                class="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md"
              >
                <p class="text-sm text-yellow-800">
                  <strong>Importante:</strong> Esta es tu primera vez cambiando la contraseña. Por
                  favor, elige una contraseña segura.
                </p>
              </div>

              <!-- Mensaje de éxito -->
              <Transition
                enter-active-class="transition ease-out duration-300"
                enter-from-class="opacity-0 translate-y-2"
                enter-to-class="opacity-100 translate-y-0"
                leave-active-class="transition ease-in duration-200"
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
                    <p class="text-sm text-green-800 font-medium">
                      ¡Contraseña cambiada exitosamente!
                    </p>
                  </div>
                </div>
              </Transition>

              <!-- Mensaje de error -->
              <Transition
                enter-active-class="transition ease-out duration-300"
                enter-from-class="opacity-0 translate-y-2"
                enter-to-class="opacity-100 translate-y-0"
                leave-active-class="transition ease-in duration-200"
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
                <div v-if="tutor?.requires_password_change">
                  <label for="correo" class="block text-sm font-medium text-gray-700 mb-1">
                    Correo Electrónico
                  </label>
                  <input
                    id="correo"
                    v-model="passwordForm.correo"
                    type="email"
                    required
                    :disabled="isChangingPassword"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                    placeholder="tu.correo@example.com"
                  />
                </div>

                <!-- Contraseña Actual -->
                <div>
                  <label
                    for="current-password"
                    class="block text-sm font-medium text-gray-700 mb-1"
                  >
                    Contraseña Actual
                  </label>
                  <div class="relative">
                    <input
                      id="current-password"
                      v-model="passwordForm.currentPassword"
                      :type="showCurrentPassword ? 'text' : 'password'"
                      required
                      :disabled="isChangingPassword"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                      placeholder="••••••••"
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
                      <svg
                        v-else
                        class="h-5 w-5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
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
                      v-model="passwordForm.newPassword"
                      :type="showNewPassword ? 'text' : 'password'"
                      required
                      minlength="8"
                      :disabled="isChangingPassword"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                      placeholder="••••••••"
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
                      <svg
                        v-else
                        class="h-5 w-5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
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
                  <label
                    for="confirm-password"
                    class="block text-sm font-medium text-gray-700 mb-1"
                  >
                    Confirmar Nueva Contraseña
                  </label>
                  <div class="relative">
                    <input
                      id="confirm-password"
                      v-model="passwordForm.confirmPassword"
                      :type="showConfirmPassword ? 'text' : 'password'"
                      required
                      minlength="8"
                      :disabled="isChangingPassword"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                      placeholder="••••••••"
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
                      <svg
                        v-else
                        class="h-5 w-5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
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
                    @click="closeChangePasswordModal"
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

        <!-- Modal para Reporte Integral (individual) -->
        <Transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div
            v-if="showReporteIntegralModal"
            class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
          >
            <div
              class="relative top-20 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white"
            >
              <div class="flex justify-end items-center mb-4">
                <button
                  @click="closeReporteIntegralModal"
                  class="text-gray-500 hover:text-gray-700"
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
              <ReporteIntegralTutoria
                v-if="selectedStudent"
                :nombre="selectedStudent.name"
                :num_control="selectedStudent.controlNumber"
              />
            </div>
          </div>
        </Transition>

        <!-- Modal para Primer Reporte -->
        <Transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div
            v-if="mostrarModalPrimerReporte"
            class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
          >
            <div
              class="relative top-20 mx-auto p-5 border w-11/12 max-w-5xl shadow-lg rounded-md bg-white"
            >
              <div class="p-4 border-b flex justify-end items-center">
                <button
                  @click="mostrarModalPrimerReporte = false"
                  class="text-gray-500 hover:text-gray-700"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-6 w-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
              <div class="p-4">
                <ReporteIndividual1 @cerrar="mostrarModalPrimerReporte = false" />
              </div>
            </div>
          </div>
        </Transition>

        <!-- Modal para Segundo Reporte -->
        <Transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div
            v-if="mostrarModalSegundoReporte"
            class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
          >
            <div
              class="relative top-20 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white"
            >
              <div class="p-4 border-b flex justify-end items-center">
                <button
                  @click="mostrarModalSegundoReporte = false"
                  class="text-gray-500 hover:text-gray-700"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-6 w-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
              <div class="p-4">
                <SegundoReporteTutoria @cerrar="mostrarModalSegundoReporte = false" />
              </div>
            </div>
          </div>
        </Transition>

        <!-- Pestañas -->
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8">
            <a
              v-for="tab in tabs"
              :key="tab.id"
              href="#"
              @click.prevent="currentTab = tab.id"
              :class="[
                currentTab === tab.id
                  ? 'border-coral-500 text-coral-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm',
              ]"
            >
              {{ tab.name }}
            </a>
          </nav>
        </div>

        <!-- Tabla de estudiantes -->
        <div class="mt-8 flex flex-col">
          <div class="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
            <div class="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
              <div class="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg bg-white">
                <!-- Loading State -->
                <div v-if="loading" class="p-8">
                  <div class="flex flex-col items-center justify-center space-y-4">
                    <svg
                      class="animate-spin h-12 w-12 text-coral-500"
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
                    <p class="text-gray-600 text-sm font-medium">Cargando estudiantes...</p>
                  </div>

                  <!-- Skeleton Loader -->
                  <div class="mt-6 space-y-3 animate-pulse">
                    <div
                      v-for="i in 5"
                      :key="i"
                      class="flex items-center space-x-4 p-4 border-t border-gray-200"
                    >
                      <div class="flex-1 space-y-2">
                        <div class="h-4 bg-gray-200 rounded w-3/4"></div>
                        <div class="h-3 bg-gray-200 rounded w-1/2"></div>
                      </div>
                      <div class="h-6 bg-gray-200 rounded w-20"></div>
                      <div class="h-8 bg-gray-200 rounded w-32"></div>
                    </div>
                  </div>
                </div>

                <!-- Tabla con datos -->
                <table v-else-if="students.length > 0" class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th
                        v-for="header in tableHeaders"
                        :key="header.key"
                        scope="col"
                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        {{ header.label }}
                      </th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr
                      v-for="student in students"
                      :key="student.id"
                      class="hover:bg-gray-50 transition-colors"
                    >
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="flex items-center">
                          <div class="ml-4">
                            <div class="text-sm font-medium text-gray-900">
                              {{ student.name }}
                            </div>
                            <div class="text-sm text-gray-500">
                              {{ student.controlNumber }}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm text-gray-900">{{ student.semester }}° Semestre</div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span
                          class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                          :class="
                            student.status === 'A'
                              ? 'bg-orange-500/20 text-orange-400'
                              : 'bg-green-500/20 text-green-400'
                          "
                        >
                          {{ student.status }}
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {{ student.tutorialPeriod }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <a
                          href="#"
                          @click.prevent="viewDetails(student)"
                          class="text-coral-600 hover:text-coral-900 mx-4"
                          >Ver detalles</a
                        >
                        <!-- <button
                          @click="openReporteIntegralModal(student)"
                          class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition duration-150 ease-in-out inline-flex items-center gap-2 ml-2"
                        >
                          Reporte Integral
                        </button> -->
                        <button
                          @click="abrirModalEliminar(student)"
                          class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition duration-150 ease-in-out inline-flex items-center gap-2 ml-2"
                          title="Eliminar tutoría"
                        >
                          <svg
                            class="w-4 h-4"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              stroke-width="2"
                              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                            />
                          </svg>
                          Eliminar
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>

                <!-- Estado vacío -->
                <div v-else-if="!loading && students.length === 0" class="text-center py-12 px-4">
                  <svg
                    class="mx-auto h-16 w-16 text-gray-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
                    />
                  </svg>
                  <h3 class="mt-4 text-lg font-medium text-gray-900">
                    No se encontraron estudiantes
                  </h3>
                  <p class="mt-2 text-sm text-gray-500">
                    {{
                      searchQuery
                        ? 'No hay estudiantes que coincidan con tu búsqueda.'
                        : 'No se le está aplicando tutoría a ningún alumno.'
                    }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Paginación -->
        <div
          v-if="!loading && students.length > 0"
          class="py-3 flex items-center justify-between bg-white mt-4 rounded-lg px-4"
        >
          <div class="flex-1 flex justify-between sm:hidden">
            <button
              @click="prevPage"
              :disabled="currentPage === 1 || loading"
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Anterior
            </button>
            <button
              @click="nextPage"
              :disabled="currentPage === totalPages || loading"
              class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Siguiente
            </button>
          </div>
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                Mostrando
                <span class="font-medium">{{ (currentPage - 1) * itemsPerPage + 1 }}</span>
                a
                <span class="font-medium">{{
                  Math.min(currentPage * itemsPerPage, totalItems)
                }}</span>
                de
                <span class="font-medium">{{ totalItems }}</span>
                resultados
              </p>
            </div>
            <div>
              <nav
                class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
                aria-label="Pagination"
              >
                <button
                  @click="prevPage"
                  :disabled="currentPage === 1 || loading"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span class="sr-only">Anterior</span>
                  <svg
                    class="h-5 w-5"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </button>
                <button
                  v-for="page in totalPages"
                  :key="page"
                  @click="goToPage(page)"
                  :disabled="loading"
                  :class="[
                    currentPage === page
                      ? 'z-10 bg-coral-50 border-coral-500 text-coral-600'
                      : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50',
                    'relative inline-flex items-center px-4 py-2 border text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed',
                  ]"
                >
                  {{ page }}
                </button>
                <button
                  @click="nextPage"
                  :disabled="currentPage === totalPages || loading"
                  class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span class="sr-only">Siguiente</span>
                  <svg
                    class="h-5 w-5"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </button>
              </nav>
            </div>
          </div>
        </div>

        <!-- Modal de detalles -->
        <Transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div v-if="showModal" class="fixed inset-0 z-50 overflow-y-auto">
            <div
              class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
            >
              <div class="fixed inset-0 transition-opacity" aria-hidden="true">
                <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
              </div>

              <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true"
                >&#8203;</span
              >

              <div
                v-if="selectedStudent"
                class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
              >
                <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                  <div class="absolute top-4 right-4">
                    <button
                      @click="closeModal"
                      class="text-gray-400 hover:text-gray-600 transition-colors"
                    >
                      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M6 18L18 6M6 6l12 12"
                        />
                      </svg>
                    </button>
                  </div>

                  <h2 class="text-2xl font-bold mb-6 text-gray-900 border-b pb-2">
                    Detalles del Estudiante
                  </h2>

                  <div class="space-y-6">
                    <div class="bg-gray-50 p-4 rounded-lg">
                      <h3 class="text-lg font-semibold text-coral-600 mb-3">
                        Información del Alumno
                      </h3>
                      <div class="space-y-2">
                        <div class="grid grid-cols-3 gap-2">
                          <span class="text-gray-600 font-medium">Nombre:</span>
                          <span class="col-span-2 text-gray-900"
                            >{{ selectedStudent.nombre }} {{ selectedStudent.apellido_p }}
                            {{ selectedStudent.apellido_m }}</span
                          >
                        </div>
                        <div class="grid grid-cols-3 gap-2">
                          <span class="text-gray-600 font-medium">Número de Control:</span>
                          <span class="col-span-2 text-gray-900">{{
                            selectedStudent.num_control
                          }}</span>
                        </div>
                        <div class="grid grid-cols-3 gap-2">
                          <span class="text-gray-600 font-medium">Carrera:</span>
                          <span class="col-span-2 text-gray-900">{{
                            selectedStudent.carrera
                          }}</span>
                        </div>
                        <div class="grid grid-cols-3 gap-2">
                          <span class="text-gray-600 font-medium">Semestre Actual:</span>
                          <span class="col-span-2 text-gray-900"
                            >{{ selectedStudent.semestre_actual }}°</span
                          >
                        </div>
                      </div>
                    </div>

                    <div class="bg-gray-50 p-4 rounded-lg">
                      <h3 class="text-lg font-semibold text-coral-600 mb-3">
                        Información de la Tutoría
                      </h3>
                      <div class="space-y-2">
                        <div class="grid grid-cols-3 gap-2">
                          <span class="text-gray-600 font-medium">Nivel de Tutoría:</span>
                          <span class="col-span-2 text-gray-900"
                            >{{ selectedStudent.tutoring.semestre }}°</span
                          >
                        </div>
                        <div class="grid grid-cols-3 gap-2">
                          <span class="text-gray-600 font-medium">Periodo:</span>
                          <span class="col-span-2 text-gray-900">{{
                            selectedStudent.tutoring.periodo
                          }}</span>
                        </div>
                        <div class="grid grid-cols-3 gap-2">
                          <span class="text-gray-600 font-medium">Día:</span>
                          <span class="col-span-2 text-gray-900">{{
                            capitalize(selectedStudent.tutoring)
                          }}</span>
                        </div>
                        <div class="grid grid-cols-3 gap-2">
                          <span class="text-gray-600 font-medium">Hora:</span>
                          <span class="col-span-2 text-gray-900">{{
                            formatoHora(selectedStudent.tutoring)
                          }}</span>
                        </div>
                        <div class="mt-4">
                          <span class="text-gray-600 font-medium block mb-1">Observaciones:</span>
                          <p class="text-gray-900 bg-white p-3 rounded border">
                            {{ selectedStudent.tutoring.observaciones || 'Sin observaciones' }}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="mt-6 flex justify-end">
                    <button
                      @click="closeModal"
                      class="bg-coral-500 hover:bg-coral-600 text-white font-medium py-2 px-6 rounded-lg transition-colors duration-200"
                    >
                      Cerrar
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Transition>
      </main>
    </div>

    <!-- Modal Reporte Integral Masivo (FUERA de main, al nivel del root div) -->
    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="showReporteIntegralMasivo" class="fixed inset-0 z-[9999]">
        <ReporteIntegralMasivo
          :tutor-info="{
            nombre: tutor?.nombre + ' ' + tutor?.apellido_p + ' ' + tutor?.apellido_m,
            departamento: 'Sistemas Computacionales',
            periodo: '22025',
            carrera: 'Ingeniería en Sistemas',
          }"
          :tutor-id="tutor?.id_tutor"
          @close="closeReporteIntegralMasivo"
          @success="handleReporteIntegralSuccess"
        />
      </div>
    </Transition>

    <!-- Modal Crear Tutoría -->
    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="showModalCrearTutoria" class="fixed inset-0 z-[9999] overflow-y-auto">
        <div class="flex items-center justify-center min-h-screen p-4">
          <div class="fixed inset-0 bg-black opacity-50" @click="cerrarModalCrear"></div>

          <div class="relative bg-white rounded-lg shadow-xl max-w-md w-full p-6 z-10">
            <!-- Header -->
            <div class="flex justify-between items-center mb-6 border-b pb-3">
              <h2 class="text-2xl font-bold text-gray-900">Crear Nueva Tutoría</h2>
              <button
                @click="cerrarModalCrear"
                :disabled="isCreating"
                class="text-gray-400 hover:text-gray-600 transition-colors disabled:opacity-50"
              >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>

            <!-- Búsqueda de Alumno -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                🔍 Buscar Alumno <span class="text-red-500">*</span>
              </label>
              <input
                v-model="searchAlumnoQuery"
                @input="buscarAlumnos"
                type="text"
                :disabled="isCreating"
                placeholder="Nombre, apellido o número de control..."
                class="w-full px-3 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-coral-500 focus:border-coral-500 disabled:bg-gray-100 disabled:cursor-not-allowed transition-all"
              />
              <p class="text-xs text-gray-500 mt-1">Mínimo 3 caracteres</p>

              <!-- Dropdown de resultados -->
              <Transition
                enter-active-class="transition ease-out duration-200"
                enter-from-class="opacity-0 translate-y-1"
                enter-to-class="opacity-100 translate-y-0"
                leave-active-class="transition ease-in duration-150"
                leave-from-class="opacity-100"
                leave-to-class="opacity-0"
              >
                <div
                  v-if="alumnosEncontrados.length > 0 && !alumnoSeleccionado"
                  class="mt-2 max-h-48 overflow-y-auto border-2 border-gray-200 rounded-lg shadow-lg bg-white"
                >
                  <div
                    v-for="alumno in alumnosEncontrados"
                    :key="alumno.id_alumno"
                    @click="seleccionarAlumno(alumno)"
                    class="p-3 hover:bg-blue-50 cursor-pointer border-b border-gray-100 last:border-b-0 transition-colors"
                  >
                    <div class="font-medium text-gray-900">
                      {{ alumno.nombre }} {{ alumno.apellido_p }} {{ alumno.apellido_m }}
                    </div>
                    <div class="text-sm text-gray-500">
                      {{ alumno.num_control }} - {{ alumno.carrera }}
                    </div>
                  </div>
                </div>
              </Transition>

              <!-- Alumno seleccionado -->
              <Transition
                enter-active-class="transition ease-out duration-200"
                enter-from-class="opacity-0 scale-95"
                enter-to-class="opacity-100 scale-100"
                leave-active-class="transition ease-in duration-150"
                leave-from-class="opacity-100"
                leave-to-class="opacity-0"
              >
                <div
                  v-if="alumnoSeleccionado"
                  class="mt-2 p-3 bg-green-50 border-2 border-green-300 rounded-lg flex items-start justify-between"
                >
                  <div class="flex items-start">
                    <svg
                      class="w-5 h-5 text-green-500 mr-2 flex-shrink-0 mt-0.5"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                        clip-rule="evenodd"
                      />
                    </svg>
                    <div>
                      <div class="font-medium text-green-900">
                        {{ alumnoSeleccionado.nombre }} {{ alumnoSeleccionado.apellido_p }}
                        {{ alumnoSeleccionado.apellido_m }}
                      </div>
                      <div class="text-sm text-green-700">{{ alumnoSeleccionado.num_control }}</div>
                    </div>
                  </div>
                  <button
                    @click="clearAlumnoSelection"
                    :disabled="isCreating"
                    class="text-green-600 hover:text-green-800 disabled:opacity-50"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                </div>
              </Transition>
            </div>

            <!-- Semestre -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                📚 Semestre <span class="text-red-500">*</span>
              </label>
              <select
                v-model="semestreSeleccionado"
                :disabled="isCreating"
                class="w-full px-3 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-coral-500 focus:border-coral-500 disabled:bg-gray-100 disabled:cursor-not-allowed transition-all"
              >
                <option value="">Seleccionar semestre...</option>
                <option v-for="sem in 9" :key="sem" :value="sem">{{ sem }}° Semestre</option>
              </select>
            </div>

            <!-- Periodo -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                📅 Periodo <span class="text-red-500">*</span>
              </label>
              <input
                v-model="periodoInput"
                @input="validarPeriodoInput"
                type="text"
                maxlength="5"
                :disabled="isCreating"
                placeholder="22025"
                class="w-full px-3 py-2 border-2 rounded-lg focus:outline-none focus:ring-2 transition-all disabled:bg-gray-100 disabled:cursor-not-allowed"
                :class="
                  errorPeriodo
                    ? 'border-red-500 focus:ring-red-500 focus:border-red-500'
                    : 'border-gray-300 focus:ring-coral-500 focus:border-coral-500'
                "
              />
              <p v-if="errorPeriodo" class="text-red-500 text-xs mt-1 flex items-center">
                <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fill-rule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                    clip-rule="evenodd"
                  />
                </svg>
                {{ errorPeriodo }}
              </p>
              <p class="text-gray-500 text-xs mt-1">
                Debe empezar con "2" y tener 5 dígitos. Ej: 22025
              </p>
            </div>

            <!-- Mensajes de error -->
            <Transition
              enter-active-class="transition ease-out duration-200"
              enter-from-class="opacity-0 translate-y-1"
              enter-to-class="opacity-100 translate-y-0"
              leave-active-class="transition ease-in duration-150"
              leave-from-class="opacity-100"
              leave-to-class="opacity-0"
            >
              <div
                v-if="errorModalCrear"
                class="mb-4 p-3 bg-red-50 border-l-4 border-red-500 rounded"
              >
                <div class="flex items-start">
                  <svg
                    class="w-5 h-5 text-red-500 mr-2 flex-shrink-0"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                      clip-rule="evenodd"
                    />
                  </svg>
                  <p class="text-sm text-red-800 font-medium">{{ errorModalCrear }}</p>
                </div>
              </div>
            </Transition>

            <!-- Botones -->
            <div class="flex gap-3 pt-4 border-t">
              <button
                @click="cerrarModalCrear"
                :disabled="isCreating"
                class="flex-1 px-4 py-2 border-2 border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                Cancelar
              </button>
              <button
                @click="crearTutoria"
                :disabled="
                  isCreating ||
                  !alumnoSeleccionado ||
                  !semestreSeleccionado ||
                  errorPeriodo ||
                  periodoInput.length !== 5
                "
                class="flex-1 px-4 py-2 rounded-lg font-bold text-white focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:cursor-not-allowed transition-all inline-flex justify-center items-center shadow-md hover:shadow-lg"
                :class="
                  isCreating ||
                  !alumnoSeleccionado ||
                  !semestreSeleccionado ||
                  errorPeriodo ||
                  periodoInput.length !== 5
                    ? 'bg-gray-400'
                    : 'bg-gradient-to-r from-orange-600 to-orange-700 hover:from-orange-700 hover:to-orange-800 focus:ring-orange-500'
                "
              >
                <svg
                  v-if="isCreating"
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
                {{ isCreating ? 'Creando...' : 'Crear Tutoría' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Modal Eliminar Tutoría con Confirmación -->
    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="showModalEliminarTutoria" class="fixed inset-0 z-[9999] overflow-y-auto">
        <div class="flex items-center justify-center min-h-screen p-4">
          <div class="fixed inset-0 bg-black opacity-50" @click="cerrarModalEliminar"></div>

          <div class="relative bg-white rounded-lg shadow-xl max-w-md w-full p-6 z-10">
            <!-- Header con icono de advertencia -->
            <div class="flex items-start mb-6">
              <div class="flex-shrink-0 bg-red-100 rounded-full p-3 mr-4">
                <svg
                  class="w-8 h-8 text-red-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
              </div>
              <div class="flex-1">
                <h2 class="text-xl font-bold text-gray-900 mb-2">⚠️ Confirmar Eliminación</h2>
                <p class="text-sm text-gray-600">
                  Esta acción es <strong class="text-red-600">permanente e irreversible</strong>
                </p>
              </div>
              <button
                @click="cerrarModalEliminar"
                :disabled="isDeleting"
                class="text-gray-400 hover:text-gray-600 transition-colors disabled:opacity-50 -mt-1"
              >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>

            <!-- Información del alumno -->
            <div
              v-if="tutoriaAEliminar"
              class="mb-6 p-4 bg-gray-50 border-l-4 border-red-500 rounded"
            >
              <p class="text-sm text-gray-700 mb-2">Estás a punto de eliminar la tutoría de:</p>
              <div class="font-bold text-gray-900 text-lg">
                {{ tutoriaAEliminar.name }}
              </div>
              <div class="text-sm text-gray-600 mt-1">
                No. Control: {{ tutoriaAEliminar.controlNumber }}
              </div>
              <div class="text-sm text-gray-600">
                Semestre: {{ tutoriaAEliminar.semester }}° - Periodo:
                {{ tutoriaAEliminar.tutorialPeriod }}
              </div>
            </div>

            <!-- Advertencia -->
            <div class="mb-4 p-3 bg-yellow-50 border-l-4 border-yellow-400 rounded">
              <div class="flex items-start">
                <svg
                  class="w-5 h-5 text-yellow-400 mr-2 flex-shrink-0 mt-0.5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fill-rule="evenodd"
                    d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                    clip-rule="evenodd"
                  />
                </svg>
                <div class="text-sm text-yellow-800">
                  <strong>Importante:</strong> Se eliminarán todos los datos relacionados con esta
                  tutoría, incluyendo reportes y seguimientos.
                </div>
              </div>
            </div>

            <!-- Input de confirmación de correo -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                🔒 Para confirmar, escribe tu correo electrónico
              </label>
              <input
                v-model="correoConfirmacion"
                type="email"
                :disabled="isDeleting"
                placeholder="tu.correo@example.com"
                class="w-full px-3 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 disabled:bg-gray-100 disabled:cursor-not-allowed transition-all"
                @keyup.enter="eliminarTutoria"
              />
              <p class="text-xs text-gray-500 mt-1">
                Tu correo: <strong class="text-gray-700">{{ tutor?.correo }}</strong>
              </p>
            </div>

            <!-- Mensajes de error -->
            <Transition
              enter-active-class="transition ease-out duration-200"
              enter-from-class="opacity-0 translate-y-1"
              enter-to-class="opacity-100 translate-y-0"
              leave-active-class="transition ease-in duration-150"
              leave-from-class="opacity-100"
              leave-to-class="opacity-0"
            >
              <div
                v-if="errorModalEliminar"
                class="mb-4 p-3 bg-red-50 border-l-4 border-red-500 rounded"
              >
                <div class="flex items-start">
                  <svg
                    class="w-5 h-5 text-red-500 mr-2 flex-shrink-0"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                      clip-rule="evenodd"
                    />
                  </svg>
                  <p class="text-sm text-red-800 font-medium">{{ errorModalEliminar }}</p>
                </div>
              </div>
            </Transition>

            <!-- Botones -->
            <div class="flex gap-3 pt-4 border-t">
              <button
                @click="cerrarModalEliminar"
                :disabled="isDeleting"
                class="flex-1 px-4 py-2 border-2 border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                Cancelar
              </button>
              <button
                @click="eliminarTutoria"
                :disabled="
                  isDeleting ||
                  !correoConfirmacion ||
                  correoConfirmacion.trim().toLowerCase() !== tutor?.correo?.trim().toLowerCase()
                "
                class="flex-1 px-4 py-2 rounded-lg font-bold text-white focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:cursor-not-allowed transition-all inline-flex justify-center items-center shadow-md hover:shadow-lg"
                :class="
                  isDeleting ||
                  !correoConfirmacion ||
                  correoConfirmacion.trim().toLowerCase() !== tutor?.correo?.trim().toLowerCase()
                    ? 'bg-gray-400'
                    : 'bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 focus:ring-red-500'
                "
              >
                <svg
                  v-if="isDeleting"
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
                <svg
                  v-else
                  class="w-5 h-5 mr-2"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                  />
                </svg>
                {{ isDeleting ? 'Eliminando...' : 'Eliminar Tutoría' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import TutorService from '@/services/TutorService.js'
import ReporteIntegralMasivo from '@/components/ReporteIntegralMasivo.vue'
import ReporteIntegralTutoria from '@/components/ReporteIntegralTutoria.vue'
// import PrimerReporteTutoria from '@/components/PrimerReporteTutoria.vue'
import SegundoReporteTutoria from '@/components/SegundoReporteTutoria.vue'
import BaseSearchInput from '@/components/ui/BaseSearchInput.vue'
import ReporteIndividual1 from '@/components/tutor/ReporteIndividual1.vue'

// ==================== ROUTER ====================
const router = useRouter()

// ==================== STATE ====================
const tutor = ref(null)
const studentsData = ref([])
const selectedStudent = ref(null)
const totalItems = ref(0)
let debounceTimer = null

// ==================== UI STATE ====================
const searchQuery = ref('')
const currentTab = ref('current')
const currentPage = ref(1)
const itemsPerPage = ref(5)
const loading = ref(false)
const error = ref(null)

// ==================== MODALS STATE ====================
const showModal = ref(false)
const showReporteIntegralModal = ref(false)
const mostrarModalPrimerReporte = ref(false)
const mostrarModalSegundoReporte = ref(false)
const showChangePasswordModal = ref(false)
const showReporteIntegralMasivo = ref(false)

// ==================== MODAL CREAR TUTORÍA STATE ====================
const showModalCrearTutoria = ref(false)
const searchAlumnoQuery = ref('')
const alumnosEncontrados = ref([])
const alumnoSeleccionado = ref(null)
const semestreSeleccionado = ref('')
const periodoInput = ref('')
const errorPeriodo = ref(null)
const errorModalCrear = ref(null)
const isCreating = ref(false)
let debounceTimerAlumnos = null

// ==================== MODAL ELIMINAR TUTORÍA STATE ====================
const showModalEliminarTutoria = ref(false)
const tutoriaAEliminar = ref(null)
const correoConfirmacion = ref('')
const errorModalEliminar = ref(null)
const isDeleting = ref(false)

// ==================== PASSWORD CHANGE STATE ====================
const passwordForm = ref({
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

// ==================== CONSTANTS ====================
const tabs = [
  { id: 'current', name: 'Tutorados Actuales' },
  { id: 'past', name: 'Tutorados Anteriores' },
]

const tableHeaders = [
  { key: 'name', label: 'Estudiante' },
  { key: 'semester', label: 'Nivel de Tutoría' },
  { key: 'status', label: 'Estado' },
  { key: 'tutorialPeriod', label: 'Periodo' },
  { key: 'actions', label: 'Acciones' },
]

const circles = [
  { color: 'bg-coral-500', size: 96, top: 10, left: 5 },
  { color: 'bg-navy-600', size: 64, top: 20, left: 80 },
  { color: 'bg-coral-400', size: 128, top: 70, left: 20 },
  { color: 'bg-navy-300', size: 80, top: 40, left: 95 },
  { color: 'bg-coral-300', size: 112, top: 85, left: 70 },
  { color: 'bg-navy-400', size: 48, top: 55, left: 10 },
  { color: 'bg-coral-600', size: 72, top: 60, left: 50 },
  { color: 'bg-navy-500', size: 56, top: 5, left: 90 },
  { color: 'bg-coral-500', size: 88, top: 80, left: 40 },
  { color: 'bg-navy-300', size: 40, top: 90, left: 10 },
  { color: 'bg-coral-400', size: 104, top: 15, left: 60 },
  { color: 'bg-navy-400', size: 68, top: 50, left: 85 },
]

// ==================== COMPUTED ====================
const students = computed(() => {
  return studentsData.value.filter((student) =>
    currentTab.value === 'current' ? student.status === 'A' : student.status === 'completada',
  )
})

const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value))

// ==================== API CALLS ====================
const fetchCurrentTutor = async () => {
  try {
    const token = localStorage.getItem('accessToken')

    if (!token) {
      console.log('No hay token, redirigiendo al login...')
      router.push('/login_tutor')
      return
    }

    const response = await axios.get('http://localhost:8000/api/tutores/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (response.status === 200) {
      tutor.value = response.data
      console.log('Tutor cargado:', tutor.value)

      passwordForm.value.correo = tutor.value.correo

      await fetchAssignedStudents(currentPage.value)
    }
  } catch (err) {
    console.error('Error al obtener datos del tutor:', err)

    if (err.response && (err.response.status === 401 || err.response.status === 403)) {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('userRole')
      router.push('/login_tutor')
    }
  }
}

const fetchAssignedStudents = async (page) => {
  if (!tutor.value || tutor.value.id_tutor === null) {
    error.value = 'Datos del tutor no disponibles.'
    return
  }

  error.value = null

  try {
    const response = await TutorService.getTutoriasPorTutor(
      tutor.value.id_tutor,
      page,
      itemsPerPage.value,
      searchQuery.value,
    )
    console.log(response.data)

    totalItems.value = response.data.total_tutorias

    studentsData.value = response.data.tutorias.map((tutoria) => ({
      id: tutoria.alumno?.id_alumno || null,
      name: tutoria.alumno
        ? `${tutoria.alumno.nombre || ''} ${tutoria.alumno.apellido_p || ''} ${tutoria.alumno.apellido_m || ''}`.trim()
        : 'Alumno Desconocido',
      controlNumber: tutoria.alumno?.num_control || 'N/A',
      semester: tutoria.semestre,
      status: tutoria.alumno?.estado || 'N/A',
      tutorialPeriod: tutoria.periodo,
      tutoringId: tutoria.id_tutoria,
      // Agregar campos necesarios para el ReporteIntegralMasivo
      nombre: tutoria.alumno
        ? `${tutoria.alumno.nombre || ''} ${tutoria.alumno.apellido_p || ''} ${tutoria.alumno.apellido_m || ''}`.trim()
        : 'Alumno Desconocido',
      num_control: tutoria.alumno?.num_control || 'N/A',
    }))
    console.log(studentsData)
  } catch (err) {
    console.error('Error al obtener las tutorías asignadas:', err)
    if (
      err.response &&
      err.response.status === 400 &&
      err.response.data.detail?.includes('string_too_short')
    ) {
      error.value = 'Favor de ingresar mínimo 3 caracteres a buscar.'
    } else if (err.response?.status !== 401 && err.response?.status !== 403) {
      error.value = 'No se pudo cargar la lista de alumnos asignados.'
    }
    studentsData.value = []
    totalItems.value = 0
  } finally {
    loading.value = false
  }
}

// ==================== PASSWORD CHANGE HANDLERS ====================
const openChangePasswordModal = () => {
  showChangePasswordModal.value = true
  passwordChangeError.value = null
  passwordChangeSuccess.value = false
  passwordForm.value = {
    correo: tutor.value?.correo || '',
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  }
}

const closeChangePasswordModal = () => {
  if (!isChangingPassword.value) {
    showChangePasswordModal.value = false
    passwordForm.value = {
      correo: tutor.value?.correo || '',
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
}

const handleChangePassword = async () => {
  passwordChangeError.value = null
  passwordChangeSuccess.value = false

  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    passwordChangeError.value = 'Las contraseñas no coinciden.'
    return
  }

  if (passwordForm.value.newPassword.length < 8) {
    passwordChangeError.value = 'La nueva contraseña debe tener al menos 8 caracteres.'
    return
  }

  if (tutor.value.requires_password_change && !passwordForm.value.correo) {
    passwordChangeError.value = 'El correo es requerido.'
    return
  }

  isChangingPassword.value = true

  try {
    const token = localStorage.getItem('accessToken')

    if (tutor.value.requires_password_change) {
      const response = await axios.post('http://localhost:8000/api/tutores/set-password', {
        correo: passwordForm.value.correo,
        contraseña_actual: passwordForm.value.currentPassword,
        nueva_contraseña: passwordForm.value.newPassword,
      })

      if (response.status === 200) {
        passwordChangeSuccess.value = true
        tutor.value.requires_password_change = false

        setTimeout(() => {
          closeChangePasswordModal()
        }, 2000)
      }
    } else {
      const response = await axios.put(
        'http://localhost:8000/api/tutores/change-password',
        {
          contraseña_actual: passwordForm.value.currentPassword,
          nueva_contraseña: passwordForm.value.newPassword,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      )

      if (response.status === 200) {
        passwordChangeSuccess.value = true

        setTimeout(() => {
          closeChangePasswordModal()
        }, 2000)
      }
    }
  } catch (err) {
    console.error('Error al cambiar la contraseña:', err)

    if (err.response && err.response.data && err.response.data.detail) {
      passwordChangeError.value = err.response.data.detail
    } else if (err.response && err.response.status === 400) {
      passwordChangeError.value = 'Contraseña actual incorrecta.'
    } else if (err.response && err.response.status === 401) {
      passwordChangeError.value = 'No tienes autorización para realizar esta acción.'
    } else {
      passwordChangeError.value = 'Error al cambiar la contraseña. Intenta de nuevo.'
    }
  } finally {
    isChangingPassword.value = false
  }
}

// ==================== SEARCH WATCHER ====================
// eslint-disable-next-line
watch(searchQuery, (newQuery, oldQuery) => {
  clearTimeout(debounceTimer)

  debounceTimer = setTimeout(() => {
    currentPage.value = 1
    fetchAssignedStudents()
  }, 500)
})

// ==================== MODAL HANDLERS ====================
// const openReporteIntegralModal = (student) => {
//   selectedStudent.value = student
//   showReporteIntegralModal.value = true
// }

const closeReporteIntegralModal = () => {
  showReporteIntegralModal.value = false
  selectedStudent.value = null
}

const viewDetails = async (student) => {
  try {
    const tutoringResponse = await axios.get(
      `http://localhost:8000/api/tutorias/alumno/${student.tutoringId}`,
    )
    console.log('STUDENT', student)
    console.log('TUTORIA RESPONSE', tutoringResponse)

    selectedStudent.value = {
      ...tutoringResponse.data.alumno,
      tutoring: tutoringResponse.data,
    }
    showModal.value = true
  } catch (err) {
    console.error('Error fetching student details:', err)
    error.value = 'No se pudieron cargar los detalles del estudiante.'
  }
}

const closeModal = () => {
  showModal.value = false
  selectedStudent.value = null
}

const openReporteIntegralMasivo = () => {
  console.log('Abriendo modal masivo...')
  showReporteIntegralMasivo.value = true
}

const closeReporteIntegralMasivo = () => {
  showReporteIntegralMasivo.value = false
}

const handleReporteIntegralSuccess = () => {
  closeReporteIntegralMasivo()
}

// ==================== PAGINATION ====================
const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    fetchAssignedStudents(currentPage.value)
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    fetchAssignedStudents(currentPage.value)
  }
}

const goToPage = (page) => {
  currentPage.value = page
  fetchAssignedStudents(page)
}

// ==================== UTILITY FUNCTIONS ====================
const capitalize = (tutoria) => {
  if (tutoria.dia != null) {
    return tutoria.dia.charAt(0).toUpperCase() + tutoria.dia.slice(1)
  }
  return null
}

const formatoHora = (tutoria) => {
  if (tutoria.hora != null) {
    const [horas, minutos] = tutoria.hora.split(':').map(Number)
    const ampm = horas < 12 ? 'AM' : 'PM'
    const horaFormateada = `${horas % 12 || 12}:${minutos.toString().padStart(2, '0')} ${ampm}`
    return horaFormateada
  }
  return null
}

// ==================== AUTH ====================
const handleLogout = () => {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('userRole')
  router.push('/login_tutor')
}

// ==================== DESCARGA PDF ====================
const descargarPDFReporteIntegral = async () => {
  try {
    loading.value = true
    const token = localStorage.getItem('accessToken')

    // Obtener el periodo desde la primera tutoría (todas deberían tener el mismo periodo)
    const periodo = studentsData.value[0]?.tutorialPeriod || '22025'

    const response = await axios.get(
      `http://localhost:8000/api/reportes/integral/pdf/tutor/${tutor.value.id_tutor}/periodo/${periodo}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        responseType: 'blob', // IMPORTANTE: para recibir el PDF como blob
      },
    )

    // Crear un URL temporal para el blob
    const blob = new Blob([response.data], { type: 'application/pdf' })
    const url = window.URL.createObjectURL(blob)

    // Crear un link temporal y hacer click para descargar
    const link = document.createElement('a')
    link.href = url
    link.download = `Reporte_Integral_${tutor.value.nombre}_${periodo}.pdf`
    document.body.appendChild(link)
    link.click()

    // Limpiar
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    console.log('✅ PDF descargado exitosamente')
  } catch (err) {
    console.error('Error al descargar PDF:', err)
    if (err.response?.status === 404) {
      error.value = 'No se encontraron reportes integrales para descargar.'
    } else {
      error.value = 'Error al generar el PDF. Intenta de nuevo.'
    }
  } finally {
    loading.value = false
  }
}

// ==================== CREAR TUTORÍA HANDLERS ====================
const abrirModalCrear = () => {
  showModalCrearTutoria.value = true
  searchAlumnoQuery.value = ''
  alumnosEncontrados.value = []
  alumnoSeleccionado.value = null
  semestreSeleccionado.value = ''
  periodoInput.value = ''
  errorPeriodo.value = null
  errorModalCrear.value = null
}

const cerrarModalCrear = () => {
  if (!isCreating.value) {
    showModalCrearTutoria.value = false
    searchAlumnoQuery.value = ''
    alumnosEncontrados.value = []
    alumnoSeleccionado.value = null
    semestreSeleccionado.value = ''
    periodoInput.value = ''
    errorPeriodo.value = null
    errorModalCrear.value = null
  }
}

const buscarAlumnos = async () => {
  clearTimeout(debounceTimerAlumnos)

  if (searchAlumnoQuery.value.length < 3) {
    alumnosEncontrados.value = []
    return
  }

  debounceTimerAlumnos = setTimeout(async () => {
    try {
      const token = localStorage.getItem('accessToken')
      const response = await axios.get('http://localhost:8000/api/alumnos/', {
        params: {
          page: 1,
          size: 100,
          search: searchAlumnoQuery.value,
        },
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      // Ajustar según la estructura de respuesta del backend
      alumnosEncontrados.value = response.data.alumnos || response.data
    } catch (error) {
      console.error('Error al buscar alumnos:', error)
      alumnosEncontrados.value = []
    }
  }, 300)
}

const seleccionarAlumno = (alumno) => {
  alumnoSeleccionado.value = alumno
  alumnosEncontrados.value = []
  searchAlumnoQuery.value = `${alumno.nombre} ${alumno.apellido_p} ${alumno.apellido_m}`
}

const clearAlumnoSelection = () => {
  alumnoSeleccionado.value = null
  searchAlumnoQuery.value = ''
}

const validarPeriodoInput = () => {
  errorPeriodo.value = null

  if (periodoInput.value.length === 0) return

  // Solo números
  if (!/^\d+$/.test(periodoInput.value)) {
    errorPeriodo.value = 'El periodo debe contener solo números'
    return
  }

  // Si ya tiene 5 caracteres, validar completo
  if (periodoInput.value.length === 5) {
    if (!periodoInput.value.startsWith('2')) {
      errorPeriodo.value = 'El periodo debe empezar con "2"'
    }
  } else if (periodoInput.value.length > 5) {
    periodoInput.value = periodoInput.value.slice(0, 5)
  }
}

const crearTutoria = async () => {
  errorModalCrear.value = null

  // Validaciones
  if (!alumnoSeleccionado.value) {
    errorModalCrear.value = 'Debes seleccionar un alumno'
    return
  }

  if (!semestreSeleccionado.value) {
    errorModalCrear.value = 'Debes seleccionar un semestre'
    return
  }

  if (periodoInput.value.length !== 5) {
    errorModalCrear.value = 'El periodo debe tener exactamente 5 dígitos'
    return
  }

  if (!periodoInput.value.startsWith('2')) {
    errorModalCrear.value = 'El periodo debe empezar con "2"'
    return
  }

  if (errorPeriodo.value) {
    return
  }

  isCreating.value = true

  try {
    const token = localStorage.getItem('accessToken')
    const response = await axios.post(
      'http://localhost:8000/api/tutorias/',
      {
        periodo: periodoInput.value,
        estado: 'pendiente',
        observaciones: null,
        semestre: parseInt(semestreSeleccionado.value),
        alumno_id: alumnoSeleccionado.value.id_alumno,
        tutor_id: tutor.value.id_tutor,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )

    if (response.status === 201 || response.status === 200) {
      error.value = null
      // Mostrar mensaje de éxito temporal
      const nombreCompleto = `${alumnoSeleccionado.value.nombre} ${alumnoSeleccionado.value.apellido_p}`
      alert(`✅ Tutoría creada exitosamente para ${nombreCompleto}`)

      cerrarModalCrear()
      await fetchAssignedStudents(currentPage.value) // Recargar lista
    }
  } catch (err) {
    console.error('Error al crear tutoría:', err)
    if (err.response?.data?.detail) {
      errorModalCrear.value = err.response.data.detail
    } else if (err.response?.status === 400) {
      errorModalCrear.value = 'Datos inválidos. Verifica la información.'
    } else if (err.response?.status === 409) {
      errorModalCrear.value = 'Este alumno ya tiene una tutoría asignada para este semestre.'
    } else {
      errorModalCrear.value = 'Error al crear la tutoría. Intenta de nuevo.'
    }
  } finally {
    isCreating.value = false
  }
}

// ==================== ELIMINAR TUTORÍA HANDLERS ====================
const abrirModalEliminar = (student) => {
  tutoriaAEliminar.value = student
  console.log('Tutoría a eliminar:', tutoriaAEliminar.value)
  showModalEliminarTutoria.value = true
  correoConfirmacion.value = ''
  errorModalEliminar.value = null
}

const cerrarModalEliminar = () => {
  if (!isDeleting.value) {
    showModalEliminarTutoria.value = false
    tutoriaAEliminar.value = null
    correoConfirmacion.value = ''
    errorModalEliminar.value = null
  }
}

const eliminarTutoria = async () => {
  errorModalEliminar.value = null

  // Validar que el correo coincida
  if (correoConfirmacion.value.trim().toLowerCase() !== tutor.value.correo.trim().toLowerCase()) {
    errorModalEliminar.value = 'El correo ingresado no coincide con tu correo registrado'
    return
  }

  if (!tutoriaAEliminar.value?.tutoringId) {
    errorModalEliminar.value = 'No se puede eliminar esta tutoría. ID no disponible.'
    return
  }

  isDeleting.value = true

  try {
    const token = localStorage.getItem('accessToken')
    const response = await axios.delete(
      `http://localhost:8000/api/tutorias/${tutoriaAEliminar.value.tutoringId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )

    if (response.status === 200 || response.status === 204) {
      error.value = null
      // Mostrar mensaje de éxito
      alert(`✅ Tutoría de ${tutoriaAEliminar.value.name} eliminada exitosamente`)

      cerrarModalEliminar()
      await fetchAssignedStudents(currentPage.value) // Recargar lista
    }
  } catch (err) {
    console.error('Error al eliminar tutoría:', err)
    if (err.response?.status === 404) {
      errorModalEliminar.value = 'La tutoría no fue encontrada. Puede que ya haya sido eliminada.'
    } else if (err.response?.status === 403) {
      errorModalEliminar.value = 'No tienes permisos para eliminar esta tutoría.'
    } else if (err.response?.data?.detail) {
      errorModalEliminar.value = err.response.data.detail
    } else {
      errorModalEliminar.value = 'Error al eliminar la tutoría. Intenta de nuevo.'
    }
  } finally {
    isDeleting.value = false
  }
}

// ==================== LIFECYCLE ====================
onMounted(async () => {
  await fetchCurrentTutor()
})
</script>

<style>
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

/* Animaciones para los círculos */
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
  animation: float-1 4s ease-in-out infinite;
}

.animate-float-2 {
  animation: float-2 6s ease-in-out infinite;
}

.animate-float-3 {
  animation: float-3 5s ease-in-out infinite;
}

/* Colores personalizados */
.bg-coral-300 {
  background-color: #ff9f92;
}
.bg-coral-400 {
  background-color: #ff8576;
}
.bg-coral-500 {
  background-color: #ff6b5b;
}
.bg-coral-600 {
  background-color: #ff5242;
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

.text-coral-600 {
  color: #ff5242;
}
.hover\:bg-coral-600:hover {
  background-color: #ff5242;
}
.hover\:text-coral-900:hover {
  color: #cc2d1d;
}
.bg-coral-50 {
  background-color: #fff1f0;
}
.border-coral-500 {
  border-color: #ff6b5b;
}
</style>
