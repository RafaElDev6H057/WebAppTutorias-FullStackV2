<template>
  <div class="min-h-screen bg-gray-50 relative overflow-hidden">
    <!-- Animated Circles -->
    <div class="absolute inset-0 pointer-events-none">
      <div
        v-for="(circle, index) in circles"
        :key="index"
        :class="[
          'absolute rounded-full opacity-20',
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

    <!-- Navigation Bar - RESPONSIVE -->
    <nav class="bg-gradient-to-r from-[#0A3B76] to-[#092F5C] border-b border-[#0A3B76] shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16 lg:h-20">
          <!-- Left Section: Logo + User Info -->
          <div class="flex items-center space-x-2 sm:space-x-4 flex-1 min-w-0">
            <div class="flex-shrink-0">
              <img
                class="h-10 w-10 sm:h-12 sm:w-12 border-2 border-white rounded-full"
                src="/EscudoITSF.png"
                alt="Escudo ITSF"
              />
            </div>
            <div class="min-w-0 flex-1">
              <div class="text-white font-semibold text-sm sm:text-base truncate">
                {{
                  alumno
                    ? `${alumno.nombre} ${alumno.apellido_p} ${alumno.apellido_m}`
                    : 'Cargando...'
                }}
              </div>
              <div class="text-lime-100 text-xs sm:text-sm">
                No. Control: {{ alumno?.num_control || 'Cargando...' }}
              </div>
            </div>
          </div>

          <!-- Desktop Navigation - Hidden on mobile -->
          <div class="hidden lg:flex items-center space-x-4">
            <span class="text-xl font-bold text-white">Sistema de Tutorías</span>

            <!-- Botón de Constancia (Condicional) -->
            <button
              v-if="estadoTutorias?.es_elegible"
              @click="descargarConstancia"
              :disabled="isDownloading"
              class="bg-white hover:bg-[#0A3B76]/10 text-[#0A3B76] font-medium px-4 py-2 rounded-lg flex items-center space-x-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg"
            >
              <svg
                v-if="isDownloading"
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
              <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              <span>{{ isDownloading ? 'Descargando...' : 'Descargar Constancia' }}</span>
            </button>

            <!-- Botón Cambiar Contraseña -->
            <button
              @click="openChangePasswordModal"
              class="bg-white hover:bg-[#0A3B76]/90 text-[#0A3B76] font-medium px-4 py-2 rounded-lg flex items-center space-x-2 transition-all duration-200 shadow-md hover:shadow-lg"
            >
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"
                />
              </svg>
              <span>Cambiar Contraseña</span>
            </button>

            <button
              @click="handleLogout"
              class="bg-red-700 hover:bg-red-800 text-white font-medium px-4 py-2 rounded-lg flex items-center space-x-2 transition-all duration-200 shadow-md hover:shadow-lg"
            >
              <span>Cerrar Sesión</span>
            </button>
          </div>

          <!-- Mobile Menu Button -->
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="lg:hidden inline-flex items-center justify-center p-2 rounded-md text-white hover:bg-lime-600 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
          >
            <svg
              v-if="!mobileMenuOpen"
              class="h-6 w-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
            <svg v-else class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        <!-- Mobile Menu Dropdown -->
        <Transition
          enter-active-class="transition ease-out duration-200"
          enter-from-class="opacity-0 -translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition ease-in duration-150"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 -translate-y-2"
        >
          <div v-if="mobileMenuOpen" class="lg:hidden pb-4 space-y-2">
            <!-- Título -->
            <div class="px-4 py-2 text-white font-bold text-center border-t border-lime-600 pt-4">
              Sistema de Tutorías
            </div>

            <!-- Botón de Constancia (Condicional) -->
            <button
              v-if="estadoTutorias?.es_elegible"
              @click="(descargarConstancia(), (mobileMenuOpen = false))"
              :disabled="isDownloading"
              class="w-full mx-4 bg-white hover:bg-lime-50 text-lime-700 font-medium px-4 py-2 rounded-lg flex items-center justify-center space-x-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-md"
              style="max-width: calc(100% - 2rem)"
            >
              <svg
                v-if="isDownloading"
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
              <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              <span>{{ isDownloading ? 'Descargando...' : 'Descargar Constancia' }}</span>
            </button>

            <!-- Botón Cambiar Contraseña -->
            <button
              @click="(openChangePasswordModal(), (mobileMenuOpen = false))"
              class="w-full mx-4 bg-white hover:bg-lime-50 text-lime-700 font-medium px-4 py-2 rounded-lg flex items-center justify-center space-x-2 transition-all duration-200 shadow-md"
              style="max-width: calc(100% - 2rem)"
            >
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"
                />
              </svg>
              <span>Cambiar Contraseña</span>
            </button>

            <!-- Botón Cerrar Sesión -->
            <button
              @click="(handleLogout(), (mobileMenuOpen = false))"
              class="w-full mx-4 bg-lime-700 hover:bg-lime-800 text-white font-medium px-4 py-2 rounded-lg flex items-center justify-center space-x-2 transition-all duration-200 shadow-md"
              style="max-width: calc(100% - 2rem)"
            >
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                />
              </svg>
              <span>Cerrar Sesión</span>
            </button>
          </div>
        </Transition>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:py-12 px-4 sm:px-6 lg:px-8 relative z-10">
      <h1 class="text-2xl sm:text-3xl font-bold text-gray-800 mb-6 sm:mb-8">Mis Tutorías</h1>

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
          v-if="alumno?.requires_password_change"
          class="mb-6 p-4 bg-gray-50 border-l-4 border-gray-500 rounded-md shadow-sm"
        >
          <div class="flex items-start">
            <svg
              class="w-6 h-6 text-gray-600 mr-3 flex-shrink-0"
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
              <h3 class="text-sm font-medium text-gray-800">Contraseña Insegura</h3>
              <p class="mt-1 text-sm text-gray-700">
                Tu contraseña actual no está protegida adecuadamente. Por seguridad, te recomendamos
                cambiarla lo antes posible.
              </p>
              <button
                @click="openChangePasswordModal"
                class="mt-3 text-sm font-medium text-gray-700 hover:text-gray-900 underline"
              >
                Cambiar contraseña ahora →
              </button>
            </div>
          </div>
        </div>
      </Transition>

      <!-- ==================== AVISOS IMPORTANTES ==================== -->
      <div class="mb-6 sm:mb-8">
        <AvisosAlumno />
      </div>

      <!-- Mensaje de Constancia no disponible -->
      <Transition
        enter-active-class="transition ease-out duration-300"
        enter-from-class="opacity-0 translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-200"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="estadoTutorias && !estadoTutorias.es_elegible"
          class="mb-6 bg-gray-50 border-l-4 border-gray-500 p-4 rounded-md shadow-sm"
        >
          <div class="flex items-start">
            <svg
              class="w-6 h-6 text-gray-600 mr-3 flex-shrink-0"
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
              <h3 class="text-sm font-bold text-[#0A3B76] mb-1">📄 Constancia no disponible</h3>
              <p class="text-sm text-[#092F5C]">
                Debes completar tus <strong>4 tutorías</strong> para poder descargar tu constancia
                de acreditación.
              </p>
              <div class="mt-2 flex items-center">
                <div class="flex-1 bg-gray-200 rounded-full h-2 mr-3">
                  <div
                    class="bg-gradient-to-r from-[#0A3B76] to-[#092F5C] h-2 rounded-full transition-all duration-500"
                    :style="{
                      width: `${(estadoTutorias.tutorias_completadas / 4) * 100}%`,
                    }"
                  ></div>
                </div>
                <span class="text-xs font-bold text-[#092F5C]">
                  {{ estadoTutorias.tutorias_completadas }} / 4 completadas
                </span>
              </div>
            </div>
          </div>
        </div>
      </Transition>

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
          v-if="successMessage"
          class="mb-6 bg-gray-50 border-l-4 border-[#0A3B76] p-4 rounded-md shadow-sm"
        >
          <div class="flex items-start">
            <svg
              class="w-6 h-6 text-[#0A3B76] mr-3 flex-shrink-0"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <div class="flex-1">
              <p class="text-sm font-medium text-[#092F5C]">{{ successMessage }}</p>
            </div>
            <button @click="successMessage = null" class="text-[#0A3B76] hover:text-[#092F5C]">
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
        </div>
      </Transition>

      <!-- Cards de Tutorías -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <div
          v-for="tutoria in sortedTutorias"
          :key="tutoria.semestre"
          :class="[
            'bg-white rounded-lg p-4 sm:p-6 border-l-4 shadow-md hover:shadow-xl transition-all duration-300',
            {
              'border-[#0A3B76]': tutoria.estado === 'completada',
              'border-gray-500': tutoria.estado === 'en curso',
              'border-red-500': tutoria.estado === 'pendiente',
            },
          ]"
        >
          <div class="flex justify-between items-start mb-4">
            <h2 class="text-lg sm:text-xl font-semibold text-gray-800">
              Semestre {{ tutoria.semestre }}
            </h2>
            <span
              :class="[
                'px-3 py-1 text-xs font-semibold rounded-full',
                {
                  'bg-[#0A3B76] text-white': tutoria.estado === 'completada',
                  'bg-gray-200 text-gray-800': tutoria.estado === 'en curso',
                  'bg-red-100 text-red-700': tutoria.estado === 'pendiente',
                },
              ]"
            >
              {{
                tutoria.estado === 'completada'
                  ? 'Acreditado'
                  : tutoria.estado === 'en curso'
                    ? 'En curso'
                    : 'Pendiente'
              }}
            </span>
          </div>
          <div class="space-y-3">
            <div class="text-gray-600">
              <p class="text-sm font-medium text-gray-500">Tutor</p>
              <p class="text-gray-800 text-sm sm:text-base">
                {{ getTutorName(tutoria) || 'Por asignar' }}
              </p>
            </div>
            <div class="text-gray-600">
              <p class="text-sm font-medium text-gray-500">Periodo</p>
              <p class="text-gray-800 text-sm sm:text-base">{{ tutoria.periodo || 'Pendiente' }}</p>
            </div>
            <div class="text-gray-600">
              <p class="text-sm font-medium text-gray-500">Día</p>
              <p class="text-gray-800 text-sm sm:text-base">
                {{ capitalize(tutoria) || 'Pendiente' }}
              </p>
            </div>
            <div class="text-gray-600">
              <p class="text-sm font-medium text-gray-500">Hora</p>
              <p class="text-gray-800 text-sm sm:text-base">
                {{ formatoHora(tutoria) || 'Pendiente' }}
              </p>
            </div>
          </div>
          <button
            v-if="showSolicitarButton(tutoria)"
            @click="solicitarTutoria(tutoria.semestre)"
            class="w-full mt-4 bg-[#0A3B76] hover:bg-[#092F5C] text-white font-medium px-4 py-2 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2 shadow-md hover:shadow-lg text-sm sm:text-base"
          >
            <span>Solicitar Tutoría</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
        </div>
      </div>
    </main>

    <!-- ==================== MODAL CAMBIAR CONTRASEÑA ==================== -->
    <!-- (El resto del código del modal permanece igual) -->
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
        class="fixed inset-0 bg-gray-900 bg-opacity-75 overflow-y-auto h-full w-full z-50 flex items-center justify-center p-4"
      >
        <div class="relative w-full max-w-md bg-white rounded-lg shadow-2xl border border-gray-200">
          <div class="bg-[#0A3B76] px-6 py-4 rounded-t-lg flex justify-between items-center">
            <h2 class="text-xl font-semibold text-white flex items-center gap-2">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"
                />
              </svg>
              Cambiar Contraseña
            </h2>
            <button
              @click="closeChangePasswordModal"
              :disabled="isChangingPassword"
              class="text-white hover:text-lime-100 disabled:opacity-50 transition-colors"
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

          <div class="p-6">
            <!-- Mensaje de advertencia para primera vez -->
            <div
              v-if="alumno?.requires_password_change"
              class="mb-4 p-3 bg-amber-50 border border-amber-200 rounded-md"
            >
              <p class="text-sm text-amber-800">
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
                class="mb-4 p-3 bg-green-50 border-l-4 border-green-500 rounded-md"
              >
                <div class="flex items-center">
                  <svg
                    class="w-5 h-5 text-green-600 mr-2"
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
                class="mb-4 p-3 bg-red-50 border-l-4 border-red-500 rounded-md"
              >
                <div class="flex items-start">
                  <svg
                    class="w-5 h-5 text-red-600 mr-2 flex-shrink-0 mt-0.5"
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
              <!-- Campo de Número de Control (solo para primera vez) -->
              <div v-if="alumno?.requires_password_change">
                <label for="num_control" class="block text-sm font-medium text-gray-700 mb-1">
                  Número de Control
                </label>
                <input
                  id="num_control"
                  v-model="passwordForm.num_control"
                  type="text"
                  required
                  :disabled="isChangingPassword"
                  class="w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-lime-500 focus:border-lime-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                  placeholder="Tu número de control"
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
                    v-model="passwordForm.currentPassword"
                    :type="showCurrentPassword ? 'text' : 'password'"
                    required
                    :disabled="isChangingPassword"
                    class="w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-lime-500 focus:border-lime-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    @click="showCurrentPassword = !showCurrentPassword"
                    class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 transition-colors"
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
                    class="w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-lime-500 focus:border-lime-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    @click="showNewPassword = !showNewPassword"
                    class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 transition-colors"
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
                <label for="confirm-password" class="block text-sm font-medium text-gray-700 mb-1">
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
                    class="w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-lime-500 focus:border-lime-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    @click="showConfirmPassword = !showConfirmPassword"
                    class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 transition-colors"
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
              <div class="flex gap-3 pt-4 border-t">
                <button
                  type="button"
                  @click="closeChangePasswordModal"
                  :disabled="isChangingPassword"
                  class="flex-1 px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-[#0A3B76] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  :disabled="isChangingPassword"
                  class="flex-1 px-4 py-2 bg-[#0A3B76] hover:from-[#092F5C] hover:to-[#8C8D8F] border border-transparent rounded-md text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-[#0A3B76] disabled:opacity-50 disabled:cursor-not-allowed transition-all inline-flex justify-center items-center"
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
      </div>
    </Transition>

    <!-- Modal de confirmación de tutoría -->
    <div
      v-if="mostrarModal"
      class="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center z-50 p-4"
    >
      <div class="bg-white p-6 rounded-lg shadow-xl max-w-md w-full">
        <h3 class="text-xl font-bold text-gray-900 mb-4">Solicitud de Tutoría</h3>
        <p class="text-gray-700 mb-6">
          Su solicitud para la tutoría del Semestre {{ semestreSolicitado }} ha sido enviada al
          administrador. Se le notificará cuando sea aprobada.
        </p>
        <button
          @click="cerrarModal"
          class="w-full bg-lime-500 hover:bg-lime-600 text-white font-medium px-4 py-2 rounded-lg transition-colors duration-200"
        >
          Entendido
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { alumnosAPI } from '@/api/alumnos'
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import AvisosAlumno from '@/components/student/AvisosAlumno.vue'

