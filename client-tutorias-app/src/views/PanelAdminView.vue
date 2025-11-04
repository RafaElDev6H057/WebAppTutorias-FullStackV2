<template>
  <!-- ==================== CONTAINER PRINCIPAL ==================== -->
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-white relative overflow-hidden">
    <!-- ==================== ANIMATED CIRCLES (FONDO) ==================== -->
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

    <!-- ==================== BARRA DE NAVEGACIÓN ==================== -->
    <nav class="bg-purple-600 shadow-lg relative z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <img class="h-12 w-12 border-2 border-white" src="/EscudoITSF.png" alt="Escudo ITSF" />
            <div class="ml-4">
              <div class="text-lg font-medium text-white">Administrador</div>
              <div class="text-sm text-indigo-200">Instituto Tecnológico Superior de Fresnillo</div>
            </div>
          </div>
          <div class="flex items-center">
            <button
              @click="handleLogout"
              class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium transition duration-150 ease-in-out"
            >
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- ==================== CONTENIDO PRINCIPAL ==================== -->
    <main class="max-w-[1400px] mx-auto py-6 sm:px-6 lg:px-8 relative z-10">
      <div class="px-4 py-6 sm:px-0">
        <h1 class="text-3xl font-bold text-gray-900 mb-8">Panel de Administración</h1>

        <!-- ==================== CONTROL DE ETAPAS - REPORTE INTEGRAL ==================== -->
        <div class="mb-8 bg-white rounded-lg shadow-md p-6 border-l-4 border-indigo-500">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h2 class="text-xl font-bold text-gray-900 flex items-center gap-2">
                <svg
                  class="w-6 h-6 text-indigo-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"
                  />
                </svg>
                Control de Etapas - Reporte Integral
              </h2>
              <p class="text-sm text-gray-600 mt-1">
                Controla qué campos pueden llenar los tutores en el Reporte Integral
              </p>
            </div>

            <!-- Etapa Actual -->
            <div v-if="!isLoadingEtapa" class="text-right">
              <p class="text-sm text-gray-600">Etapa Actual:</p>
              <div class="flex items-center gap-2 mt-1">
                <span
                  :class="[
                    'px-4 py-2 rounded-full font-bold text-lg',
                    {
                      'bg-gray-200 text-gray-700': reporteIntegralEtapa === 0,
                      'bg-yellow-100 text-yellow-800': reporteIntegralEtapa === 1,
                      'bg-blue-100 text-blue-800': reporteIntegralEtapa === 2,
                      'bg-green-100 text-green-800': reporteIntegralEtapa === 3,
                    },
                  ]"
                >
                  {{ reporteIntegralEtapa === 0 ? 'Bloqueado' : `Etapa ${reporteIntegralEtapa}` }}
                </span>
              </div>
            </div>
          </div>

          <!-- Mensajes de éxito/error -->
          <Transition
            enter-active-class="transition ease-out duration-200"
            enter-from-class="opacity-0 translate-y-1"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition ease-in duration-150"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
          >
            <div
              v-if="successEtapa"
              class="mb-4 p-3 bg-green-50 border-l-4 border-green-500 rounded"
            >
              <p class="text-sm text-green-800 font-medium">{{ successEtapa }}</p>
            </div>
          </Transition>

          <Transition
            enter-active-class="transition ease-out duration-200"
            enter-from-class="opacity-0 translate-y-1"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition ease-in duration-150"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
          >
            <div v-if="errorEtapa" class="mb-4 p-3 bg-red-50 border-l-4 border-red-500 rounded">
              <p class="text-sm text-red-800 font-medium">{{ errorEtapa }}</p>
            </div>
          </Transition>

          <!-- Botones de Etapas -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <!-- Botón Etapa 1 -->
            <button
              @click="cambiarEtapa(1)"
              :disabled="isLoadingEtapa"
              :class="[
                'p-4 rounded-lg border-2 transition-all duration-200 text-left',
                reporteIntegralEtapa === 1
                  ? 'border-yellow-500 bg-yellow-50 shadow-md'
                  : 'border-gray-300 hover:border-yellow-400 hover:bg-yellow-50',
                isLoadingEtapa ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer',
              ]"
            >
              <div class="flex items-start gap-3">
                <div
                  :class="[
                    'flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg',
                    reporteIntegralEtapa === 1
                      ? 'bg-yellow-500 text-white'
                      : 'bg-gray-200 text-gray-600',
                  ]"
                >
                  1
                </div>
                <div class="flex-1">
                  <h3 class="font-bold text-gray-900 mb-1">Etapa 1</h3>
                  <p class="text-sm text-gray-600">Solo Seguimiento 1</p>
                  <div class="mt-2 flex items-center gap-2">
                    <svg class="w-4 h-4 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fill-rule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                        clip-rule="evenodd"
                      />
                    </svg>
                    <span class="text-xs text-gray-600">seguimiento_1</span>
                  </div>
                </div>
                <div v-if="reporteIntegralEtapa === 1" class="flex-shrink-0">
                  <svg class="w-6 h-6 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </div>
              </div>
            </button>

            <!-- Botón Etapa 2 -->
            <button
              @click="cambiarEtapa(2)"
              :disabled="isLoadingEtapa"
              :class="[
                'p-4 rounded-lg border-2 transition-all duration-200 text-left',
                reporteIntegralEtapa === 2
                  ? 'border-blue-500 bg-blue-50 shadow-md'
                  : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50',
                isLoadingEtapa ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer',
              ]"
            >
              <div class="flex items-start gap-3">
                <div
                  :class="[
                    'flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg',
                    reporteIntegralEtapa === 2
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-200 text-gray-600',
                  ]"
                >
                  2
                </div>
                <div class="flex-1">
                  <h3 class="font-bold text-gray-900 mb-1">Etapa 2</h3>
                  <p class="text-sm text-gray-600">Seguimientos 1 y 2</p>
                  <div class="mt-2 space-y-1">
                    <div class="flex items-center gap-2">
                      <svg class="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                        <path
                          fill-rule="evenodd"
                          d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                          clip-rule="evenodd"
                        />
                      </svg>
                      <span class="text-xs text-gray-600">seguimiento_1, seguimiento_2</span>
                    </div>
                  </div>
                </div>
                <div v-if="reporteIntegralEtapa === 2" class="flex-shrink-0">
                  <svg class="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </div>
              </div>
            </button>

            <!-- Botón Etapa 3 -->
            <button
              @click="cambiarEtapa(3)"
              :disabled="isLoadingEtapa"
              :class="[
                'p-4 rounded-lg border-2 transition-all duration-200 text-left',
                reporteIntegralEtapa === 3
                  ? 'border-green-500 bg-green-50 shadow-md'
                  : 'border-gray-300 hover:border-green-400 hover:bg-green-50',
                isLoadingEtapa ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer',
              ]"
            >
              <div class="flex items-start gap-3">
                <div
                  :class="[
                    'flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg',
                    reporteIntegralEtapa === 3
                      ? 'bg-green-500 text-white'
                      : 'bg-gray-200 text-gray-600',
                  ]"
                >
                  3
                </div>
                <div class="flex-1">
                  <h3 class="font-bold text-gray-900 mb-1">Etapa 3</h3>
                  <p class="text-sm text-gray-600">Todos los campos</p>
                  <div class="mt-2">
                    <div class="flex items-center gap-2">
                      <svg class="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                        <path
                          fill-rule="evenodd"
                          d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                          clip-rule="evenodd"
                        />
                      </svg>
                      <span class="text-xs text-gray-600">Reporte completo</span>
                    </div>
                  </div>
                </div>
                <div v-if="reporteIntegralEtapa === 3" class="flex-shrink-0">
                  <svg class="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </div>
              </div>
            </button>
          </div>

          <!-- Loader -->
          <div v-if="isLoadingEtapa" class="mt-4 flex items-center justify-center">
            <svg
              class="animate-spin h-6 w-6 text-indigo-600"
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
            <span class="ml-2 text-sm text-gray-600">Actualizando etapa...</span>
          </div>
        </div>

        <!-- ==================== GESTIÓN DE AVISOS ==================== -->
        <GestionAvisos class="mb-8" />

        <!-- ==================== PESTAÑAS (ESTUDIANTES/TUTORES) ==================== -->
        <div class="mb-8">
          <nav class="flex space-x-4" aria-label="Tabs">
            <button
              @click="activeTab = 'students'"
              :class="[
                activeTab === 'students'
                  ? 'bg-indigo-100 text-purple-700'
                  : 'text-gray-500 hover:text-gray-700',
                'px-3 py-2 font-medium text-sm rounded-md',
              ]"
            >
              Estudiantes
            </button>
            <button
              @click="activeTab = 'tutors'"
              :class="[
                activeTab === 'tutors'
                  ? 'bg-indigo-100 text-purple-700'
                  : 'text-gray-500 hover:text-gray-700',
                'px-3 py-2 font-medium text-sm rounded-md',
              ]"
            >
              Tutores
            </button>
          </nav>
        </div>

        <!-- ==================== PANEL DE ESTUDIANTES ==================== -->
        <div v-if="activeTab === 'students'">
          <p v-if="uploadMessage">{{ uploadMessage }}</p>

          <!-- Header con botones de acción -->
          <div class="mb-4 flex justify-between items-center">
            <h2 class="text-2xl font-bold text-gray-900">Gestión de Estudiantes</h2>
            <div class="flex items-center gap-4">
              <BaseSearchInput v-model="searchQuery" placeholder="Buscar Estudiante..." />

              <button
                @click="showModalExcel = true"
                class="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-md text-sm font-medium transition duration-150 ease-in-out"
              >
                Cargar Excel
              </button>
              <button
                @click="openModal('student')"
                class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium transition duration-150 ease-in-out"
              >
                Añadir Estudiante
              </button>

              <AssignmentUploader />
            </div>
          </div>

          <!-- Estado de carga -->
          <div v-if="loading" class="text-center text-gray-500">Cargando estudiantes...</div>

          <!-- Mensaje de error -->
          <div v-if="error" class="text-red-500 text-center">{{ error }}</div>

          <!-- Tabla de estudiantes -->
          <div class="bg-white shadow overflow-hidden sm:rounded-lg">
            <table
              v-if="students.length > 0"
              class="min-w-full divide-y divide-gray-200 table-fixed"
            >
              <thead class="bg-gray-50">
                <tr>
                  <th
                    class="w-3/12 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Nombre Completo
                  </th>
                  <th
                    class="w-2/12 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                  >
                    Número de Control
                  </th>
                  <th
                    class="w-1/12 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Semestre
                  </th>
                  <th
                    class="w-3/12 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Carrera
                  </th>
                  <th
                    class="w-1/12 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Estado
                  </th>
                  <th
                    class="w-2/12 px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="student in students" :key="student.id">
                  <td class="px-6 py-4 whitespace-nowrap overflow-hidden text-ellipsis">
                    <div
                      v-if="student.apellido_m != null"
                      class="text-sm font-medium text-gray-900"
                    >
                      {{ `${student.nombre} ${student.apellido_p} ${student.apellido_m}` }}
                    </div>
                    <div v-else class="text-sm font-medium text-gray-900">
                      {{ `${student.nombre} ${student.apellido_p}` }}
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">{{ student.num_control }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">{{ student.semestre_actual }}° Semestre</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap overflow-hidden text-ellipsis">
                    <div class="text-sm text-gray-900">{{ student.carrera }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      class="px-2 text-xs leading-5 font-semibold rounded-full flex justify-center"
                      :class="
                        student.estado === 'A'
                          ? 'bg-green-100 text-green-800'
                          : 'bg-red-100 text-red-800'
                      "
                    >
                      {{ student.estado }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div class="flex items-center">
                      <button
                        @click="editItem(student, 'student')"
                        class="text-white hover:bg-indigo-900 mr-2 px-2 py-1 bg-indigo-600 rounded-xl transition-colors duration-200"
                      >
                        <EditIcon />
                      </button>
                      <button
                        @click="deleteItem(student)"
                        class="text-white hover:bg-red-900 mr-2 px-2 py-1 rounded-xl bg-red-600 transition-colors duration-200"
                      >
                        <DeleteIcon />
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-if="!loading && students.length === 0" class="text-center text-gray-500">
              No hay estudiantes registrados.
            </div>
          </div>

          <!-- Paginación Estudiantes -->
          <div
            class="bg-white mt-2 rounded-xl px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6"
          >
            <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p class="text-sm text-gray-700">
                  Mostrando
                  <span class="font-medium">{{ (currentPage - 1) * itemsPerPage + 1 }}</span>
                  a
                  <span class="font-medium">{{ Math.min(currentPage * itemsPerPage) }}</span>
                  de
                  <span class="font-medium">{{ totalStudents }}</span>
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
                    :disabled="currentPage === 1"
                    class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-black hover:bg-gray-50"
                  >
                    <svg
                      class="h-5 w-5"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                    <span>Anterior</span>
                  </button>

                  <button
                    @click="nextPage"
                    :disabled="!hayMasAlumnos"
                    class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-black hover:bg-gray-50"
                  >
                    <span>Siguiente</span>
                    <svg
                      class="h-5 w-5"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 20 20"
                      fill="currentColor"
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
        </div>
        <!-- ==================== PANEL DE TUTORES ==================== -->
        <div v-if="activeTab === 'tutors'">
          <!-- Header con botones de acción -->
          <div class="mb-4 flex justify-between items-center">
            <h2 class="text-2xl font-bold text-gray-900">Gestión de Tutores</h2>
            <div class="flex items-center gap-4">
              <BaseSearchInput v-model="searchQueryTutor" placeholder="Buscar Tutor..." />

              <button
                @click="openAssignmentModal"
                class="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-md text-sm font-medium transition duration-150 ease-in-out flex items-center gap-2"
              >
                <svg
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 4v16m8-8H4"
                  ></path>
                </svg>
                Asignar Tutorías
              </button>

              <AssignmentUploader
                :show="showAssignmentModal"
                @close="closeAssignmentModal"
                @success="handleAssignmentSuccess"
              />

              <button
                @click="openModal('tutor')"
                class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium transition duration-150 ease-in-out"
              >
                Añadir Tutor
              </button>
            </div>
          </div>

          <!-- Estado de carga -->
          <div v-if="loadingTutor" class="text-center text-gray-500">Cargando Tutores...</div>

          <!-- Mensaje de error -->
          <div v-if="errorTutor" class="text-red-500 text-center">{{ errorTutor }}</div>

          <!-- Tabla de tutores -->
          <div class="bg-white shadow overflow-hidden sm:rounded-lg">
            <table v-if="tutors.length > 0" class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Nombre Completo
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Correo
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Telefono
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Departamento
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="tutor in tutors" :key="tutor.id">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="ml-4">
                        <div class="text-sm font-medium text-gray-900">
                          {{ `${tutor.nombre} ${tutor.apellido_p} ${tutor.apellido_m}` }}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">{{ tutor.correo }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">---</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">---</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium flex">
                    <button
                      @click="editItem(tutor, 'tutor')"
                      class="text-white hover:bg-indigo-900 mr-2 px-2 py-1 bg-indigo-600 rounded-xl transition-colors duration-200"
                    >
                      <EditIcon />
                    </button>
                    <button
                      @click="deleteTutor(tutor)"
                      class="text-white hover:bg-red-900 mr-2 px-2 py-1 rounded-xl bg-red-600 transition-colors duration-200"
                    >
                      <DeleteIcon />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-if="tutors.length === 0 && !loadingTutor" class="text-center text-gray-500">
              No hay tutores registrados.
            </div>
          </div>

          <!-- Paginación Tutores -->
          <div
            class="bg-white mt-2 rounded-xl px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6"
          >
            <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p class="text-sm text-gray-700">
                  Mostrando
                  <span class="font-medium">{{
                    (currentPageTutor - 1) * itemsPerPageTutor + 1
                  }}</span>
                  a
                  <span class="font-medium">{{
                    Math.min(currentPageTutor * itemsPerPageTutor)
                  }}</span>
                  de
                  <span class="font-medium">{{ totalTutors }}</span>
                  resultados
                </p>
              </div>
              <div>
                <nav
                  class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
                  aria-label="Pagination"
                >
                  <button
                    @click="prevPageTutor"
                    :disabled="currentPageTutor === 1"
                    class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-black hover:bg-gray-50"
                  >
                    <svg
                      class="h-5 w-5"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                    <span>Anterior</span>
                  </button>

                  <button
                    @click="nextPageTutor"
                    :disabled="!hayMasTutores"
                    class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-black hover:bg-gray-50"
                  >
                    <span>Siguiente</span>
                    <svg
                      class="h-5 w-5"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 20 20"
                      fill="currentColor"
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
        </div>
      </div>
    </main>

    <!-- ==================== MODALES ==================== -->

    <!-- Modal para añadir/editar estudiante o tutor -->
    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="showModal"
        class="fixed z-10 inset-0 overflow-y-auto"
        aria-labelledby="modal-title"
        role="dialog"
        aria-modal="true"
      >
        <div
          class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
        >
          <div
            class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
            aria-hidden="true"
          ></div>
          <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true"
            >&#8203;</span
          >
          <div
            class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full"
          >
            <div class="bg-gradient-to-r from-purple-600 to-purple-700 px-4 py-3 sm:px-6">
              <h3 class="text-lg leading-6 font-medium text-white" id="modal-title">
                {{ modalMode === 'add' ? 'Añadir' : 'Editar' }}
                {{ modalType === 'student' ? 'Estudiante' : 'Tutor' }}
              </h3>
            </div>
            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <div class="mt-2">
                <form @submit.prevent="submitForm" class="space-y-6">
                  <div v-if="modalType === 'student'">
                    <div class="grid grid-cols-1 gap-6 sm:grid-cols-3">
                      <div>
                        <label for="nombre" class="block text-sm font-medium text-gray-700"
                          >Nombre</label
                        >
                        <input
                          type="text"
                          name="nombre"
                          id="nombre"
                          v-model="formData.nombre"
                          :class="[
                            'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                            { 'border-red-500': errors.nombre },
                          ]"
                        />
                        <p v-if="errors.nombre" class="mt-2 text-sm text-red-600">
                          {{ errors.nombre[0] }}
                        </p>
                      </div>
                      <div>
                        <label for="apellidoPaterno" class="block text-sm font-medium text-gray-700"
                          >Apellido Paterno</label
                        >
                        <input
                          type="text"
                          name="apellidoPaterno"
                          id="apellidoPaterno"
                          v-model="formData.apellido_p"
                          :class="[
                            'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                            { 'border-red-500': errors.apellido_p },
                          ]"
                        />
                        <p v-if="errors.apellido_p" class="mt-2 text-sm text-red-600">
                          {{ errors.apellido_p[0] }}
                        </p>
                      </div>
                      <div>
                        <label for="apellidoMaterno" class="block text-sm font-medium text-gray-700"
                          >Apellido Materno</label
                        >
                        <input
                          type="text"
                          name="apellidoMaterno"
                          id="apellidoMaterno"
                          v-model="formData.apellido_m"
                          :class="[
                            'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                            { 'border-red-500': errors.apellido_m },
                          ]"
                        />
                        <p v-if="errors.apellido_m" class="mt-2 text-sm text-red-600">
                          {{ errors.apellido_m[0] }}
                        </p>
                      </div>
                    </div>
                    <div class="mt-6">
                      <div class="grid grid-cols-2 gap-6">
                        <div>
                          <label for="numeroControl" class="block text-sm font-medium text-gray-700"
                            >Número de Control</label
                          >
                          <input
                            type="text"
                            name="numeroControl"
                            id="numeroControl"
                            v-model="formData.num_control"
                            :class="[
                              'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                              { 'border-red-500': errors.num_control },
                            ]"
                          />
                          <p v-if="errors.num_control" class="mt-2 text-sm text-red-600">
                            {{ errors.num_control[0] }}
                          </p>
                        </div>
                        <div>
                          <label for="contraseña" class="block text-sm font-medium text-gray-700"
                            >Contraseña</label
                          >
                          <div class="relative">
                            <input
                              name="contraseña"
                              id="contraseña"
                              v-model="formData.contraseña"
                              :type="showPassword ? 'text' : 'password'"
                              :class="[
                                'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                                { 'border-red-500': errors.contraseña },
                              ]"
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
                          <p v-if="errors.contraseña" class="mt-2 text-sm text-red-600">
                            {{ errors.contraseña[0] }}
                          </p>
                        </div>
                      </div>
                    </div>
                    <!-- Correo y contraseña -->
                    <div class="mt-6">
                      <div class="grid grid-cols-2 gap-6">
                        <div>
                          <label for="correo" class="block text-sm font-medium text-gray-700"
                            >Correo</label
                          >
                          <input
                            type="text"
                            name="correo"
                            id="correo"
                            v-model="formData.correo"
                            :class="[
                              'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                              { 'border-red-500': errors.correo },
                            ]"
                          />
                          <p v-if="errors.num_control" class="mt-2 text-sm text-red-600">
                            {{ errors.correo[0] }}
                          </p>
                        </div>
                        <div>
                          <label for="telefono" class="block text-sm font-medium text-gray-700"
                            >Telefono</label
                          >
                          <input
                            type="text"
                            name="telefono"
                            id="telefono"
                            v-model="formData.telefono"
                            :class="[
                              'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                              { 'border-red-500': errors.telefono },
                            ]"
                          />
                          <p v-if="errors.telefono" class="mt-2 text-sm text-red-600">
                            {{ errors.telefono[0] }}
                          </p>
                        </div>
                      </div>
                    </div>
                    <div class="mt-6">
                      <label for="carrera" class="block text-sm font-medium text-gray-700"
                        >Carrera</label
                      >
                      <select
                        name="carrera"
                        id="carrera"
                        v-model="formData.carrera"
                        :class="[
                          'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                          { 'border-red-500': errors.carrera },
                        ]"
                      >
                        <option value="">Selecciona una carrera</option>
                        <option value="Ingeniería en Semiconductores">
                          Ingeniería en Semiconductores
                        </option>
                        <option value="Ingeniería en Logística">Ingeniería en Logística</option>
                        <option value="Ingeniería en Informática">Ingeniería en Informática</option>
                        <option value="Ingeniería en Electrónica">Ingeniería en Electrónica</option>
                        <option value="Ingeniería en Sistemas Computacionales">
                          Ingeniería en Sistemas Computacionales
                        </option>
                        <option value="Ingeniería Ambiental">Ingeniería Ambiental</option>
                        <option value="Ingeniería Industrial">Ingeniería Industrial</option>
                        <option value="Ingeniería en Gestión Empresarial">
                          Ingeniería en Gestión Empresarial
                        </option>
                        <option value="Ingeniería en Minería">Ingeniería en Minería</option>
                        <option value="Arquitectura">Arquitectura</option>
                      </select>
                      <p v-if="errors.carrera" class="mt-2 text-sm text-red-600">
                        {{ errors.carrera[0] }}
                      </p>
                    </div>
                    <div class="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2">
                      <div>
                        <label for="semestre" class="block text-sm font-medium text-gray-700"
                          >Semestre</label
                        >
                        <select
                          name="semestre"
                          id="semestre"
                          v-model="formData.semestre_actual"
                          :class="[
                            'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                            { 'border-red-500': errors.semestre_actual },
                          ]"
                        >
                          <option value="">Selecciona un semestre</option>
                          <option value="1">1° Semestre</option>
                          <option value="2">2° Semestre</option>
                          <option value="3">3° Semestre</option>
                          <option value="4">4° Semestre</option>
                          <option value="5">5° Semestre</option>
                          <option value="6">6° Semestre</option>
                          <option value="7">7° Semestre</option>
                          <option value="8">8° Semestre</option>
                          <option value="9">9° Semestre</option>
                        </select>
                        <p v-if="errors.semestre_actual" class="mt-2 text-sm text-red-600">
                          {{ errors.semestre_actual[0] }}
                        </p>
                      </div>
                      <div>
                        <label for="estado" class="block text-sm font-medium text-gray-700"
                          >Estado</label
                        >
                        <select
                          name="estado"
                          id="estado"
                          v-model="formData.estado"
                          :class="[
                            'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                            { 'border-red-500': errors.estado },
                          ]"
                        >
                          <option value="A">Activo</option>
                          <option value="I">Inactivo</option>
                        </select>
                        <p v-if="errors.estado" class="mt-2 text-sm text-red-600">
                          {{ errors.estado[0] }}
                        </p>
                      </div>
                    </div>
                  </div>

                  <!-- Modal para añadir/editar tutor -->
                  <div v-if="modalType === 'tutor'">
                    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
                      <div class="col-span-2">
                        <label for="nombre" class="block text-sm font-medium text-gray-700"
                          >Nombre</label
                        >
                        <input
                          type="text"
                          name="nombre"
                          id="nombre"
                          v-model="formData.nombre"
                          :class="[
                            'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                            { 'border-red-500': errors.nombre },
                          ]"
                        />
                        <p v-if="errors.nombre" class="mt-2 text-sm text-red-600">
                          {{ errors.nombre[0] }}
                        </p>
                      </div>
                      <div>
                        <label for="apellidoPaterno" class="block text-sm font-medium text-gray-700"
                          >Apellido Paterno</label
                        >
                        <input
                          type="text"
                          name="apellidoPaterno"
                          id="apellidoPaterno"
                          v-model="formData.apellido_p"
                          :class="[
                            'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                            { 'border-red-500': errors.apellido_p },
                          ]"
                        />
                        <p v-if="errors.apellido_p" class="mt-2 text-sm text-red-600">
                          {{ errors.apellido_p[0] }}
                        </p>
                      </div>
                      <div>
                        <label for="apellidoMaterno" class="block text-sm font-medium text-gray-700"
                          >Apellido Materno</label
                        >
                        <input
                          type="text"
                          name="apellidoMaterno"
                          id="apellidoMaterno"
                          v-model="formData.apellido_m"
                          :class="[
                            'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                            { 'border-red-500': errors.apellido_m },
                          ]"
                        />
                        <p v-if="errors.apellido_m" class="mt-2 text-sm text-red-600">
                          {{ errors.apellido_m[0] }}
                        </p>
                      </div>
                      <div>
                        <label for="correo" class="block text-sm font-medium text-gray-700"
                          >Correo</label
                        >
                        <input
                          type="email"
                          name="correo"
                          id="correo"
                          v-model="formData.correo"
                          :class="[
                            'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                            { 'border-red-500': errors.correo },
                          ]"
                        />
                        <p v-if="errors.correo" class="mt-2 text-sm text-red-600">
                          {{ errors.correo[0] }}
                        </p>
                      </div>
                      <div>
                        <label for="contraseña" class="block text-sm font-medium text-gray-700"
                          >Contraseña</label
                        >
                        <div class="relative">
                          <input
                            name="contraseña"
                            id="contraseña"
                            v-model="formData.contraseña"
                            :type="showPassword ? 'text' : 'password'"
                            :class="[
                              'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                              { 'border-red-500': errors.contraseña },
                            ]"
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
                        <p v-if="errors.contraseña" class="mt-2 text-sm text-red-600">
                          {{ errors.contraseña[0] }}
                        </p>
                      </div>
                    </div>
                  </div>
                </form>
              </div>
            </div>
            <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button
                @click="submitForm"
                type="button"
                class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-purple-600 text-base font-medium text-white hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 sm:ml-3 sm:w-auto sm:text-sm"
              >
                {{ modalMode === 'add' ? 'Añadir' : 'Guardar cambios' }}
              </button>
              <button
                @click="closeModal"
                type="button"
                class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
              >
                Cancelar
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Modal Confirmar Eliminación Estudiante -->
    <div
      v-if="showDeleteModal"
      class="fixed z-10 inset-0 overflow-y-auto"
      aria-labelledby="modal-title"
      role="dialog"
      aria-modal="true"
    >
      <div
        class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
      >
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
          aria-hidden="true"
        ></div>

        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true"
          >&#8203;</span
        >

        <div
          class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
        >
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div
                class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10"
              >
                <svg
                  class="h-6 w-6 text-red-600"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  aria-hidden="true"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
              </div>
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                  Eliminar Estudiante
                </h3>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    ¿Estás seguro de que quieres eliminar a
                    <strong>{{ studentToDelete?.nombre }}</strong>
                    {{ studentToDelete?.apellido_p }} {{ studentToDelete?.apellido_m }}? Esta acción
                    no se puede deshacer.
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              @click="confirmDelete"
              type="button"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Eliminar
            </button>
            <button
              @click="cancelDelete"
              type="button"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Cancelar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Confirmar Eliminación Tutor -->
    <div
      v-if="showDeleteTutorModal"
      class="fixed z-10 inset-0 overflow-y-auto"
      aria-labelledby="modal-title"
      role="dialog"
      aria-modal="true"
    >
      <div
        class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
      >
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
          aria-hidden="true"
        ></div>

        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true"
          >&#8203;</span
        >

        <div
          class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
        >
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div
                class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10"
              >
                <svg
                  class="h-6 w-6 text-red-600"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  aria-hidden="true"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
              </div>
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                  Eliminar Tutor
                </h3>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    ¿Estás seguro de que quieres eliminar a
                    <strong>{{ tutorToDelete?.nombre }}</strong>
                    {{ tutorToDelete?.apellido_p }} {{ tutorToDelete?.apellido_m }}? Esta acción no
                    se puede deshacer.
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              @click="confirmDeleteTutor"
              type="button"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Eliminar
            </button>
            <button
              @click="cancelDeleteTutor"
              type="button"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Cancelar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Cargar Excel -->
    <CargarAlumnosModal
      :show="showModalExcel"
      @close="showModalExcel = false"
      @upload-success="handleUploadSuccess"
    />
  </div>
