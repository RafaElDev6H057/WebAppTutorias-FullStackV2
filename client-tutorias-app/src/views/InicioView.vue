<template>
  <div class="flex flex-col min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <!-- Header con navegación -->
    <header class="border-b border-gray-100 shadow-sm bg-white flex-shrink-0">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center w-11/12">
        <div class="flex items-center space-x-3">
          <img src="/EscudoITSF.png" alt="Escudo ITSF" class="h-14 w-auto" />
          <div class="hidden md:block">
            <h1 class="text-lg font-semibold text-gray-800">
              Instituto Tecnológico Superior de Fresnillo
            </h1>
            <p class="text-sm text-gray-600">Educación de calidad para el futuro</p>
          </div>
        </div>
        <div class="flex items-center">
          <button
            class="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700 transition-colors"
          >
            Contacto
          </button>
        </div>
      </div>
    </header>

    <!-- Hero Section - Flex-grow para ocupar el espacio disponible -->
    <section
      class="relative overflow-hidden bg-gradient-to-r from-green-50 via-blue-50 to-green-50 flex-grow flex items-center"
    >
      <div class="container mx-auto px-4 py-8 w-11/12">
        <div class="grid lg:grid-cols-2 gap-12 items-center">
          <!-- Contenido izquierdo -->
          <div class="space-y-8 z-10">
            <div class="space-y-4 max-w-xl">
              <div
                class="inline-block px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium"
              >
                Sistema Institucional
              </div>
              <h2 class="text-4xl md:text-5xl font-bold text-gray-900">
                Área de
                <span
                  class="text-transparent bg-clip-text bg-gradient-to-r from-green-600 to-blue-600"
                >
                  Tutorías
                </span>
              </h2>
              <p class="text-xl text-gray-600 leading-relaxed">
                Un espacio diseñado para fortalecer tu desarrollo académico y personal a través de
                acompañamiento especializado.
              </p>
            </div>

            <!-- ==================== SECCIÓN 1: ACCESO GENERAL ==================== -->
            <div class="space-y-4">
              <div class="flex items-center gap-2">
                <div
                  class="h-1 w-12 bg-gradient-to-r from-green-600 to-blue-600 rounded-full"
                ></div>
                <h3 class="text-lg font-bold text-gray-800">Acceso General</h3>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <InicioRolCard
                  :icono="AdminLogo"
                  titulo="Administrador"
                  descripcion="Gestión y supervisión del sistema"
                  ruta="/login_admin"
                  color="purple"
                />

                <InicioRolCard
                  :icono="TutorLogo"
                  titulo="Tutor"
                  descripcion="Impartir y gestionar tutorías"
                  ruta="/login_tutor"
                  color="blue"
                />

                <InicioRolCard
                  :icono="AlumnoLogo"
                  titulo="Alumno"
                  descripcion="Accede a tus tutorías"
                  ruta="/login_alumno"
                  color="green"
                />
              </div>
            </div>

            <!-- ==================== SECCIÓN 2: ACCESO DEPARTAMENTOS ==================== -->
            <div class="space-y-4">
              <div class="flex items-center gap-2">
                <div
                  class="h-1 w-12 bg-gradient-to-r from-orange-500 to-pink-500 rounded-full"
                ></div>
                <h3 class="text-lg font-bold text-gray-800">Acceso Departamental</h3>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <InicioRolCard
                  :icono="PsicologiaLogo"
                  titulo="Psicología"
                  descripcion="Área de desarrollo estudiantil"
                  ruta="/login_departamento/psicologia"
                  color="teal"
                  :isDepartamento="true"
                />

                <InicioRolCard
                  :icono="CienciasLogo"
                  titulo="Ciencias Básicas"
                  descripcion="Departamento académico"
                  ruta="/login_departamento/ciencias"
                  color="indigo"
                  :isDepartamento="true"
                />

                <InicioRolCard
                  :icono="JefaturaLogo"
                  titulo="Jefatura Académica"
                  descripcion="Coordinación académica"
                  ruta="/login_departamento/jefatura"
                  color="rose"
                  :isDepartamento="true"
                />
              </div>
            </div>
          </div>

          <!-- Contenido derecho -->
          <div class="relative hidden lg:block">
            <div
              class="relative z-10 rounded-xl overflow-hidden shadow-2xl transform hover:scale-[1.01] transition-transform duration-300"
            >
              <img
                src="/logoITSF.jpg"
                alt="Ilustración del área de tutorías"
                class="w-full h-auto object-cover"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent"></div>
            </div>

            <!-- Decoración de fondo -->
            <div
              class="absolute -top-20 -right-20 w-64 h-64 bg-green-200 rounded-full mix-blend-multiply filter blur-3xl opacity-50"
            ></div>
            <div
              class="absolute -bottom-20 -left-20 w-64 h-64 bg-blue-200 rounded-full mix-blend-multiply filter blur-3xl opacity-50"
            ></div>
          </div>
        </div>
      </div>

      <!-- Decoración de fondo -->
      <div class="absolute top-0 left-0 w-full h-full overflow-hidden z-0 opacity-10">
        <div
          class="absolute -top-10 -right-10 w-40 h-40 border-4 border-green-200 rounded-full"
        ></div>
        <div class="absolute top-40 left-20 w-20 h-20 border-4 border-blue-200 rounded-full"></div>
        <div
          class="absolute bottom-20 right-40 w-30 h-30 border-4 border-green-200 rounded-full"
        ></div>
      </div>
    </section>

    <!-- Footer - Siempre pegado al fondo -->
    <footer class="bg-gray-900 text-white py-6 flex-shrink-0">
      <div class="container mx-auto px-4 w-11/12">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <div class="flex items-center space-x-3 mb-4 md:mb-0">
            <img src="/EscudoITSF.png" alt="Escudo ITSF" class="h-10 w-auto" />
            <div>
              <h3 class="font-semibold">ITSF</h3>
              <p class="text-sm text-gray-400">
                Tecnológico Nacional de México Campus Fresnillo {{ new Date().getFullYear() }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import InicioRolCard from '@/components/InicioRolCard.vue'
import AdminLogo from '@/components/icons/AdminLogo.vue'
import TutorLogo from '@/components/icons/TutorLogo.vue'
import AlumnoLogo from '@/components/icons/AlumnoLogo.vue'
import PsicologiaLogo from '@/components/icons/PsicologiaLogo.vue'
import CienciasLogo from '@/components/icons/CienciasLogo.vue'
import JefaturaLogo from '@/components/icons/JefaturaLogo.vue'
</script>

<style scoped>
/* Animaciones sutiles para elementos interactivos */
@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0px);
  }
}

.float-animation {
  animation: float 6s ease-in-out infinite;
}
</style>
