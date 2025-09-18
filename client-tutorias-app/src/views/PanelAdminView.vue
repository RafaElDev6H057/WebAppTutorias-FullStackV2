<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-white relative overflow-hidden">
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
    <!-- Barra de navegación -->
    <nav class="bg-indigo-600 shadow-lg relative z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <img
              class="h-10 w-10 rounded-full border-2 border-white"
              src="/login_admin.jpg"
              alt="Foto del administrador"
            />
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

    <!-- Contenido principal -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8 relative z-10">
      <div class="px-4 py-6 sm:px-0">
        <h1 class="text-3xl font-bold text-gray-900 mb-8">Panel de Administración</h1>

        <!-- Pestañas para cambiar entre estudiantes y tutores -->
        <div class="mb-8">
          <nav class="flex space-x-4" aria-label="Tabs">
            <button
              @click="activeTab = 'students'"
              :class="[
                activeTab === 'students'
                  ? 'bg-indigo-100 text-indigo-700'
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
                  ? 'bg-indigo-100 text-indigo-700'
                  : 'text-gray-500 hover:text-gray-700',
                'px-3 py-2 font-medium text-sm rounded-md',
              ]"
            >
              Tutores
            </button>
          </nav>
        </div>

        <!-- Panel de Estudiantes -->
        <div v-if="activeTab === 'students'">
          <!-- <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold text-gray-900">Gestión de Estudiantes</h2>
            <button
              @click="openModal('student')"
              class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium transition duration-150 ease-in-out"
            >
              Añadir Estudiante
            </button>
          </div> -->

          <!-- Add search input before the table -->
          <div class="mb-4 flex justify-between items-center">
            <h2 class="text-2xl font-bold text-gray-900">Gestión de Estudiantes</h2>
            <div class="flex items-center gap-4">
              <div class="relative">
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Buscar estudiante..."
                  class="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 block w-64"
                />
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg
                    class="h-5 w-5 text-gray-400"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </div>
              </div>
              <button
                @click="openModal('student')"
                class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium transition duration-150 ease-in-out"
              >
                Añadir Estudiante
              </button>
            </div>
          </div>

          <!-- Estado de carga -->
          <div v-if="loading" class="text-center text-gray-500">Cargando estudiantes...</div>

          <!-- Mensaje de error -->
          <div v-if="error" class="text-red-500 text-center">{{ error }}</div>

          <div class="bg-white shadow overflow-hidden sm:rounded-lg">
            <!-- Tabla de estudiantes -->
            <table
              table
              v-if="!loading && paginatedStudents.length > 0"
              class="min-w-full divide-y divide-gray-200"
            >
              <thead class="bg-gray-50">
                <tr>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Nombre Completo
                  </th>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Número de Control
                  </th>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Semestre
                  </th>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Carrera
                  </th>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Estado
                  </th>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="student in paginatedStudents" :key="student.id">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <!-- <div class="flex-shrink-0 h-10 w-10">
                        <img
                          class="h-10 w-10 rounded-full"
                          :src="student.avatar || '/placeholder.svg'"
                          alt=""
                        />
                      </div> -->
                      <div class="ml-4">
                        <div class="text-sm font-medium text-gray-900">
                          {{ `${student.nombre} ${student.apellido_p} ${student.apellido_m}` }}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">{{ student.num_control }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">{{ student.semestre_actual }}° Semestre</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">{{ student.carrera }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                      :class="
                        student.estado === 'activo'
                          ? 'bg-green-100 text-green-800'
                          : 'bg-red-100 text-red-800'
                      "
                    >
                      {{ student.estado }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium flex">
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
                    <button
                      @click="openTutoringModal(student)"
                      class="text-white hover:bg-orange-500 bg-orange-400 px-2 py-1 rounded-2xl transition-colors duration-200"
                    >
                      Administrar Tutorías
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-if="!loading && students.length === 0" class="text-center text-gray-500">
              No hay estudiantes registrados.
            </div>
          </div>
          <!-- Add pagination controls after the table -->
          <div
            class="bg-white mt-2 rounded-xl px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6"
          >
            <div class="flex-1 flex justify-between sm:hidden">
              <button
                @click="prevPage"
                :disabled="currentPage === 1"
                class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                Anterior
              </button>
              <button
                @click="nextPage"
                :disabled="currentPage === totalPages"
                class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
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
                    Math.min(currentPage * itemsPerPage, filteredStudents.length)
                  }}</span>
                  de
                  <span class="font-medium">{{ filteredStudents.length }}</span>
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
                    class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                  >
                    <span class="sr-only">Anterior</span>
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
                  </button>

                  <template v-for="page in totalPages" :key="page">
                    <button
                      @click="goToPage(page)"
                      :class="[
                        currentPage === page
                          ? 'z-10 bg-indigo-50 border-indigo-500 text-indigo-600'
                          : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50',
                        'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                      ]"
                    >
                      {{ page }}
                    </button>
                  </template>

                  <button
                    @click="nextPage"
                    :disabled="currentPage === totalPages"
                    class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                  >
                    <span class="sr-only">Siguiente</span>
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

        <!-- Panel de Tutores -->
        <div v-if="activeTab === 'tutors'">
          <!-- Add search input before the table -->
          <div class="mb-4 flex justify-between items-center">
            <h2 class="text-2xl font-bold text-gray-900">Gestión de Tutores</h2>
            <div class="flex items-center gap-4">
              <div class="relative">
                <input
                  v-model="tutorSearchQuery"
                  type="text"
                  placeholder="Buscar tutor..."
                  class="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 block w-64"
                />
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg
                    class="h-5 w-5 text-gray-400"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </div>
              </div>
              <button
                @click="openModal('tutor')"
                class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium transition duration-150 ease-in-out"
              >
                Añadir Tutor
              </button>
            </div>
          </div>
          <div class="bg-white shadow overflow-hidden sm:rounded-lg">
            <table v-if="paginatedTutors.length > 0" class="min-w-full divide-y divide-gray-200">
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
                <tr v-for="tutor in paginatedTutors" :key="tutor.id">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <!-- <div class="flex-shrink-0 h-10 w-10">
                        <img class="h-10 w-10 rounded-full" :src="tutor.avatar" alt="" />
                      </div> -->
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
                    <div class="text-sm text-gray-900">{{ tutor.telefono }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">{{ tutor.especialidad }}</div>
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
            <div v-if="tutors.length === 0" class="text-center text-gray-500">
              No hay tutores registrados.
            </div>
          </div>
          <!-- Add pagination controls after the table -->
          <div
            class="bg-white mt-2 rounded-xl px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6"
          >
            <div class="flex-1 flex justify-between sm:hidden">
              <button
                @click="prevTutorPage"
                :disabled="tutorCurrentPage === 1"
                class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                Anterior
              </button>
              <button
                @click="nextTutorPage"
                :disabled="tutorCurrentPage === totalTutorPages"
                class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                Siguiente
              </button>
            </div>
            <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p class="text-sm text-gray-700">
                  Mostrando
                  <span class="font-medium">{{
                    (tutorCurrentPage - 1) * tutorItemsPerPage + 1
                  }}</span>
                  a
                  <span class="font-medium">{{
                    Math.min(tutorCurrentPage * tutorItemsPerPage, filteredTutors.length)
                  }}</span>
                  de
                  <span class="font-medium">{{ filteredTutors.length }}</span>
                  resultados
                </p>
              </div>
              <div>
                <nav
                  class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
                  aria-label="Pagination"
                >
                  <button
                    @click="prevTutorPage"
                    :disabled="tutorCurrentPage === 1"
                    class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                  >
                    <span class="sr-only">Anterior</span>
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
                  </button>

                  <template v-for="page in totalTutorPages" :key="page">
                    <button
                      @click="goToTutorPage(page)"
                      :class="[
                        tutorCurrentPage === page
                          ? 'z-10 bg-indigo-50 border-indigo-500 text-indigo-600'
                          : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50',
                        'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                      ]"
                    >
                      {{ page }}
                    </button>
                  </template>

                  <button
                    @click="nextTutorPage"
                    :disabled="tutorCurrentPage === totalTutorPages"
                    class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                  >
                    <span class="sr-only">Siguiente</span>
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
            <div class="bg-gradient-to-r from-indigo-500 to-purple-600 px-4 py-3 sm:px-6">
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
                        <option value="Ing. en Semiconductores">Ing. en Semiconductores</option>
                        <option value="Ing. en Logistica">Ing. en Logistica</option>
                        <option value="Ing. en Informatica">Ing. en Informatica</option>
                        <option value="Ing. en Electronica">Ing. en Electronica</option>
                        <option value="Ing. en Sistemas Computacionales">
                          Ing. en Sistemas Computacionales
                        </option>
                        <option value="Ing. Ambiental">Ing. Ambiental</option>
                        <option value="Ing. Industrial">Ing. Industrial</option>
                        <option value="Ing. en Gestion Empresarial">
                          Ing. en Gestion Empresarial
                        </option>
                        <option value="Ing. en Mineria">Ing. en Mineria</option>
                        <option value="Lic. en Arquitectura">Lic. en Arquitectura</option>
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
                          <option value="activo">Activo</option>
                          <option value="inactivo">Inactivo</option>
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
                      <div>
                        <label for="especialidad" class="block text-sm font-medium text-gray-700"
                          >Departamento</label
                        >
                        <input
                          type="text"
                          name="especialidad"
                          id="especialidad"
                          v-model="formData.especialidad"
                          :class="[
                            'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                            { 'border-red-500': errors.especialidad },
                          ]"
                        />
                        <p v-if="errors.especialidad" class="mt-2 text-sm text-red-600">
                          {{ errors.especialidad[0] }}
                        </p>
                      </div>

                      <div>
                        <label for="telefono" class="block text-sm font-medium text-gray-700"
                          >Teléfono</label
                        >
                        <input
                          type="tel"
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
                </form>
              </div>
            </div>
            <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button
                @click="submitForm"
                type="button"
                class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:ml-3 sm:w-auto sm:text-sm"
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

    <!-- Delete Confirmation Modal -->
    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
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
                    Eliminar estudiante
                  </h3>
                  <div class="mt-2">
                    <p class="text-sm text-gray-500">
                      ¿Estás seguro de que deseas eliminar a este estudiante? Esta acción no se
                      puede deshacer.
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
    </Transition>

    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
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
                    Eliminar tutor
                  </h3>
                  <div class="mt-2">
                    <p class="text-sm text-gray-500">
                      ¿Estás seguro de que deseas eliminar a este tutor? Esta acción no se puede
                      deshacer.
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
    </Transition>
  </div>

  <!-- Modal de Asignación de Tutoría -->
  <Transition
    enter-active-class="transition ease-out duration-300"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition ease-in duration-200"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div
      v-if="showTutoringModal"
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
            <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
              Asignar Tutoría para {{ selectedStudent?.nombre }} {{ selectedStudent?.apellido_p }}
            </h3>
            <div class="mt-2">
              <form @submit.prevent="submitTutoring">
                <!-- Campo para seleccionar la tutoría a actualizar -->
                <div class="mb-4">
                  <label for="tutoring_id" class="block text-sm font-medium text-gray-700"
                    >Tutoría a actualizar</label
                  >
                  <select
                    id="tutoring_id"
                    v-model="tutoringForm.tutoring_id"
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    required
                  >
                    <option
                      v-for="tutoring in studentTutorings"
                      :key="tutoring.id_tutoria"
                      :value="tutoring.id_tutoria"
                    >
                      Tutoría {{ tutoring.semestre }}° semestre
                    </option>
                  </select>
                </div>

                <div class="mb-4">
                  <label for="tutor" class="block text-sm font-medium text-gray-700">Tutor</label>
                  <input
                    autocomplete="off"
                    type="text"
                    id="tutor"
                    v-model="tutoringForm.tutorSearch"
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    placeholder="Buscar por nombre o correo"
                  />
                  <div
                    v-if="searchTutors.length > 0"
                    class="mt-1 absolute z-10 w-full bg-white shadow-lg max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto sm:text-sm"
                  >
                    <div
                      v-for="tutor in searchTutors"
                      :key="tutor.id_tutor"
                      @click="selectTutor(tutor)"
                      class="cursor-pointer select-none relative py-2 pl-3 pr-9 hover:bg-indigo-600 hover:text-white"
                    >
                      {{ tutor.nombre }} {{ tutor.apellido_p }} ({{ tutor.correo }})
                    </div>
                  </div>
                </div>

                <div class="mb-4">
                  <label for="periodo" class="block text-sm font-medium text-gray-700"
                    >Periodo</label
                  >
                  <select
                    id="periodo"
                    v-model="tutoringForm.periodo"
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  >
                    <option v-for="option in periodOptions" :key="option" :value="option">
                      {{ option }}
                    </option>
                  </select>
                </div>
                <div class="mb-4">
                  <label for="observaciones" class="block text-sm font-medium text-gray-700"
                    >Observaciones (opcional)</label
                  >
                  <textarea
                    id="observaciones"
                    v-model="tutoringForm.observaciones"
                    rows="3"
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  ></textarea>
                </div>
                <div class="mb-4">
                  <label for="dia" class="block text-sm font-medium text-gray-700">Día</label>
                  <select
                    id="dia"
                    v-model="tutoringForm.dia"
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  >
                    <option value="lunes">Lunes</option>
                    <option value="martes">Martes</option>
                    <option value="miércoles">Miércoles</option>
                    <option value="jueves">Jueves</option>
                    <option value="viernes">Viernes</option>
                  </select>
                </div>
                <div class="mb-4">
                  <label for="hora" class="block text-sm font-medium text-gray-700">Hora</label>
                  <input
                    type="time"
                    id="hora"
                    v-model="tutoringForm.hora"
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>
                <!-- Campo para el estado -->
                <div class="mb-4">
                  <label for="estado" class="block text-sm font-medium text-gray-700">Estado</label>
                  <select
                    id="estado"
                    v-model="tutoringForm.estado"
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  >
                    <option value="pendiente">Pendiente</option>
                    <option value="en curso">En curso</option>
                    <option value="completada">Completada</option>
                  </select>
                </div>
              </form>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="button"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:ml-3 sm:w-auto sm:text-sm"
              @click="submitTutoring"
            >
              Actualizar Tutoría
            </button>
            <button
              type="button"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
              @click="closeTutoringModal"
            >
              Cancelar
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import DeleteIcon from '@/components/icons/DeleteIcon.vue'
import EditIcon from '@/components/icons/EditIcon.vue'
import ShowEye from '@/components/icons/ShowEye.vue'
import HideEye from '@/components/icons/HideEye.vue'