</template>

<script setup>
// ==================== IMPORTS ====================
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import DeleteIcon from '@/components/icons/DeleteIcon.vue'
import EditIcon from '@/components/icons/EditIcon.vue'
import ShowEye from '@/components/icons/ShowEye.vue'
import HideEye from '@/components/icons/HideEye.vue'
import BaseSearchInput from '@/components/ui/BaseSearchInput.vue'
import GestionAvisos from '@/components/admin/GestionAvisos.vue'
import AlumnoService from '@/services/AlumnoService.js'
import TutorService from '@/services/TutorService.js'
import CargarAlumnosModal from '@/components/student/CargarAlumnosModal.vue'
import AssignmentUploader from '@/components/tutor/AssignmentUploader.vue'

// ==================== ROUTER ====================
const router = useRouter()

// ==================== STATE - UI CONTROL ====================
const activeTab = ref('students')
const showModal = ref(false)
const showModalExcel = ref(false)
const modalType = ref('')
const modalMode = ref('')
const showPassword = ref(false)
const showDeleteModal = ref(false)
const studentToDelete = ref(null)
const showDeleteTutorModal = ref(false)
const tutorToDelete = ref(null)
// const showTutoringModal = ref(false)
// const selectedStudent = ref(null)
const showAssignmentModal = ref(false)

