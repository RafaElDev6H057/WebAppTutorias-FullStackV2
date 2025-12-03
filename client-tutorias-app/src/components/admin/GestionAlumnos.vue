<template>
  <!-- ==================== PANEL DE ESTUDIANTES ==================== -->
  <div class="space-y-6">
    <!-- Header con botones de acción -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div class="flex justify-between items-start mb-4">
        <div>
          <h2 class="text-2xl font-bold text-gray-900">Gestión de Estudiantes</h2>
          <p class="text-sm text-gray-600 mt-1">
            Administra los estudiantes registrados en el sistema
          </p>
        </div>
      </div>

      <!-- Barra de acciones -->
      <div class="flex items-center gap-3 flex-wrap">
        <div class="flex-1 min-w-[250px]">
          <BaseSearchInput v-model="searchQuery" placeholder="Buscar estudiante..." />
        </div>

        <button
          @click="showModalExcel = true"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 flex items-center gap-2 shadow-sm hover:shadow-md"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
          Cargar Excel
        </button>

        <button
          @click="openModal('add')"
          class="bg-green-600 hover:bg-green-700 text-white px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 flex items-center gap-2 shadow-sm hover:shadow-md"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 4v16m8-8H4"
            />
          </svg>
          Añadir Estudiante
        </button>
      </div>
    </div>

    <!-- Mensaje de éxito de carga -->
    <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 translate-y-1"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="uploadMessage"
        class="bg-green-50 border-l-4 border-green-500 p-4 rounded-lg shadow-sm"
      >
        <div class="flex items-center">
          <svg class="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
              clip-rule="evenodd"
            />
          </svg>
          <p class="text-sm text-green-800 font-medium">{{ uploadMessage }}</p>
        </div>
      </div>
    </Transition>

    <!-- Mensaje de error -->
    <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 translate-y-1"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="error" class="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg shadow-sm">
        <div class="flex items-center">
          <svg class="w-5 h-5 text-red-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clip-rule="evenodd"
            />
          </svg>
          <p class="text-sm text-red-800 font-medium">{{ error }}</p>
        </div>
      </div>
    </Transition>

    <!-- Tabla de estudiantes -->
    <div class="bg-white shadow-sm rounded-lg overflow-hidden border border-gray-200">
      <table v-if="students.length > 0" class="min-w-full divide-y divide-gray-200 table-fixed">
        <thead class="bg-gray-50">
          <tr>
            <th
              class="w-3/12 px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider"
            >
              Nombre Completo
            </th>
            <th
              class="w-2/12 px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider whitespace-nowrap"
            >
              Número de Control
            </th>
            <th
              class="w-1/12 px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider"
            >
              Semestre
            </th>
            <th
              class="w-3/12 px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider"
            >
              Carrera
            </th>
            <th
              class="w-1/12 px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider"
            >
              Estado
            </th>
            <th
              class="w-2/12 px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider"
            >
              Acciones
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr
            v-for="student in students"
            :key="student.id_alumno"
            class="hover:bg-gray-50 transition-colors duration-150"
          >
            <td class="px-6 py-4 whitespace-nowrap overflow-hidden text-ellipsis">
              <div class="text-sm font-medium text-gray-900">
                {{
                  student.apellido_m
                    ? `${student.nombre} ${student.apellido_p} ${student.apellido_m}`
                    : `${student.nombre} ${student.apellido_p}`
                }}
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-700">{{ student.num_control }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-700">{{ student.semestre_actual }}°</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap overflow-hidden text-ellipsis">
              <div class="text-sm text-gray-700">{{ student.carrera }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span
                class="px-3 py-1 text-xs leading-5 font-semibold rounded-full"
                :class="
                  student.estado === 'A'
                    ? 'bg-green-100 text-green-800 border border-green-200'
                    : 'bg-gray-100 text-gray-600 border border-gray-200'
                "
              >
                {{ student.estado === 'A' ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <div class="flex items-center gap-2">
                <button
                  @click="editItem(student)"
                  class="text-white hover:bg-amber-600 px-3 py-2 bg-amber-500 rounded-lg transition-all duration-200 shadow-sm hover:shadow-md"
                  title="Editar"
                >
                  <EditIcon />
                </button>
                <button
                  @click="deleteItem(student)"
                  class="text-white hover:bg-red-700 px-3 py-2 rounded-lg bg-red-600 transition-all duration-200 shadow-sm hover:shadow-md"
                  title="Eliminar"
                >
                  <DeleteIcon />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Sin estudiantes -->
      <div
        v-if="!loading && students.length === 0"
        class="text-center py-16 px-4 bg-gray-50 rounded-lg"
      >
        <svg
          class="w-20 h-20 mx-auto mb-4 text-gray-300"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
          />
        </svg>
        <p class="text-lg font-medium text-gray-900 mb-1">No hay estudiantes registrados</p>
        <p class="text-sm text-gray-500">Comienza agregando estudiantes al sistema</p>
        <button
          @click="openModal('add')"
          class="mt-4 inline-flex items-center gap-2 text-[#0A3B76] hover:text-[#083060] font-medium text-sm"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 4v16m8-8H4"
            />
          </svg>
          Añadir primer estudiante
        </button>
      </div>
    </div>

    <!-- Paginación Estudiantes -->
    <div
      v-if="students.length > 0"
      class="bg-white rounded-lg px-6 py-4 flex items-center justify-between border border-gray-200 shadow-sm"
    >
      <div class="flex-1 flex items-center justify-between">
        <div>
          <p class="text-sm text-gray-700">
            Mostrando
            <span class="font-medium text-gray-900">{{
              (currentPage - 1) * itemsPerPage + 1
            }}</span>
            a
            <span class="font-medium text-gray-900">{{
              Math.min(currentPage * itemsPerPage, totalStudents)
            }}</span>
            de
            <span class="font-medium text-gray-900">{{ totalStudents }}</span>
            resultados
          </p>
        </div>
        <div>
          <nav
            class="relative z-0 inline-flex rounded-lg shadow-sm -space-x-px"
            aria-label="Pagination"
          >
            <button
              @click="prevPage"
              :disabled="currentPage === 1"
              class="relative inline-flex items-center px-4 py-2 rounded-l-lg border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
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
              <span class="ml-1">Anterior</span>
            </button>

            <span
              class="relative inline-flex items-center px-6 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700"
            >
              Página {{ currentPage }} de {{ totalPages }}
            </span>

            <button
              @click="nextPage"
              :disabled="currentPage >= totalPages"
              class="relative inline-flex items-center px-4 py-2 rounded-r-lg border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
            >
              <span class="mr-1">Siguiente</span>
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

    <!-- ==================== MODAL AÑADIR/EDITAR ESTUDIANTE ==================== -->
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
        class="fixed z-50 inset-0 overflow-y-auto"
        aria-labelledby="modal-title"
        role="dialog"
        aria-modal="true"
      >
        <div
          class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
        >
          <div
            class="fixed inset-0 bg-gray-900 bg-opacity-75 transition-opacity"
            @click="closeModal"
          ></div>

          <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true"
            >&#8203;</span
          >

          <div
            class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full"
          >
            <!-- Header -->
            <div class="bg-[#0A3B76] px-6 py-4 border-b-2 border-[#083060]">
              <div class="flex items-center gap-3">
                <svg
                  class="w-6 h-6 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                  />
                </svg>
                <h3 class="text-xl leading-6 font-bold text-white" id="modal-title">
                  {{ modalMode === 'add' ? 'Añadir Nuevo Estudiante' : 'Editar Estudiante' }}
                </h3>
              </div>
            </div>

            <!-- Body -->
            <div class="bg-white px-6 pt-5 pb-4">
              <form @submit.prevent="submitForm" class="space-y-6">
                <!-- Nombres -->
                <div class="grid grid-cols-1 gap-6 sm:grid-cols-3">
                  <div>
                    <label for="nombre" class="block text-sm font-medium text-gray-700 mb-1">
                      Nombre <span class="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      id="nombre"
                      v-model="formData.nombre"
                      class="block w-full py-2.5 px-3 border border-gray-300 bg-white rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-[#0A3B76] focus:border-[#0A3B76] sm:text-sm transition-colors duration-200"
                      :class="{ 'border-red-500 focus:ring-red-500': errors.nombre }"
                    />
                    <p v-if="errors.nombre" class="mt-1 text-sm text-red-600">
                      {{ errors.nombre[0] }}
                    </p>
                  </div>

                  <div>
                    <label for="apellido_p" class="block text-sm font-medium text-gray-700 mb-1">
                      Apellido Paterno <span class="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      id="apellido_p"
                      v-model="formData.apellido_p"
                      class="block w-full py-2.5 px-3 border border-gray-300 bg-white rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-[#0A3B76] focus:border-[#0A3B76] sm:text-sm transition-colors duration-200"
                      :class="{ 'border-red-500 focus:ring-red-500': errors.apellido_p }"
                    />
                    <p v-if="errors.apellido_p" class="mt-1 text-sm text-red-600">
                      {{ errors.apellido_p[0] }}
                    </p>
                  </div>

                  <div>
                    <label for="apellido_m" class="block text-sm font-medium text-gray-700 mb-1">
                      Apellido Materno
                    </label>
                    <input
                      type="text"
                      id="apellido_m"
                      v-model="formData.apellido_m"
                      class="block w-full py-2.5 px-3 border border-gray-300 bg-white rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-[#0A3B76] focus:border-[#0A3B76] sm:text-sm transition-colors duration-200"
                    />
                  </div>
                </div>

                <!-- Número de Control y Contraseña -->
                <div class="grid grid-cols-2 gap-6">
                  <div>
                    <label for="num_control" class="block text-sm font-medium text-gray-700 mb-1">
                      Número de Control <span class="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      id="num_control"
                      v-model="formData.num_control"
                      class="block w-full py-2.5 px-3 border border-gray-300 bg-white rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-[#0A3B76] focus:border-[#0A3B76] sm:text-sm transition-colors duration-200"
                      :class="{ 'border-red-500 focus:ring-red-500': errors.num_control }"
                    />
                    <p v-if="errors.num_control" class="mt-1 text-sm text-red-600">
                      {{ errors.num_control[0] }}
                    </p>
                  </div>

                  <div>
                    <label for="contraseña" class="block text-sm font-medium text-gray-700 mb-1">
                      Contraseña <span class="text-red-500">*</span>
                    </label>
                    <div class="relative">
                      <input
                        id="contraseña"
                        v-model="formData.contraseña"
                        :type="showPassword ? 'text' : 'password'"
                        class="block w-full py-2.5 px-3 pr-10 border border-gray-300 bg-white rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-[#0A3B76] focus:border-[#0A3B76] sm:text-sm transition-colors duration-200"
                        :class="{ 'border-red-500 focus:ring-red-500': errors.contraseña }"
                      />
                      <button
                        type="button"
                        @click="showPassword = !showPassword"
                        class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
                      >
                        <ShowEye v-if="showPassword" />
                        <HideEye v-else />
                      </button>
                    </div>
                    <p v-if="errors.contraseña" class="mt-1 text-sm text-red-600">
                      {{ errors.contraseña[0] }}
                    </p>
                  </div>
                </div>

                <!-- Correo y Teléfono -->
                <div class="grid grid-cols-2 gap-6">
                  <div>
                    <label for="correo" class="block text-sm font-medium text-gray-700 mb-1">
                      Correo <span class="text-red-500">*</span>
                    </label>
                    <input
                      type="email"
                      id="correo"
                      v-model="formData.correo"
                      class="block w-full py-2.5 px-3 border border-gray-300 bg-white rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-[#0A3B76] focus:border-[#0A3B76] sm:text-sm transition-colors duration-200"
                      :class="{ 'border-red-500 focus:ring-red-500': errors.correo }"
                    />
                    <p v-if="errors.correo" class="mt-1 text-sm text-red-600">
                      {{ errors.correo[0] }}
                    </p>
                  </div>

                  <div>
                    <label for="telefono" class="block text-sm font-medium text-gray-700 mb-1">
                      Teléfono
                    </label>
                    <input
                      type="text"
                      id="telefono"
                      v-model="formData.telefono"
                      class="block w-full py-2.5 px-3 border border-gray-300 bg-white rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-[#0A3B76] focus:border-[#0A3B76] sm:text-sm transition-colors duration-200"
                    />
                  </div>
                </div>

                <!-- Carrera -->
                <div>
                  <label for="carrera" class="block text-sm font-medium text-gray-700 mb-1">
                    Carrera <span class="text-red-500">*</span>
                  </label>
                  <select
                    id="carrera"
                    v-model="formData.carrera"
                    class="block w-full py-2.5 px-3 border border-gray-300 bg-white rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-[#0A3B76] focus:border-[#0A3B76] sm:text-sm transition-colors duration-200"
                    :class="{ 'border-red-500 focus:ring-red-500': errors.carrera }"
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
                    <option value="Ingeniería en Minera">Ingeniería en Minera</option>
                    <option value="Arquitectura">Arquitectura</option>
                  </select>
                  <p v-if="errors.carrera" class="mt-1 text-sm text-red-600">
                    {{ errors.carrera[0] }}
                  </p>
                </div>

                <!-- Semestre y Estado -->
                <div class="grid grid-cols-2 gap-6">
                  <div>
                    <label for="semestre" class="block text-sm font-medium text-gray-700 mb-1">
                      Semestre <span class="text-red-500">*</span>
                    </label>
                    <select
                      id="semestre"
                      v-model="formData.semestre_actual"
                      class="block w-full py-2.5 px-3 border border-gray-300 bg-white rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-[#0A3B76] focus:border-[#0A3B76] sm:text-sm transition-colors duration-200"
                      :class="{ 'border-red-500 focus:ring-red-500': errors.semestre_actual }"
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
                    <p v-if="errors.semestre_actual" class="mt-1 text-sm text-red-600">
                      {{ errors.semestre_actual[0] }}
                    </p>
                  </div>

                  <div>
                    <label for="estado" class="block text-sm font-medium text-gray-700 mb-1">
                      Estado <span class="text-red-500">*</span>
                    </label>
                    <select
                      id="estado"
                      v-model="formData.estado"
                      class="block w-full py-2.5 px-3 border border-gray-300 bg-white rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-[#0A3B76] focus:border-[#0A3B76] sm:text-sm transition-colors duration-200"
                      :class="{ 'border-red-500 focus:ring-red-500': errors.estado }"
                    >
                      <option value="A">Activo</option>
                      <option value="I">Inactivo</option>
                    </select>
                    <p v-if="errors.estado" class="mt-1 text-sm text-red-600">
                      {{ errors.estado[0] }}
                    </p>
                  </div>
                </div>

                <!-- Botones -->
                <div class="bg-gray-50 px-6 py-4 -mx-6 -mb-4 rounded-b-lg flex justify-end gap-3">
                  <button
                    @click="closeModal"
                    type="button"
                    class="px-6 py-2.5 rounded-lg border border-gray-300 shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all duration-200"
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    class="px-6 py-2.5 rounded-lg shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-all duration-200"
                  >
                    {{ modalMode === 'add' ? 'Añadir Estudiante' : 'Guardar Cambios' }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- ==================== MODAL CONFIRMAR ELIMINACIÓN ==================== -->
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
        class="fixed z-50 inset-0 overflow-y-auto"
        aria-labelledby="modal-title"
        role="dialog"
        aria-modal="true"
      >
        <div
          class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
        >
          <div class="fixed inset-0 bg-gray-900 bg-opacity-75 transition-opacity"></div>

          <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true"
            >&#8203;</span
          >

          <div
            class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
          >
            <div class="bg-white px-6 pt-6 pb-4">
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
                  <h3 class="text-lg leading-6 font-bold text-gray-900" id="modal-title">
                    Eliminar Estudiante
                  </h3>
                  <div class="mt-3">
                    <p class="text-sm text-gray-600">
                      ¿Estás seguro de que deseas eliminar a
                      <strong class="text-gray-900"
                        >{{ studentToDelete?.nombre }} {{ studentToDelete?.apellido_p }}
                        {{ studentToDelete?.apellido_m }}</strong
                      >?
                    </p>
                    <p class="text-sm text-red-600 font-medium mt-2">
                      Esta acción no se puede deshacer.
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div class="bg-gray-50 px-6 py-4 flex justify-end gap-3 rounded-b-lg">
              <button
                @click="cancelDelete"
                type="button"
                class="px-6 py-2.5 rounded-lg border border-gray-300 shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all duration-200"
              >
                Cancelar
              </button>
              <button
                @click="confirmDelete"
                type="button"
                class="px-6 py-2.5 rounded-lg shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-all duration-200"
              >
                Eliminar
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- ==================== MODAL CARGAR EXCEL ==================== -->
    <CargarAlumnosModal
      :show="showModalExcel"
      @close="showModalExcel = false"
      @upload-success="handleUploadSuccess"
    />
  </div>
</template>

<script setup>
import { alumnosAPI } from '@/api/alumnos'
import { ref, reactive, onMounted, watch } from 'vue'

// IMPORTS - COMPONENTS
import DeleteIcon from '@/components/icons/DeleteIcon.vue'
import EditIcon from '@/components/icons/EditIcon.vue'
import ShowEye from '@/components/icons/ShowEye.vue'
import HideEye from '@/components/icons/HideEye.vue'
import BaseSearchInput from '@/components/ui/BaseSearchInput.vue'
import CargarAlumnosModal from '@/components/student/CargarAlumnosModal.vue'

// ==================== STATE - DATA ====================
const students = ref([])
const loading = ref(true)
const error = ref(null)
const errors = ref({})
const uploadMessage = ref(null)

// ==================== STATE - PAGINATION & SEARCH ====================
const currentPage = ref(1)
const itemsPerPage = ref(5)
const searchQuery = ref('')
const hayMasAlumnos = ref(true)
const totalStudents = ref(0)
const totalPages = ref(1)
let debounceTimer = null

// ==================== STATE - MODALS ====================
const showModal = ref(false)
const showDeleteModal = ref(false)
const showModalExcel = ref(false)
const studentToDelete = ref(null)
const modalMode = ref('add') // 'add' | 'edit'
const showPassword = ref(false)

// ==================== STATE - FORM ====================
const formData = reactive({
  nombre: '',
  apellido_p: '',
  apellido_m: '',
  num_control: '',
  contraseña: '',
  carrera: '',
  semestre_actual: '',
  estado: 'A',
  correo: '',
  telefono: '',
})

// ==================== API CALLS ====================
const fetchStudents = async (page = currentPage.value) => {
  try {
    loading.value = true
    error.value = null

    const response = await alumnosAPI.getAll(page, itemsPerPage.value, searchQuery.value)

    students.value = response.data.alumnos
    hayMasAlumnos.value = response.data.alumnos.length === 5
    totalStudents.value = response.data.total_alumnos
    totalPages.value = Math.ceil(response.data.total_alumnos / itemsPerPage.value)
  } catch (err) {
    console.error('Error al obtener los estudiantes:', err)

    if (err.response?.data?.detail?.[0]?.type === 'string_too_short') {
      error.value = 'Favor de ingresar mínimo 3 caracteres a buscar'
    } else {
      error.value = 'No se pudo cargar la lista de estudiantes'
    }
    students.value = []
  } finally {
    loading.value = false
  }
}

const submitForm = async () => {
  try {
    errors.value = {}
    let response

    if (modalMode.value === 'add') {
      response = await alumnosAPI.create(formData)

      if (response.status === 201) {
        console.log('Alumno agregado exitosamente:', response.data)
        await fetchStudents()
        closeModal()
      }
    } else if (modalMode.value === 'edit') {
      response = await alumnosAPI.update(formData.id_alumno, formData)

      if (response.status === 200) {
        console.log('Alumno actualizado exitosamente:', response.data)
        await fetchStudents()
        closeModal()
      }
    }
  } catch (error) {
    console.error('Error al enviar el formulario:', error)

    if (error.response?.data?.errors) {
      errors.value = error.response.data.errors
    } else {
      errors.value = { general: 'Ocurrió un error al procesar la solicitud.' }
    }
  }
}

const confirmDelete = async () => {
  if (studentToDelete.value) {
    try {
      const response = await alumnosAPI.delete(studentToDelete.value.id_alumno)

      if (response.status === 204) {
        console.log('Estudiante eliminado exitosamente')
        await fetchStudents()
      }
    } catch (error) {
      console.error('Error al eliminar el estudiante:', error)
      error.value = 'No se pudo eliminar el estudiante'
    } finally {
      showDeleteModal.value = false
      studentToDelete.value = null
    }
  }
}

// ==================== EVENT HANDLERS ====================
const openModal = (mode = 'add', item = null) => {
  modalMode.value = mode
  showModal.value = true
  clearErrors()

  // Limpiar formulario
  Object.keys(formData).forEach((key) => {
    delete formData[key]
  })

  if (mode === 'edit' && item) {
    // eslint-disable-next-line no-unused-vars
    const { contraseña, ...rest } = item
    Object.assign(formData, rest)
    formData.contraseña = '' // Reset password
  } else {
    Object.assign(formData, {
      nombre: '',
      apellido_p: '',
      apellido_m: '',
      num_control: '',
      contraseña: '',
      carrera: '',
      semestre_actual: '',
      estado: 'A',
      correo: '',
      telefono: '',
    })
  }
}

const closeModal = () => {
  showModal.value = false
  showPassword.value = false
  clearErrors()
}

const editItem = (student) => {
  openModal('edit', student)
}

const deleteItem = (student) => {
  studentToDelete.value = student
  showDeleteModal.value = true
}

const cancelDelete = () => {
  showDeleteModal.value = false
  studentToDelete.value = null
}

const handleUploadSuccess = () => {
  console.log('¡Éxito! Archivo cargado y datos procesados.')
  uploadMessage.value = '✅ Estudiantes cargados exitosamente'
  currentPage.value = 1
  fetchStudents()

  setTimeout(() => {
    uploadMessage.value = null
  }, 3000)
}

// ==================== UTILITY FUNCTIONS ====================
const clearErrors = () => {
  errors.value = {}
}

// ==================== PAGINATION ====================
const nextPage = () => {
  if (hayMasAlumnos.value) {
    currentPage.value++
    fetchStudents(currentPage.value)
  }
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    fetchStudents(currentPage.value)
  }
}

// ==================== WATCHERS ====================
watch(searchQuery, () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    currentPage.value = 1
    fetchStudents()
  }, 500)
})

// ==================== LIFECYCLE HOOKS ====================
onMounted(async () => {
  await fetchStudents(currentPage.value)
})
</script>
