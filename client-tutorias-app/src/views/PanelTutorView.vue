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
            <div class="flex items-center">
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
        <!-- Encabezado y búsqueda -->
        <div
          class="px-4 py-6 sm:px-0 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-x-6"
        >
          <div class="flex items-center justify-between w-full mb-4 sm:mb-0">
            <h1 class="text-3xl font-bold text-gray-900">Dashboard del Tutor</h1>
          </div>
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
            <!-- <input
              v-model="searchQuery"
              type="text"
              placeholder="Buscar estudiante..."
              :disabled="loading"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-coral-500 focus:border-coral-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
            /> -->
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

        <!-- Modal para Reporte Integral -->
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
              class="relative top-20 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white"
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
                <PrimerReporteTutoria @cerrar="mostrarModalPrimerReporte = false" />
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
                            student.status === 'en curso'
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
                        <button
                          @click="openReporteIntegralModal(student)"
                          class="px-4 py-2 bg-coral-600 text-white rounded-md hover:bg-coral-700 transition duration-150 ease-in-out"
                        >
                          Reporte Integral
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import TutorService from '@/services/TutorService.js' // Ajusta la ruta según tu estructura
import ReporteIntegralTutoria from '@/components/ReporteIntegralTutoria.vue'
import PrimerReporteTutoria from '@/components/PrimerReporteTutoria.vue'
import SegundoReporteTutoria from '@/components/SegundoReporteTutoria.vue'
import BaseSearchInput from '@/components/ui/BaseSearchInput.vue'

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

// const filteredStudents = computed(() => {
//   return students.value
// })

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

  // loading.value = true
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

// eslint-disable-next-line
watch(searchQuery, (newQuery, oldQuery) => {
  // Limpiamos el temporizador anterior para evitar búsquedas innecesarias
  clearTimeout(debounceTimer)

  // Creamos un nuevo temporizador. La búsqueda no se ejecutará hasta
  // que el usuario deje de escribir por 500ms.
  debounceTimer = setTimeout(() => {
    currentPage.value = 1 // Cada nueva búsqueda debe reiniciar la paginación a la página 1
    fetchAssignedStudents()
  }, 500) // 500ms de espera
})

// ==================== MODAL HANDLERS ====================
const openReporteIntegralModal = (student) => {
  selectedStudent.value = student
  showReporteIntegralModal.value = true
}

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

// ==================== WATCHERS ====================
// Observa cambios en la búsqueda para recargar datos
watch(searchQuery, async (newValue) => {
  if (newValue.length === 0 || newValue.length >= 3) {
    currentPage.value = 1
    await fetchAssignedStudents(1)
  }
})

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