// ==================== STATE - CONTROL DE ETAPAS ====================
const reporteIntegralEtapa = ref(0)
const isLoadingEtapa = ref(false)
const errorEtapa = ref(null)
const successEtapa = ref(null)

// ==================== STATE - DATA ====================
const students = ref([])
const tutors = ref([])
const studentTutorings = ref([])
const loading = ref(true)
const error = ref(null)
const loadingTutor = ref(true)
const errorTutor = ref(null)
const errors = ref({})

// ==================== STATE - FORMS ====================
const formData = reactive({})
const tutoringForm = reactive({
  tutoring_id: null,
  tutorSearch: '',
  tutor_id: null,
  periodo: '',
  observaciones: '',
  dia: 'Lunes',
  hora: '',
  estado: 'en curso',
})

// ==================== STATE - PAGINATION & SEARCH (ESTUDIANTES) ====================
const currentPage = ref(1)
const itemsPerPage = ref(5)
const searchQuery = ref('')
const hayMasAlumnos = ref(true)
const totalStudents = ref(0)
const uploadMessage = ref('')
const totalPages = ref(1)
let debounceTimer = null

// ==================== STATE - PAGINATION & SEARCH (TUTORES) ====================
const currentPageTutor = ref(1)
const itemsPerPageTutor = ref(5)
const searchQueryTutor = ref('')
const hayMasTutores = ref(true)
const totalTutors = ref(0)
const totalPagesTutor = ref(1)
let debounceTimerTutor = null