const router = useRouter()

const showPassword = ref(false)
const activeTab = ref('students')
const showModal = ref(false)
const modalType = ref('')
const modalMode = ref('')
const formData = reactive({})

const students = ref([])
const tutors = ref([])
const loading = ref(true) // Indica si los datos están cargando
const error = ref(null) // Manejo de errores

const showDeleteModal = ref(false)
const studentToDelete = ref(null)
const showDeleteTutorModal = ref(false)
const tutorToDelete = ref(null)

const deleteItem = (student) => {
  studentToDelete.value = student
  showDeleteModal.value = true
}

const cancelDelete = () => {
  showDeleteModal.value = false
  studentToDelete.value = null
}

const confirmDelete = async () => {
  if (studentToDelete.value) {
    try {
      const response = await axios.delete(
        `http://localhost:8000/api/alumnos/${studentToDelete.value.id_alumno}`,
      )
      if (response.status === 204) {
        students.value = students.value.filter(
          (s) => s.id_alumno !== studentToDelete.value.id_alumno,
        )
        console.log('Estudiante eliminado exitosamente')
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

const deleteTutor = (tutor) => {
  tutorToDelete.value = tutor
  showDeleteTutorModal.value = true
}

const cancelDeleteTutor = () => {
  showDeleteTutorModal.value = false
  tutorToDelete.value = null
}

const confirmDeleteTutor = async () => {
  if (tutorToDelete.value) {
    try {
      const response = await axios.delete(
        `http://localhost:8000/api/tutores/${tutorToDelete.value.id_tutor}`,
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

// Método para obtener los estudiantes
const fetchStudents = async () => {
  try {
    // Realiza la solicitud GET al endpoint de estudiantes
    const response = await axios.get('http://localhost:8000/api/alumnos')
    // Asigna específicamente el array de alumnos al estado
    students.value = response.data // <-- Aquí extraemos 'alumnos'
    // console.log(students.value) // Verifica que ahora sea un array
  } catch (err) {
    console.error('Error al obtener los estudiantes:', err)
    error.value = 'No se pudo cargar la lista de estudiantes'
  } finally {
    loading.value = false // Finaliza la carga
  }
}

// const fetchTutors = async () => {
//   try {
//     // Realiza la solicitud GET al endpoint de estudiantes
//     const response = await axios.get('http://localhost:8000/api/tutores')
//     // Asigna específicamente el array de alumnos al estado
//     tutors.value = response.data.tutores // <-- Aquí extraemos 'alumnos'
//     // console.log(students.value) // Verifica que ahora sea un array
//   } catch (err) {
//     console.error('Error al obtener los tutores:', err)
//     error.value = 'No se pudo cargar la lista de tutores'
//   } finally {
//     loading.value = false // Finaliza la carga
//   }
// }

onMounted(() => {
  fetchStudents()
  fetchTutors()
})

const handleLogout = () => {
  localStorage.removeItem('administrador') // Limpia los datos del almacenamiento
  router.push('/login_admin') // Redirige al login
}

const openModal = (type, mode = 'add', item = null) => {
  modalType.value = type
  modalMode.value = mode
  showModal.value = true
  clearErrors()

  // Reset formData
  Object.keys(formData).forEach((key) => delete formData[key])

  if (mode === 'edit' && item) {
    // Clone the item to avoid directly modifying the original data
    /* eslint-disable-next-line no-unused-vars */
    const { contraseña, ...rest } = item
    Object.assign(formData, rest)
    formData.contraseña = '' // Ensure password field is empty
  } else {
    // Set default values based on the type
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

const closeModal = () => {
  showModal.value = false
  showPassword.value = false
  clearErrors()
}

const editItem = (item, type) => {
  openModal(type, 'edit', item)
}
const errors = ref({})

const submitForm = async () => {
  try {
    errors.value = {} // Limpiar errores anteriores
    let response
    if (modalMode.value === 'add') {
      if (modalType.value === 'student') {
        response = await axios.post('http://localhost:8000/api/alumnos', formData)
        if (response.status === 201) {
          const nuevoAlumno = response.data
          students.value.push(nuevoAlumno)
          console.log('Alumno agregado exitosamente:', response.data)
          closeModal()
        }
      } else if (modalType.value === 'tutor') {
        response = await axios.post('http://localhost:8000/api/tutores', formData)
        if (response.status === 201) {
          console.log(response.data)
          const nuevoTutor = response.data
          tutors.value.push(nuevoTutor)
          console.log('Tutor agregado exitosamente:', response.data)
          closeModal()
        }
      }
    } else if (modalMode.value === 'edit') {
      if (modalType.value === 'student') {
        response = await axios.put(
          `http://localhost:8000/api/alumnos/${formData.id_alumno}`,
          formData,
        )
        if (response.status === 200) {
          const updatedStudent = response.data
          const index = students.value.findIndex(
            (student) => student.id_alumno === updatedStudent.id_alumno,
          )
          if (index !== -1) {
            students.value[index] = updatedStudent
          }
          console.log('Alumno actualizado exitosamente:', response.data)
          closeModal()
        }
      } else if (modalType.value === 'tutor') {
        response = await axios.put(
          `http://localhost:8000/api/tutores/${formData.id_tutor}`,
          formData,
        )
        if (response.status === 200) {
          const updatedTutor = response.data
          const index = tutors.value.findIndex((tutor) => tutor.id_tutor === updatedTutor.id_tutor)
          if (index !== -1) {
            tutors.value[index] = updatedTutor
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

const clearErrors = () => {
  errors.value = {}
}

// Pagination and search state
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = ref(5)

// Computed property for filtered students
const filteredStudents = computed(() => {
  return students.value.filter((student) => {
    const fullName = `${student.nombre} ${student.apellido_p} ${student.apellido_m}`.toLowerCase()
    const searchTerm = searchQuery.value.toLowerCase()
    return (
      fullName.includes(searchTerm) ||
      student.num_control.toLowerCase().includes(searchTerm) ||
      student.carrera.toLowerCase().includes(searchTerm)
    )
  })
})

// Computed property for paginated students
const paginatedStudents = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredStudents.value.slice(start, end)
})

// Computed property for total pages
const totalPages = computed(() => {
  return Math.ceil(filteredStudents.value.length / itemsPerPage.value)
})

// Navigation methods
const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const goToPage = (page) => {
  currentPage.value = page
}

// Reset to first page when search query changes
// watch(searchQuery, () => {
//   currentPage.value = 1
// })

// Tutors search and pagination state
const tutorSearchQuery = ref('')
const tutorCurrentPage = ref(1)
const tutorItemsPerPage = ref(5)

// Computed property for filtered tutors
const filteredTutors = computed(() => {
  return tutors.value.filter((tutor) => {
    const searchTerm = tutorSearchQuery.value.toLowerCase()
    return (
      tutor.nombre.toLowerCase().includes(searchTerm) ||
      tutor.correo.toLowerCase().includes(searchTerm) ||
      tutor.especialidad.toLowerCase().includes(searchTerm)
    )
  })
})

// Computed property for paginated tutors
const paginatedTutors = computed(() => {
  const start = (tutorCurrentPage.value - 1) * tutorItemsPerPage.value
  const end = start + tutorItemsPerPage.value
  return filteredTutors.value.slice(start, end)
})

// Computed property for total tutor pages
const totalTutorPages = computed(() => {
  return Math.ceil(filteredTutors.value.length / tutorItemsPerPage.value)
})

// Tutor navigation methods
const nextTutorPage = () => {
  if (tutorCurrentPage.value < totalTutorPages.value) {
    tutorCurrentPage.value++
  }
}

const prevTutorPage = () => {
  if (tutorCurrentPage.value > 1) {
    tutorCurrentPage.value--
  }
}

const goToTutorPage = (page) => {
  tutorCurrentPage.value = page
}

const showTutoringModal = ref(false)
const selectedStudent = ref(null)
const studentTutorings = ref([])
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

// Modify the existing fetchTutors function to store all tutors
const fetchTutors = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/tutores')
    tutors.value = response.data
  } catch (err) {
    console.error('Error al obtener los tutores:', err)
    error.value = 'No se pudo cargar la lista de tutores'
  } finally {
    loading.value = false
  }
}

// Función modificada para abrir el modal de tutoría
const openTutoringModal = async (student) => {
  selectedStudent.value = student
  showTutoringModal.value = true
  await fetchTutors() // Asegurarse de que tenemos la lista de tutores actualizada
  await fetchStudentTutorings(student.id_alumno)
}

const fetchStudentTutorings = async (studentId) => {
  try {
    const response = await axios.get(`http://localhost:8000/api/tutorias/alumno/${studentId}`)
    studentTutorings.value = response.data
    if (studentTutorings.value.length > 0) {
      tutoringForm.tutoring_id = studentTutorings.value[0].id_tutoria
      await loadTutoringData(studentTutorings.value[0])
    }
  } catch (error) {
    console.error('Error al obtener las tutorías del alumno:', error)
  }
}

const loadTutoringData = async (tutoring) => {
  tutoringForm.tutoring_id = tutoring.id_tutoria
  tutoringForm.tutor_id = tutoring.tutor_id
  tutoringForm.periodo = tutoring.periodo
  tutoringForm.observaciones = tutoring.observaciones
  tutoringForm.dia = tutoring.dia
  tutoringForm.hora = tutoring.hora
  tutoringForm.estado = tutoring.estado || 'en curso'

  // Buscar la información del tutor
  const tutor = tutors.value.find((t) => t.id_tutor === tutoring.tutor_id)
  if (tutor) {
    tutoringForm.tutorSearch = `${tutor.nombre} ${tutor.apellido_p} (${tutor.correo})`
  } else {
    tutoringForm.tutorSearch = ``
  }
}

watch(
  () => tutoringForm.tutoring_id,
  (newTutoringId) => {
    const selectedTutoring = studentTutorings.value.find((t) => t.id_tutoria === newTutoringId)
    if (selectedTutoring) {
      loadTutoringData(selectedTutoring)
    }
  },
)

// New function to close tutoring modal
const closeTutoringModal = () => {
  showTutoringModal.value = false
  selectedStudent.value = null
  studentTutorings.value = []
  Object.keys(tutoringForm).forEach((key) => {
    if (key === 'estado') {
      tutoringForm[key] = 'en curso'
    } else {
      tutoringForm[key] = ''
    }
  })
}

// New function to search tutors
const searchTutors = computed(() => {
  if (tutoringForm.tutorSearch.length > 2) {
    const searchTerm = tutoringForm.tutorSearch.toLowerCase()
    return tutors.value.filter(
      (tutor) =>
        tutor.nombre.toLowerCase().includes(searchTerm) ||
        tutor.apellido_p.toLowerCase().includes(searchTerm) ||
        tutor.apellido_m.toLowerCase().includes(searchTerm) ||
        tutor.correo.toLowerCase().includes(searchTerm),
    )
  }
  return []
})

// New function to select a tutor
const selectTutor = (tutor) => {
  tutoringForm.tutor_id = tutor.id_tutor
  tutoringForm.tutorSearch = `${tutor.nombre} ${tutor.apellido_p} (${tutor.correo})`
}

// New function to submit tutoring assignment
const submitTutoring = async () => {
  if (!tutoringForm.tutoring_id) {
    console.error('No se ha seleccionado una tutoría para actualizar')
    return
  }

  const selectedTutoring = studentTutorings.value.find(
    (t) => t.id_tutoria === tutoringForm.tutoring_id,
  )
  if (!selectedTutoring) {
    console.error('No se pudo encontrar la tutoría seleccionada')
    return
  }

  try {
    const response = await axios.put(
      `http://localhost:8000/api/tutorias/${tutoringForm.tutoring_id}`,
      {
        tutor_id: tutoringForm.tutor_id,
        es_activa: tutoringForm.estado === 'en curso',
        periodo: tutoringForm.periodo,
        observaciones: tutoringForm.observaciones,
        semestre: selectedTutoring.semestre,
        dia: tutoringForm.dia,
        hora: tutoringForm.hora,
        estado: tutoringForm.estado,
      },
    )
    if (response.status === 200) {
      console.log('Tutoría actualizada exitosamente:', response.data)
      // Actualizar la lista de tutorías del estudiante si es necesario
      await fetchStudentTutorings(selectedStudent.value.id_alumno)
      closeTutoringModal()
    } else {
      console.error('Error al actualizar tutoría:', response.data)
    }
  } catch (error) {
    console.error('Error al enviar la solicitud de actualización de tutoría:', error)
  }
}

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

const periodOptions = ref(generatePeriodOptions())
console.log(periodOptions.value)

const circles = [
  { color: 'bg-blue-500', size: 96, top: 10, left: 5 },
  { color: 'bg-blue-600', size: 64, top: 20, left: 80 },
  { color: 'bg-blue-400', size: 128, top: 70, left: 20 },
  { color: 'bg-blue-300', size: 80, top: 40, left: 95 },
  { color: 'bg-blue-300', size: 112, top: 85, left: 70 },
  { color: 'bg-blue-400', size: 48, top: 55, left: 10 },
  { color: 'bg-blue-600', size: 72, top: 60, left: 50 },
  { color: 'bg-blue-500', size: 56, top: 5, left: 90 },
  { color: 'bg-blue-500', size: 88, top: 80, left: 40 },
  { color: 'bg-blue-300', size: 40, top: 90, left: 10 },
  { color: 'bg-blue-400', size: 104, top: 15, left: 60 },
  { color: 'bg-blue-400', size: 68, top: 50, left: 85 },
]
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