// ==================== STATE - GENERAL ====================
const mostrarModal = ref(false)
const semestreSolicitado = ref(null)
const alumno = ref(null)
const tutorias = ref([])
const estadoTutorias = ref(null)
const isDownloading = ref(false)
const successMessage = ref(null)
const errorMessage = ref(null)
const router = useRouter()
const mobileMenuOpen = ref(false) // ✅ NUEVO: Estado del menú móvil

// ==================== STATE - CAMBIO DE CONTRASEÑA ====================
const showChangePasswordModal = ref(false)
const isChangingPassword = ref(false)
const passwordChangeError = ref(null)
const passwordChangeSuccess = ref(false)
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

const passwordForm = ref({
  num_control: '',
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})

// ==================== (El resto del código JavaScript permanece igual) ====================
// ... (todas las funciones fetchAlumnoData, fetchEstadoTutorias, etc.)

// ==================== API CALLS - ALUMNO ====================
const fetchAlumnoData = async () => {
  try {
    const response = await alumnosAPI.getMe()

    alumno.value = response.data
    console.log('✅ Datos del alumno cargados:', alumno.value)
  } catch (error) {
    console.error('❌ Error al obtener datos del alumno:', error)

    // El interceptor ya maneja el 401/403 y redirige automáticamente
    // Solo manejamos otros errores
    if (error.response?.status !== 401 && error.response?.status !== 403) {
      errorMessage.value = 'Error al cargar tus datos. Por favor, intenta de nuevo.'
    }
  }
}