// ==================== STATIC DATA ====================
const generatePeriodOptions = (yearsAhead = 3) => {
  const currentYear = new Date().getFullYear()
  const options = []
  for (let i = 0; i < yearsAhead; i++) {
    const year = currentYear + i
    options.push(`Enero-Junio ${year}`)
    options.push(`Agosto-Diciembre ${year}`)
  }
  return options
}

// eslint-disable-next-line
const periodOptions = ref(generatePeriodOptions())

const circles = [
  { color: 'bg-purple-300', size: 96, top: 10, left: 5 },
  { color: 'bg-rose-200', size: 64, top: 20, left: 80 },
  { color: 'bg-purple-400', size: 128, top: 70, left: 20 },
  { color: 'bg-gray-100', size: 80, top: 40, left: 95 },
  { color: 'bg-rose-300', size: 112, top: 85, left: 70 },
  { color: 'bg-gray-200', size: 48, top: 55, left: 10 },
  { color: 'bg-purple-500', size: 72, top: 60, left: 50 },
  { color: 'bg-rose-100', size: 56, top: 5, left: 90 },
  { color: 'bg-gray-300', size: 88, top: 80, left: 40 },
  { color: 'bg-rose-200', size: 40, top: 90, left: 10 },
  { color: 'bg-purple-400', size: 104, top: 15, left: 60 },
  { color: 'bg-gray-100', size: 68, top: 50, left: 85 },
]