const fetchEstadoTutorias = async () => {
  try {
    const response = await alumnosAPI.getEstadoTutorias()
    estadoTutorias.value = response.data
  } catch (error) {
    console.error('❌ Error al obtener estado de tutorías:', error)
  }
}

const fetchTutorias = async () => {
  try {
    if (!alumno.value?.id_alumno) {
      console.error('No se puede obtener tutorías sin id_alumno')
      return
    }

    const response = await axios.get(
      `http://localhost:8000/api/tutorias/alumno/${alumno.value.id_alumno}`,
    )

    tutorias.value = response.data
    console.log('✅ Tutorías cargadas:', tutorias.value)
  } catch (error) {
    console.error('❌ Error al obtener las tutorías:', error)
    errorMessage.value = 'Error al cargar tus tutorías.'
  }
}

const descargarConstancia = async () => {
  try {
    isDownloading.value = true
    errorMessage.value = null

    const response = await alumnosAPI.getConstanciaPDF()

    // Crear blob y descargar
    const blob = new Blob([response.data], { type: 'application/pdf' })
    const url = window.URL.createObjectURL(blob)

    const link = document.createElement('a')
    link.href = url
    link.download = `Constancia_${alumno.value.nombre}_${alumno.value.num_control}.pdf`
    document.body.appendChild(link)
    link.click()

    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    successMessage.value = '✅ Constancia descargada exitosamente'
    setTimeout(() => {
      successMessage.value = null
    }, 3000)

    console.log('✅ PDF descargado exitosamente')
  } catch (error) {
    console.error('❌ Error al descargar constancia:', error)

    if (error.response?.status === 404) {
      errorMessage.value = 'No se encontró tu constancia. Contacta al administrador.'
    } else if (error.response?.status === 403) {
      errorMessage.value =
        'No tienes permisos para descargar la constancia. Completa tus 4 tutorías.'
    } else {
      errorMessage.value = 'Error al generar la constancia. Intenta de nuevo.'
    }
  } finally {
    isDownloading.value = false
  }
}

// ==================== PASSWORD CHANGE HANDLERS ====================
const openChangePasswordModal = () => {
  showChangePasswordModal.value = true
  passwordChangeError.value = null
  passwordChangeSuccess.value = false
  passwordForm.value = {
    num_control: alumno.value?.num_control || '',
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  }
}

const closeChangePasswordModal = () => {
  if (!isChangingPassword.value) {
    showChangePasswordModal.value = false
    passwordForm.value = {
      num_control: alumno.value?.num_control || '',
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

  // Validaciones
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    passwordChangeError.value = 'Las contraseñas no coinciden.'
    return
  }

  if (passwordForm.value.newPassword.length < 8) {
    passwordChangeError.value = 'La nueva contraseña debe tener al menos 8 caracteres.'
    return
  }

  if (alumno.value.requires_password_change && !passwordForm.value.num_control) {
    passwordChangeError.value = 'El número de control es requerido.'
    return
  }

  isChangingPassword.value = true

  try {
    let response

    if (alumno.value.requires_password_change) {
      // Primera vez - usar setPassword
      response = await alumnosAPI.setPassword({
        num_control: passwordForm.value.num_control,
        contraseña_actual: passwordForm.value.currentPassword,
        nueva_contraseña: passwordForm.value.newPassword,
      })
    } else {
      // Cambio normal - usar changePassword
      response = await alumnosAPI.changePassword({
        contraseña_actual: passwordForm.value.currentPassword,
        nueva_contraseña: passwordForm.value.newPassword,
      })
    }

    if (response.status === 200) {
      passwordChangeSuccess.value = true

      if (alumno.value.requires_password_change) {
        alumno.value.requires_password_change = false
      }

      setTimeout(() => {
        closeChangePasswordModal()
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

// ==================== COMPUTED ====================
const sortedTutorias = computed(() => {
  return [...tutorias.value].sort((a, b) => a.semestre - b.semestre)
})

// ==================== HELPER FUNCTIONS ====================
const getTutorName = (tutoria) => {
  if (tutoria.tutor) {
    return `${tutoria.tutor.nombre} ${tutoria.tutor.apellido_p} ${tutoria.tutor.apellido_m}`
  }
  return 'Por asignar'
}

const capitalize = (tutoria) => {
  if (tutoria.dia != null) {
    return tutoria.dia.charAt(0).toUpperCase() + tutoria.dia.slice(1)
  }
  return null
}

const formatoHora = (tutoria) => {
  if (tutoria.hora != null) {
    /* eslint-disable-next-line no-unused-vars */
    const [horas, minutos, segundos] = tutoria.hora.split(':').map(Number)
    const ampm = horas < 12 ? 'AM' : 'PM'
    const horaFormateada = `${horas % 12 || 12}:${minutos.toString().padStart(2, '0')} ${ampm}`
    return horaFormateada
  }
  return null
}

const showSolicitarButton = (tutoria) => {
  const index = sortedTutorias.value.findIndex((t) => t.semestre === tutoria.semestre)
  const previousTutorias = sortedTutorias.value.slice(0, index)
  const allPreviousCompleted = previousTutorias.every((t) => t.estado === 'completada')
  return tutoria.estado === 'pendiente' && allPreviousCompleted
}

const handleLogout = () => {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('alumno')
  router.push('/')
}

const solicitarTutoria = (semestre) => {
  console.log(`Solicitando tutoría para el Semestre ${semestre}`)
  semestreSolicitado.value = semestre
  mostrarModal.value = true
}

const cerrarModal = () => {
  mostrarModal.value = false
}

// ==================== LIFECYCLE ====================
onMounted(async () => {
  await fetchAlumnoData()

  if (alumno.value) {
    await Promise.all([fetchTutorias(), fetchEstadoTutorias()])
  }
})

// ==================== CIRCLES ANIMATION ====================
const circles = [
  { color: 'bg-lime-400', size: 96, top: 10, left: 5 },
  { color: 'bg-lime-300', size: 64, top: 20, left: 80 },
  { color: 'bg-lime-500', size: 128, top: 70, left: 20 },
  { color: 'bg-lime-200', size: 80, top: 40, left: 95 },
  { color: 'bg-lime-600', size: 112, top: 85, left: 70 },
  { color: 'bg-lime-300', size: 48, top: 25, left: 30 },
  { color: 'bg-lime-400', size: 72, top: 60, left: 50 },
  { color: 'bg-lime-200', size: 56, top: 5, left: 90 },
  { color: 'bg-lime-500', size: 88, top: 80, left: 40 },
  { color: 'bg-lime-300', size: 40, top: 90, left: 10 },
  { color: 'bg-lime-600', size: 104, top: 15, left: 60 },
  { color: 'bg-lime-400', size: 68, top: 50, left: 85 },
  { color: 'bg-lime-300', size: 52, top: 5, left: 15 },
  { color: 'bg-lime-500', size: 60, top: 10, left: 50 },
  { color: 'bg-lime-400', size: 100, top: 55, left: 10 },
  { color: 'bg-lime-600', size: 90, top: 65, left: 85 },
  { color: 'bg-lime-500', size: 76, top: 80, left: 15 },
  { color: 'bg-lime-200', size: 44, top: 35, left: 60 },
  { color: 'bg-lime-400', size: 84, top: 25, left: 10 },
  { color: 'bg-lime-500', size: 50, top: 45, left: 75 },
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
  animation: float-1 4s ease-in-out infinite;
}

.animate-float-2 {
  animation: float-2 6s ease-in-out infinite;
}

.animate-float-3 {
  animation: float-3 5s ease-in-out infinite;
}
</style>