// ==================== API CALLS - ESTUDIANTES ====================
const fetchStudents = async (page) => {
  try {
    const response = await AlumnoService.getAlumnos(page, itemsPerPage.value, searchQuery.value)
    students.value = response.data.alumnos
    hayMasAlumnos.value = response.data.alumnos.length === 5
    totalStudents.value = response.data.total_alumnos
    totalPages.value = Math.ceil(response.data.total_alumnos / itemsPerPage.value)
    error.value = ''
  } catch (err) {
    console.error('Error al obtener los estudiantes:', err.response.data.detail[0].type)
    if (err.response.data.detail[0].type == 'string_too_short') {
      error.value = 'Favor de ingresar mínimo 3 carácteres a buscar'
    } else {
      error.value = 'No se pudo cargar la lista de estudiantes'
    }
    students.value = []
  } finally {
    loading.value = false
  }
}

// const fetchStudentTutorings = async (studentId) => {
//   try {
//     const response = await axios.get(`http://localhost:8000/api/tutorias/alumno/${studentId}`)
//     studentTutorings.value = response.data
//     if (studentTutorings.value.length > 0) {
//       tutoringForm.tutoring_id = studentTutorings.value[0].id_tutoria
//       await loadTutoringData(studentTutorings.value[0])
//     }
//   } catch (error) {
//     console.error('Error al obtener las tutorías del alumno:', error)
//   }
// }

const handleUploadSuccess = () => {
  console.log('¡Éxito! Archivo cargado y datos procesados.')
  currentPage.value = 1
  fetchStudents()
}

// ==================== API CALLS - TUTORES ====================
const fetchTutors = async (page) => {
  try {
    const response = await TutorService.getTutores(
      page,
      itemsPerPageTutor.value,
      searchQueryTutor.value,
    )
    tutors.value = response.data.tutores
    hayMasTutores.value = response.data.tutores.length === 5
    totalTutors.value = response.data.total_tutores
    totalPagesTutor.value = Math.ceil(response.data.total_tutores / itemsPerPageTutor.value)
    errorTutor.value = ''
  } catch (err) {
    console.error('Error al obtener los tutores:', err.response.data.detail[0].type)
    if (err.response.data.detail[0].type == 'string_too_short') {
      errorTutor.value = 'Favor de ingresar mínimo 3 carácteres a buscar'
    } else {
      errorTutor.value = 'No se pudo cargar la lista de estudiantes'
    }
    tutors.value = []
  } finally {
    loadingTutor.value = false
  }
}

// ==================== API CALLS - CONFIGURACIÓN ====================
const fetchConfiguracion = async () => {
  try {
    isLoadingEtapa.value = true
    const token = localStorage.getItem('accessToken')

    const response = await axios.get('http://localhost:8000/api/configuracion/', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (response.status === 200) {
      reporteIntegralEtapa.value = response.data.reporte_integral_etapa
      console.log('✅ Etapa actual:', reporteIntegralEtapa.value)
    }
  } catch (error) {
    console.error('❌ Error al obtener configuración:', error)
    errorEtapa.value = 'No se pudo cargar la configuración de etapas.'
  } finally {
    isLoadingEtapa.value = false
  }
}

const cambiarEtapa = async (nuevaEtapa) => {
  if (reporteIntegralEtapa.value === nuevaEtapa) {
    return // Ya está en esa etapa
  }

  const mensajes = {
    1: 'Etapa 1: Los tutores podrán llenar solo el Seguimiento 1',
    2: 'Etapa 2: Los tutores podrán llenar los Seguimientos 1 y 2',
    3: 'Etapa 3: Los tutores podrán llenar todos los campos del reporte integral',
  }

  if (!confirm(`¿Cambiar a ${mensajes[nuevaEtapa]}?`)) {
    return
  }

  try {
    isLoadingEtapa.value = true
    errorEtapa.value = null
    successEtapa.value = null

    const token = localStorage.getItem('accessToken')

    const response = await axios.put(
      'http://localhost:8000/api/configuracion/',
      {
        reporte_integral_etapa: nuevaEtapa,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )

    if (response.status === 200) {
      reporteIntegralEtapa.value = nuevaEtapa
      successEtapa.value = `✅ Etapa cambiada exitosamente a Etapa ${nuevaEtapa}`

      setTimeout(() => {
        successEtapa.value = null
      }, 3000)

      console.log('✅ Etapa actualizada a:', nuevaEtapa)
    }
  } catch (error) {
    console.error('❌ Error al cambiar etapa:', error)
    errorEtapa.value = 'No se pudo cambiar la etapa. Intenta de nuevo.'

    setTimeout(() => {
      errorEtapa.value = null
    }, 3000)
  } finally {
    isLoadingEtapa.value = false
  }
}

// ==================== CRUD OPERATIONS ====================
const submitForm = async () => {
  try {
    const token = localStorage.getItem('accessToken')

    if (!token) {
      console.log('No hay token, redirigiendo al login...')
      router.push('/login_tutor')
      return
    }

    errors.value = {}
    let response

    if (modalMode.value === 'add') {
      if (modalType.value === 'student') {
        response = await axios.post('http://localhost:8000/api/alumnos', formData, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        if (response.status === 201) {
          students.value.push(response.data)
          console.log('Alumno agregado exitosamente:', response.data)
          fetchStudents()
          closeModal()
        }
      } else if (modalType.value === 'tutor') {
        response = await axios.post('http://localhost:8000/api/tutores', formData, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        if (response.status === 201) {
          tutors.value.push(response.data)
          console.log('Tutor agregado exitosamente:', response.data)
          fetchTutors()
          closeModal()
        }
      }
    } else if (modalMode.value === 'edit') {
      if (modalType.value === 'student') {
        response = await axios.put(
          `http://localhost:8000/api/alumnos/${formData.id_alumno}`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        )
        if (response.status === 200) {
          const index = students.value.findIndex(
            (student) => student.id_alumno === response.data.id_alumno,
          )
          if (index !== -1) {
            students.value[index] = response.data
          }
          console.log('Alumno actualizado exitosamente:', response.data)
          closeModal()
        }
      } else if (modalType.value === 'tutor') {
        response = await axios.put(
          `http://localhost:8000/api/tutores/${formData.id_tutor}`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        )
        if (response.status === 200) {
          const index = tutors.value.findIndex((tutor) => tutor.id_tutor === response.data.id_tutor)
          if (index !== -1) {
            tutors.value[index] = response.data
          }
          console.log('Tutor actualizado exitosamente:', response.data)
          closeModal()
        }
      }
    }
  } catch (error) {
    console.error('Error al enviar el formulario:', error)
    if (error.response && error.response.data && error.response.data.errors) {
      errors.value = error.response.data.errors
    } else {
      errors.value = { general: ['Ocurrió un error al procesar la solicitud.'] }
    }
  }
}

// const submitTutoring = async () => {
//   if (!tutoringForm.tutoring_id) {
//     console.error('No se ha seleccionado una tutoría para actualizar')
//     return
//   }

//   const selectedTutoring = studentTutorings.value.find(
//     (t) => t.id_tutoria === tutoringForm.tutoring_id,
//   )
//   if (!selectedTutoring) {
//     console.error('No se pudo encontrar la tutoría seleccionada')
//     return
//   }

//   try {
//     const response = await axios.put(
//       `http://localhost:8000/api/tutorias/${tutoringForm.tutoring_id}`,
//       {
//         tutor_id: tutoringForm.tutor_id,
//         es_activa: tutoringForm.estado === 'en curso',
//         periodo: tutoringForm.periodo,
//         observaciones: tutoringForm.observaciones,
//         semestre: selectedTutoring.semestre,
//         dia: tutoringForm.dia,
//         hora: tutoringForm.hora,
//         estado: tutoringForm.estado,
//       },
//     )
//     if (response.status === 200) {
//       console.log('Tutoría actualizada exitosamente:', response.data)
//       await fetchStudentTutorings(selectedStudent.value.id_alumno)
//       closeTutoringModal()
//     } else {
//       console.error('Error al actualizar tutoría:', response.data)
//     }
//   } catch (error) {
//     console.error('Error al enviar la solicitud de actualización de tutoría:', error)
//   }
// }

// ==================== DELETE OPERATIONS ====================
const confirmDelete = async () => {
  if (studentToDelete.value) {
    try {
      const response = await axios.delete(
        `http://localhost:8000/api/alumnos/${studentToDelete.value.id_alumno}`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
          },
        },
      )
      if (response.status === 204) {
        students.value = students.value.filter(
          (s) => s.id_alumno !== studentToDelete.value.id_alumno,
        )
        console.log('Estudiante eliminado exitosamente')
        fetchStudents()
      } else {
        console.error('Error al eliminar el estudiante:', response.data)
      }
    } catch (error) {
      console.error('Error al eliminar el estudiante:', error)
    } finally {
      showDeleteModal.value = false
      studentToDelete.value = null
    }
  }
}

const confirmDeleteTutor = async () => {
  const token = localStorage.getItem('accessToken')
  if (tutorToDelete.value) {
    try {
      const response = await axios.delete(
        `http://localhost:8000/api/tutores/${tutorToDelete.value.id_tutor}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      )
      if (response.status === 204) {
        tutors.value = tutors.value.filter((t) => t.id_tutor !== tutorToDelete.value.id_tutor)
        console.log('Tutor eliminado exitosamente')
      } else {
        console.error('Error al eliminar el tutor:', response.data)
      }
    } catch (error) {
      console.error('Error al eliminar el tutor:', error)
    } finally {
      showDeleteTutorModal.value = false
      tutorToDelete.value = null
    }
  }
}

// ==================== MODAL HANDLERS ====================
const openModal = (type, mode = 'add', item = null) => {
  modalType.value = type
  modalMode.value = mode
  showModal.value = true
  clearErrors()

  Object.keys(formData).forEach((key) => delete formData[key])

  if (mode === 'edit' && item) {
    // eslint-disable-next-line
    const { contraseña, ...rest } = item
    Object.assign(formData, rest)
    formData.contraseña = ''
  } else {
    if (type === 'student') {
      Object.assign(formData, {
        nombre: '',
        apellido_p: '',
        apellido_m: '',
        num_control: '',
        contraseña: '',
        carrera: '',
        semestre_actual: '',
        estado: 'activo',
        correo: '',
        telefono: '',
      })
    } else if (type === 'tutor') {
      Object.assign(formData, {
        nombre: '',
        apellido_p: '',
        apellido_m: '',
        especialidad: '',
        correo: '',
        contraseña: '',
        telefono: '',
      })
    }
  }
}

const openAssignmentModal = () => {
  showAssignmentModal.value = true
}

const closeAssignmentModal = () => {
  showAssignmentModal.value = false
}

const handleAssignmentSuccess = () => {
  console.log('Asignaciones procesadas exitosamente')
}

const closeModal = () => {
  showModal.value = false
  showPassword.value = false
  clearErrors()
}

// const closeTutoringModal = () => {
//   showTutoringModal.value = false
//   selectedStudent.value = null
//   studentTutorings.value = []
//   Object.keys(tutoringForm).forEach((key) => {
//     if (key === 'estado') {
//       tutoringForm[key] = 'en curso'
//     } else {
//       tutoringForm[key] = ''
//     }
//   })
// }

// ==================== UTILITY FUNCTIONS ====================
const clearErrors = () => {
  errors.value = {}
}

const loadTutoringData = async (tutoring) => {
  tutoringForm.tutoring_id = tutoring.id_tutoria
  tutoringForm.tutor_id = tutoring.tutor_id
  tutoringForm.periodo = tutoring.periodo
  tutoringForm.observaciones = tutoring.observaciones
  tutoringForm.dia = tutoring.dia
  tutoringForm.hora = tutoring.hora
  tutoringForm.estado = tutoring.estado || 'en curso'

  const tutor = tutors.value.find((t) => t.id_tutor === tutoring.tutor_id)
  if (tutor) {
    tutoringForm.tutorSearch = `${tutor.nombre} ${tutor.apellido_p} (${tutor.correo})`
  } else {
    tutoringForm.tutorSearch = ``
  }
}

// const selectTutor = (tutor) => {
//   tutoringForm.tutor_id = tutor.id_tutor
//   tutoringForm.tutorSearch = `${tutor.nombre} ${tutor.apellido_p} (${tutor.correo})`
// }

// ==================== EVENT HANDLERS ====================
const handleLogout = () => {
  console.log(localStorage.getItem('accessToken'))
  localStorage.removeItem('accessToken')
  localStorage.removeItem('administrador')
  router.push('/login_admin')
}

const editItem = (item, type) => {
  openModal(type, 'edit', item)
}

const deleteItem = (student) => {
  studentToDelete.value = student
  showDeleteModal.value = true
}

const cancelDelete = () => {
  showDeleteModal.value = false
  studentToDelete.value = null
}

const deleteTutor = (tutor) => {
  tutorToDelete.value = tutor
  showDeleteTutorModal.value = true
}

const cancelDeleteTutor = () => {
  showDeleteTutorModal.value = false
  tutorToDelete.value = null
}

// ==================== PAGINATION - ESTUDIANTES ====================
const nextPage = () => {
  currentPage.value++
  fetchStudents(currentPage.value)
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    fetchStudents(currentPage.value)
  }
}

// ==================== PAGINATION - TUTORES ====================
const nextPageTutor = () => {
  currentPageTutor.value++
  fetchTutors(currentPageTutor.value)
}

const prevPageTutor = () => {
  if (currentPageTutor.value > 1) {
    currentPageTutor.value--
    fetchTutors(currentPageTutor.value)
  }
}

// ==================== WATCHERS ====================
// eslint-disable-next-line
watch(searchQuery, (newQuery, oldQuery) => {
  clearTimeout(debounceTimer)

  debounceTimer = setTimeout(() => {
    currentPage.value = 1
    fetchStudents()
  }, 500)
})

// eslint-disable-next-line
watch(searchQueryTutor, (newQuery, oldQuery) => {
  clearTimeout(debounceTimerTutor)

  debounceTimerTutor = setTimeout(() => {
    currentPageTutor.value = 1
    fetchTutors()
  }, 500)
})

watch(
  () => tutoringForm.tutoring_id,
  (newTutoringId) => {
    const selectedTutoring = studentTutorings.value.find((t) => t.id_tutoria === newTutoringId)
    if (selectedTutoring) {
      loadTutoringData(selectedTutoring)
    }
  },
)

// ==================== LIFECYCLE HOOKS ====================
onMounted(async () => {
  await fetchConfiguracion() // Cargar configuración de etapas primero
  await fetchStudents(currentPage.value)
  await fetchTutors(currentPageTutor.value)
})
</script>

<style>
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

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

<style>
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

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
