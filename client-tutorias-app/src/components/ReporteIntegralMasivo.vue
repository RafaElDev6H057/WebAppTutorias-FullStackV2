<template>
  <div class="fixed inset-0 bg-gray-900 bg-opacity-75 overflow-hidden flex flex-col z-[9999]">
    <div class="flex-1 flex flex-col max-h-screen">
      <!-- Header con más color -->
      <div class="bg-[#0A3B76] shadow-2xl p-6 text-white flex-shrink-0">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-3xl font-bold drop-shadow-md">Reporte Integral de Tutoría</h1>
            <p class="text-white/90 text-sm mt-1 font-medium">Periodo 22025</p>
          </div>
          <button
            @click="closeModal"
            class="text-white hover:bg-white/20 rounded-full p-2 transition-all duration-200"
          >
            <svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2.5"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Información del Tutor con color -->
      <div
        class="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 shadow-md flex-shrink-0 border-b-2 border-[#ffccc6]"
      >
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="bg-white p-3 rounded-lg shadow-sm border-l-4 border-[#ff5242]">
            <label class="block text-xs font-medium text-gray-600 mb-1">Nombre del Tutor</label>
            <p class="text-sm font-semibold text-gray-900">{{ tutorInfo.nombre }}</p>
          </div>
          <div class="bg-white p-3 rounded-lg shadow-sm border-l-4 border-blue-500">
            <label class="block text-xs font-medium text-gray-600 mb-1"
              >Departamento Académico</label
            >
            <p class="text-sm font-semibold text-gray-900">{{ tutorInfo.departamento }}</p>
          </div>
          <div class="bg-white p-3 rounded-lg shadow-sm border-l-4 border-green-500">
            <label class="block text-xs font-medium text-gray-600 mb-1">Periodo Semestral</label>
            <p class="text-sm font-semibold text-gray-900">{{ tutorInfo.periodo }}</p>
          </div>
          <div class="bg-white p-3 rounded-lg shadow-sm border-l-4 border-purple-500">
            <label class="block text-xs font-medium text-gray-600 mb-1">Carrera</label>
            <p class="text-sm font-semibold text-gray-900">{{ tutorInfo.carrera }}</p>
          </div>
        </div>
      </div>

      <!-- Toolbar con color -->
      <div
        class="bg-gradient-to-r from-gray-50 to-gray-100 p-4 shadow-md flex flex-col md:flex-row justify-between items-start md:items-center gap-4 flex-shrink-0 border-b border-gray-300"
      >
        <div class="flex-1 max-w-md">
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Buscar alumno por nombre o número de control..."
              class="w-full pl-10 pr-4 py-2.5 border-2 border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-[#ff6b5b] focus:border-[#ff6b5b] transition-all"
            />
            <svg
              class="absolute left-3 top-3 h-5 w-5 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
        </div>
        <div class="flex gap-3 items-center">
          <span
            class="text-sm font-medium text-gray-700 bg-white px-3 py-2 rounded-lg shadow-sm border border-gray-200"
          >
            📊 Mostrando <strong class="text-[#ff5242]">{{ alumnosFiltrados.length }}</strong> de
            <strong class="text-[#ff5242]">{{ totalAlumnos }}</strong> alumnos
          </span>
          <button
            v-if="isLoadingMore"
            disabled
            class="px-6 py-2.5 bg-gray-400 text-white rounded-lg font-medium cursor-not-allowed inline-flex items-center shadow-md"
          >
            <svg
              class="animate-spin -ml-1 mr-2 h-5 w-5 text-white"
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
            Cargando...
          </button>
          <button
            v-else
            @click="guardarTodo"
            :disabled="isSaving || alumnosFiltrados.length === 0"
            class="px-6 py-2.5 bg-[#0A3B76] text-white rounded-lg font-bold hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#0A3B76] disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl transform hover:scale-105 inline-flex items-center"
          >
            <svg
              v-if="isSaving"
              class="animate-spin -ml-1 mr-2 h-5 w-5 text-white"
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
            <svg v-else class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"
              />
            </svg>
            {{ isSaving ? 'Guardando...' : 'Guardar Todo' }}
          </button>
        </div>
      </div>

      <!-- Banner de Etapa -->
      <Transition
        enter-active-class="transition ease-out duration-300"
        enter-from-class="opacity-0 translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-200"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="!isLoadingConfig"
          :class="[
            'mx-4 mt-2 p-4 rounded-md border-l-4 shadow-md',
            {
              'bg-red-50 border-red-500': reporteIntegralEtapa === 0,
              'bg-yellow-50 border-yellow-500': reporteIntegralEtapa === 1,
              'bg-blue-50 border-blue-500': reporteIntegralEtapa === 2,
              'bg-green-50 border-green-500': reporteIntegralEtapa === 3,
            },
          ]"
        >
          <div class="flex items-start">
            <svg
              :class="[
                'w-6 h-6 mr-3 flex-shrink-0',
                {
                  'text-red-500': reporteIntegralEtapa === 0,
                  'text-yellow-500': reporteIntegralEtapa === 1,
                  'text-blue-500': reporteIntegralEtapa === 2,
                  'text-green-500': reporteIntegralEtapa === 3,
                },
              ]"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                v-if="reporteIntegralEtapa === 0"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
              />
              <path
                v-else
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <p
              :class="[
                'text-sm font-medium flex-1',
                {
                  'text-red-800': reporteIntegralEtapa === 0,
                  'text-yellow-800': reporteIntegralEtapa === 1,
                  'text-blue-800': reporteIntegralEtapa === 2,
                  'text-green-800': reporteIntegralEtapa === 3,
                },
              ]"
            >
              {{ mensajeEtapa }}
            </p>
          </div>
        </div>
      </Transition>

      <!-- Mensajes de éxito/error -->
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
          class="mx-4 mt-2 p-4 bg-gradient-to-r from-green-50 to-emerald-50 border-l-4 border-green-500 rounded-md flex items-start flex-shrink-0 shadow-md"
        >
          <svg
            class="w-6 h-6 text-green-500 mr-3 flex-shrink-0"
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
          <div class="flex-1">
            <p class="text-sm font-bold text-green-800">{{ successMessage }}</p>
          </div>
          <button @click="successMessage = null" class="text-green-500 hover:text-green-700 ml-4">
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

      <Transition
        enter-active-class="transition ease-out duration-300"
        enter-from-class="opacity-0 translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-200"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="errorMessage"
          class="mx-4 mt-2 p-4 bg-gradient-to-r from-red-50 to-pink-50 border-l-4 border-red-500 rounded-md flex items-start flex-shrink-0 shadow-md"
        >
          <svg
            class="w-6 h-6 text-red-500 mr-3 flex-shrink-0"
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
            <p class="text-sm font-bold text-red-800">{{ errorMessage }}</p>
          </div>
          <button @click="errorMessage = null" class="text-red-500 hover:text-red-700 ml-4">
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

      <!-- Tabla de Alumnos con Scroll Horizontal -->
      <div class="flex-1 overflow-hidden bg-white shadow-xl rounded-xl border-2 border-gray-200">
        <div class="h-full overflow-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-[#0A3B76] sticky top-0 z-20 shadow-md">
              <tr>
                <th
                  class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider sticky left-0 bg-[#0A3B76] z-30 border-r border-gray-300 min-w-[200px]"
                >
                  Alumno
                </th>
                <th
                  class="px-4 py-4 text-center text-xs font-bold text-white uppercase tracking-wider min-w-[100px]"
                >
                  Tutoría Grupal
                </th>
                <th
                  class="px-4 py-4 text-center text-xs font-bold text-white uppercase tracking-wider min-w-[120px]"
                >
                  Tutoría Individual
                </th>
                <th
                  class="px-4 py-4 text-left text-xs font-bold text-white uppercase tracking-wider min-w-[180px]"
                >
                  Seguimiento 1
                </th>
                <th
                  class="px-4 py-4 text-left text-xs font-bold text-white uppercase tracking-wider min-w-[180px]"
                >
                  Seguimiento 2
                </th>
                <th
                  class="px-4 py-4 text-left text-xs font-bold text-white uppercase tracking-wider min-w-[180px]"
                >
                  Seguimiento 3
                </th>
                <th
                  class="px-4 py-4 text-center text-xs font-bold text-white uppercase tracking-wider min-w-[180px]"
                >
                  Área Canalizada
                </th>
                <th
                  class="px-4 py-4 text-center text-xs font-bold text-white uppercase tracking-wider min-w-[100px]"
                >
                  Mat. Aprob.
                </th>
                <th
                  class="px-4 py-4 text-left text-xs font-bold text-white uppercase tracking-wider min-w-[180px]"
                >
                  Mat. No Aprob.
                </th>
                <th
                  class="px-4 py-4 text-center text-xs font-bold text-white uppercase tracking-wider min-w-[120px]"
                >
                  Estado
                </th>
                <th
                  class="px-4 py-4 text-center text-xs font-bold text-white uppercase tracking-wider bg-[#0A3B76] z-30 border-l border-gray-300 min-w-[180px]"
                >
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr
                v-for="alumno in alumnosFiltrados"
                :key="alumno.num_control"
                class="hover:bg-blue-50 transition-colors"
              >
                <!-- Columna Alumno (sticky) -->
                <td
                  class="px-6 py-4 whitespace-nowrap sticky left-0 bg-white hover:bg-blue-50 z-10 border-r border-gray-200"
                >
                  <div class="flex flex-col">
                    <span class="text-sm font-bold text-gray-900">{{ alumno.nombre }}</span>
                    <span class="text-xs text-gray-500 font-medium">{{ alumno.num_control }}</span>
                  </div>
                </td>

                <!-- Tutoría Grupal con validación -->
                <td class="px-4 py-4 whitespace-nowrap text-center">
                  <div class="relative">
                    <input
                      v-model.number="alumno.datos.tutoria_grupal"
                      @input="validarTutoriaGrupal(alumno)"
                      type="number"
                      min="0"
                      max="16"
                      :disabled="alumno.modoVer || !camposHabilitados.tutoria_grupal"
                      :class="[
                        'w-20 px-3 py-2 text-center border-2 rounded-lg focus:outline-none focus:ring-2 transition-all',
                        alumno.modoVer ? 'bg-gray-100 cursor-not-allowed' : '',
                        alumno.errores?.tutoria_grupal
                          ? 'border-red-500 focus:ring-red-500 focus:border-red-500 bg-red-50'
                          : 'border-gray-300 focus:ring-[#ff6b5b] focus:border-[#ff6b5b]',
                      ]"
                    />
                    <Transition
                      enter-active-class="transition ease-out duration-200"
                      enter-from-class="opacity-0 scale-95"
                      enter-to-class="opacity-100 scale-100"
                      leave-active-class="transition ease-in duration-150"
                      leave-from-class="opacity-100"
                      leave-to-class="opacity-0"
                    >
                      <div
                        v-if="alumno.errores?.tutoria_grupal"
                        class="absolute top-full left-1/2 transform -translate-x-1/2 mt-1 px-2 py-1 bg-red-500 text-white text-xs rounded shadow-lg whitespace-nowrap z-50"
                      >
                        {{ alumno.errores.tutoria_grupal }}
                      </div>
                    </Transition>
                  </div>
                </td>

                <!-- Tutoría Individual con validación -->
                <td class="px-4 py-4 whitespace-nowrap text-center">
                  <div class="relative">
                    <input
                      v-model.number="alumno.datos.tutoria_individual"
                      @input="validarTutoriaIndividual(alumno)"
                      type="number"
                      min="0"
                      max="5"
                      :disabled="alumno.modoVer || !camposHabilitados.tutoria_individual"
                      :class="[
                        'w-20 px-3 py-2 text-center border-2 rounded-lg focus:outline-none focus:ring-2 transition-all',
                        alumno.modoVer ? 'bg-gray-100 cursor-not-allowed' : '',
                        alumno.errores?.tutoria_individual
                          ? 'border-red-500 focus:ring-red-500 focus:border-red-500 bg-red-50'
                          : 'border-gray-300 focus:ring-[#ff6b5b] focus:border-[#ff6b5b]',
                      ]"
                    />
                    <Transition
                      enter-active-class="transition ease-out duration-200"
                      enter-from-class="opacity-0 scale-95"
                      enter-to-class="opacity-100 scale-100"
                      leave-active-class="transition ease-in duration-150"
                      leave-from-class="opacity-100"
                      leave-to-class="opacity-0"
                    >
                      <div
                        v-if="alumno.errores?.tutoria_individual"
                        class="absolute top-full left-1/2 transform -translate-x-1/2 mt-1 px-2 py-1 bg-red-500 text-white text-xs rounded shadow-lg whitespace-nowrap z-50"
                      >
                        {{ alumno.errores.tutoria_individual }}
                      </div>
                    </Transition>
                  </div>
                </td>

                <!-- Seguimiento 1 -->
                <td class="px-4 py-4">
                  <input
                    v-model="alumno.datos.seguimiento_1"
                    type="text"
                    placeholder="Ej: Cálculo, Álgebra..."
                    :disabled="alumno.modoVer || !camposHabilitados.seguimiento_1"
                    :class="[
                      'w-full px-3 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#ff6b5b] focus:border-[#ff6b5b] text-sm transition-all',
                      alumno.modoVer || !camposHabilitados.seguimiento_1
                        ? 'bg-gray-100 cursor-not-allowed opacity-60'
                        : '',
                    ]"
                  />
                </td>

                <!-- Seguimiento 2 -->
                <td class="px-4 py-4">
                  <input
                    v-model="alumno.datos.seguimiento_2"
                    type="text"
                    placeholder="Ej: Programación..."
                    :disabled="alumno.modoVer || !camposHabilitados.seguimiento_2"
                    :class="[
                      'w-full px-3 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#ff6b5b] focus:border-[#ff6b5b] text-sm transition-all',
                      alumno.modoVer || !camposHabilitados.seguimiento_2
                        ? 'bg-gray-100 cursor-not-allowed opacity-60'
                        : '',
                    ]"
                  />
                </td>

                <!-- Seguimiento 3 -->
                <td class="px-4 py-4">
                  <input
                    v-model="alumno.datos.seguimiento_3"
                    type="text"
                    placeholder="Ej: Física..."
                    :disabled="alumno.modoVer || !camposHabilitados.seguimiento_3"
                    :class="[
                      'w-full px-3 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#ff6b5b] focus:border-[#ff6b5b] text-sm transition-all',
                      alumno.modoVer || !camposHabilitados.seguimiento_3
                        ? 'bg-gray-100 cursor-not-allowed opacity-60'
                        : '',
                    ]"
                  />
                </td>

                <!-- Área Canalizada (Checkboxes con color) -->
                <td class="px-4 py-4">
                  <div class="flex flex-col gap-2 text-xs">
                    <label
                      class="flex items-center cursor-pointer hover:bg-gray-50 p-1 rounded transition-colors"
                    >
                      <input
                        v-model="alumno.datos.jefatura_academica"
                        type="checkbox"
                        :true-value="1"
                        :false-value="0"
                        :disabled="alumno.modoVer || !camposHabilitados.jefatura_academica"
                        class="rounded border-gray-300 text-blue-600 focus:ring-blue-500 h-4 w-4 disabled:opacity-50 disabled:cursor-not-allowed"
                      />
                      <span class="ml-2 text-gray-700 font-medium">Jef. Acad.</span>
                    </label>
                    <label
                      class="flex items-center cursor-pointer hover:bg-gray-50 p-1 rounded transition-colors"
                    >
                      <input
                        v-model="alumno.datos.ciencias_basicas"
                        type="checkbox"
                        :true-value="1"
                        :false-value="0"
                        :disabled="alumno.modoVer || !camposHabilitados.ciencias_basicas"
                        class="rounded border-gray-300 text-green-600 focus:ring-green-500 h-4 w-4 disabled:opacity-50 disabled:cursor-not-allowed"
                      />
                      <span class="ml-2 text-gray-700 font-medium">C. Básicas</span>
                    </label>
                    <label
                      class="flex items-center cursor-pointer hover:bg-gray-50 p-1 rounded transition-colors"
                    >
                      <input
                        v-model="alumno.datos.psicologia"
                        type="checkbox"
                        :true-value="1"
                        :false-value="0"
                        :disabled="alumno.modoVer || !camposHabilitados.psicologia"
                        class="rounded border-gray-300 text-purple-600 focus:ring-purple-500 h-4 w-4 disabled:opacity-50 disabled:cursor-not-allowed"
                      />
                      <span class="ml-2 text-gray-700 font-medium">Psicología</span>
                    </label>
                  </div>
                </td>

                <!-- Materias Aprobadas con validación -->
                <td class="px-4 py-4 whitespace-nowrap text-center">
                  <div class="relative">
                    <input
                      v-model.number="alumno.datos.materias_aprobadas"
                      @input="validarMateriasAprobadas(alumno)"
                      type="number"
                      min="0"
                      :disabled="alumno.modoVer || !camposHabilitados.materias_aprobadas"
                      :class="[
                        'w-20 px-3 py-2 text-center border-2 rounded-lg focus:outline-none focus:ring-2 transition-all',
                        alumno.modoVer ? 'bg-gray-100 cursor-not-allowed' : '',
                        alumno.errores?.materias_aprobadas
                          ? 'border-red-500 focus:ring-red-500 focus:border-red-500 bg-red-50'
                          : 'border-gray-300 focus:ring-[#ff6b5b] focus:border-[#ff6b5b]',
                      ]"
                    />
                    <Transition
                      enter-active-class="transition ease-out duration-200"
                      enter-from-class="opacity-0 scale-95"
                      enter-to-class="opacity-100 scale-100"
                      leave-active-class="transition ease-in duration-150"
                      leave-from-class="opacity-100"
                      leave-to-class="opacity-0"
                    >
                      <div
                        v-if="alumno.errores?.materias_aprobadas"
                        class="absolute top-full left-1/2 transform -translate-x-1/2 mt-1 px-2 py-1 bg-red-500 text-white text-xs rounded shadow-lg whitespace-nowrap z-50"
                      >
                        {{ alumno.errores.materias_aprobadas }}
                      </div>
                    </Transition>
                  </div>
                </td>

                <!-- Materias No Aprobadas -->
                <td class="px-4 py-4">
                  <input
                    v-model="alumno.datos.materias_no_aprobadas"
                    type="text"
                    placeholder="Ej: Bases de Datos..."
                    :disabled="alumno.modoVer || !camposHabilitados.materias_no_aprobadas"
                    :class="[
                      'w-full px-3 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#ff6b5b] focus:border-[#ff6b5b] text-sm transition-all',
                      alumno.modoVer ? 'bg-gray-100 cursor-not-allowed' : '',
                    ]"
                  />
                </td>

                <!-- Estado con colores mejorados -->
                <td class="px-4 py-4 whitespace-nowrap text-center">
                  <span
                    v-if="alumno.estado === 'guardado'"
                    class="inline-flex items-center px-3 py-1.5 rounded-full text-xs font-bold bg-gradient-to-r from-green-400 to-emerald-500 text-white shadow-md"
                  >
                    <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fill-rule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                    Guardado
                  </span>
                  <span
                    v-else-if="alumno.estado === 'guardando'"
                    class="inline-flex items-center px-3 py-1.5 rounded-full text-xs font-bold bg-gradient-to-r from-blue-400 to-indigo-500 text-white shadow-md"
                  >
                    <svg
                      class="animate-spin w-4 h-4 mr-1"
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
                    Guardando...
                  </span>
                  <span
                    v-else-if="alumno.estado === 'error'"
                    class="inline-flex items-center px-3 py-1.5 rounded-full text-xs font-bold bg-gradient-to-r from-red-400 to-pink-500 text-white shadow-md"
                  >
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                    Error
                  </span>
                  <span
                    v-else
                    class="inline-flex items-center px-3 py-1.5 rounded-full text-xs font-bold bg-gradient-to-r from-yellow-400 to-orange-500 text-white shadow-md"
                  >
                    Pendiente
                  </span>
                </td>

                <!-- Acciones DINÁMICAS -->
                <td
                  class="px-4 py-4 whitespace-nowrap text-center bg-white hover:bg-blue-50 z-10 border-l border-gray-200"
                >
                  <!-- Si está en modo VER -->
                  <div v-if="alumno.modoVer" class="flex gap-2 justify-center">
                    <button
                      @click="cerrarVistaReporte(alumno)"
                      class="px-3 py-2 rounded-lg bg-gray-500 text-white hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all text-xs font-bold shadow-md"
                    >
                      ✖️ Cerrar
                    </button>
                  </div>

                  <!-- Si NO está guardado (pendiente) -->
                  <button
                    v-else-if="alumno.estado === 'pendiente'"
                    @click="guardarAlumno(alumno)"
                    :disabled="alumno.estado === 'guardando' || tieneErrores(alumno)"
                    :class="[
                      'px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 transition-all text-xs font-bold shadow-md transform hover:scale-105',
                      tieneErrores(alumno)
                        ? 'bg-gray-400 text-gray-700 cursor-not-allowed' // Gris institucional
                        : 'bg-[#0A3B76] text-white hover:bg-blue-800 focus:ring-[#0A3B76]', // Azul institucional
                    ]"
                  >
                    {{ tieneErrores(alumno) ? 'Errores' : 'Guardar' }}
                  </button>

                  <!-- Si está GUARDADO - Botones Ver/Editar/Eliminar -->
                  <div v-else-if="alumno.estado === 'guardado'" class="flex gap-2 justify-center">
                    <button
                      @click="verReporte(alumno)"
                      class="px-3 py-2 rounded-lg bg-blue-500 text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all text-xs font-bold shadow-md"
                      title="Ver reporte"
                    >
                      👁️
                    </button>
                    <button
                      @click="editarReporte(alumno)"
                      :disabled="alumno.estado === 'guardando' || tieneErrores(alumno)"
                      :class="[
                        'px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 transition-all text-xs font-bold shadow-md',
                        tieneErrores(alumno)
                          ? 'bg-gray-400 text-gray-700 cursor-not-allowed'
                          : 'bg-gradient-to-r from-[#ff5242] to-[#ff3d2a] text-white hover:from-[#ff3d2a] hover:to-[#e62a1a] focus:ring-[#ff6b5b]',
                      ]"
                      title="Editar y actualizar"
                    >
                      ✏️
                    </button>
                    <button
                      @click="eliminarReporte(alumno)"
                      class="px-3 py-2 rounded-lg bg-red-500 text-white hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-all text-xs font-bold shadow-md"
                      title="Eliminar reporte"
                    >
                      🗑️
                    </button>
                  </div>

                  <!-- Si está GUARDANDO -->
                  <div v-else-if="alumno.estado === 'guardando'" class="flex justify-center">
                    <div
                      class="px-4 py-2 rounded-lg bg-blue-400 text-white text-xs font-bold inline-flex items-center"
                    >
                      <svg
                        class="animate-spin w-4 h-4 mr-1"
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
                      ...
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Estado vacío -->
          <div
            v-if="alumnosFiltrados.length === 0 && !isLoadingMore"
            class="text-center py-16 px-4 bg-gradient-to-br from-gray-50 to-gray-100"
          >
            <svg
              class="mx-auto h-20 w-20 text-gray-400"
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
            <h3 class="mt-4 text-xl font-bold text-gray-900">No se encontraron alumnos</h3>
            <p class="mt-2 text-sm text-gray-600">No hay alumnos que coincidan con tu búsqueda.</p>
          </div>
        </div>
      </div>

      <!-- Footer con información y color -->
      <div
        class="p-4 bg-gradient-to-r from-gray-100 to-gray-200 shadow-inner text-sm font-medium text-gray-700 flex-shrink-0 border-t-2 border-gray-300"
      >
        <div class="flex justify-between items-center">
          <p>
            <strong class="text-[#ff5242]">Total de alumnos:</strong> {{ totalAlumnos }} |
            <strong class="text-green-600">Guardados:</strong> {{ alumnosGuardados }} |
            <strong class="text-yellow-600">Pendientes:</strong> {{ alumnosPendientes }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { tutoriasAPI } from '@/api/tutorias'
import { reportesAPI } from '@/api/reportes'
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

// ==================== PROPS ====================
const props = defineProps({
  tutorInfo: {
    type: Object,
    required: true,
  },
  tutorId: {
    type: Number,
    required: true,
  },
})

// ==================== EMITS ====================
const emit = defineEmits(['close', 'success'])

// ==================== STATE ====================
const searchQuery = ref('')
const isSaving = ref(false)
const isLoadingMore = ref(false)
const successMessage = ref(null)
const errorMessage = ref(null)
const alumnos = ref([])
const totalAlumnos = ref(0)

// ==================== CONFIGURACIÓN ETAPAS ====================
const reporteIntegralEtapa = ref(0)
const isLoadingConfig = ref(false)

// ==================== COMPUTED ====================
const alumnosFiltrados = computed(() => {
  if (!searchQuery.value) return alumnos.value

  const query = searchQuery.value.toLowerCase()
  return alumnos.value.filter(
    (alumno) =>
      alumno.nombre.toLowerCase().includes(query) ||
      alumno.num_control.toLowerCase().includes(query),
  )
})

const alumnosGuardados = computed(() => {
  return alumnos.value.filter((a) => a.estado === 'guardado').length
})

const alumnosPendientes = computed(() => {
  return alumnos.value.filter((a) => a.estado === 'pendiente').length
})

// ==================== COMPUTED ETAPAS ====================
const camposHabilitados = computed(() => ({
  seguimiento_1: reporteIntegralEtapa.value >= 1,
  seguimiento_2: reporteIntegralEtapa.value >= 2,
  seguimiento_3: reporteIntegralEtapa.value >= 3,
  tutoria_grupal: reporteIntegralEtapa.value >= 3,
  tutoria_individual: reporteIntegralEtapa.value >= 3,
  jefatura_academica: reporteIntegralEtapa.value >= 3,
  ciencias_basicas: reporteIntegralEtapa.value >= 3,
  psicologia: reporteIntegralEtapa.value >= 3,
  materias_aprobadas: reporteIntegralEtapa.value >= 3,
  materias_no_aprobadas: reporteIntegralEtapa.value >= 3,
}))

const mensajeEtapa = computed(() => {
  switch (reporteIntegralEtapa.value) {
    case 0:
      return '🔒 El reporte integral no está disponible aún. Espera a que el administrador habilite el primer seguimiento.'
    case 1:
      return '📝 Etapa 1: Solo puedes llenar el Seguimiento 1.'
    case 2:
      return '📝 Etapa 2: Puedes llenar los Seguimientos 1 y 2.'
    case 3:
      return '✅ Etapa 3: Todos los campos están disponibles para completar el reporte integral.'
    default:
      return '⏳ Cargando configuración...'
  }
})

// eslint-disable-next-line no-unused-vars
const colorBannerEtapa = computed(() => {
  switch (reporteIntegralEtapa.value) {
    case 0:
      return 'red'
    case 1:
      return 'yellow'
    case 2:
      return 'blue'
    case 3:
      return 'green'
    default:
      return 'gray'
  }
})

// ==================== VALIDACIONES ====================
const validarTutoriaGrupal = (alumno) => {
  if (!alumno.errores) {
    alumno.errores = {}
  }

  if (alumno.datos.tutoria_grupal < 0) {
    alumno.errores.tutoria_grupal = '❌ El número debe ser mayor o igual a 0'
  } else if (alumno.datos.tutoria_grupal > 16) {
    alumno.errores.tutoria_grupal = '❌ El número debe ser menor o igual a 16'
  } else {
    delete alumno.errores.tutoria_grupal
  }
}

const validarTutoriaIndividual = (alumno) => {
  if (!alumno.errores) {
    alumno.errores = {}
  }

  if (alumno.datos.tutoria_individual < 0) {
    alumno.errores.tutoria_individual = '❌ El número debe ser mayor o igual a 0'
  } else if (alumno.datos.tutoria_individual > 5) {
    alumno.errores.tutoria_individual = '❌ El número debe ser menor o igual a 5'
  } else {
    delete alumno.errores.tutoria_individual
  }
}

const validarMateriasAprobadas = (alumno) => {
  if (!alumno.errores) {
    alumno.errores = {}
  }

  if (alumno.datos.materias_aprobadas < 0) {
    alumno.errores.materias_aprobadas = '❌ El número debe ser mayor o igual a 0'
  } else {
    delete alumno.errores.materias_aprobadas
  }
}

const tieneErrores = (alumno) => {
  return alumno.errores && Object.keys(alumno.errores).length > 0
}

// ==================== CONFIGURACIÓN ====================
const fetchConfiguracion = async () => {
  try {
    isLoadingConfig.value = true
    const token = localStorage.getItem('accessToken')

    const response = await axios.get('http://localhost:8000/api/configuracion/', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (response.status === 200) {
      reporteIntegralEtapa.value = response.data.reporte_integral_etapa
      console.log('✅ Etapa de reporte integral:', reporteIntegralEtapa.value)
    }
  } catch (error) {
    console.error('❌ Error al obtener configuración:', error)
    reporteIntegralEtapa.value = 0 // Por defecto bloqueado
    errorMessage.value =
      'No se pudo cargar la configuración del reporte. Los campos estarán bloqueados.'
  } finally {
    isLoadingConfig.value = false
  }
}

// ==================== CARGAR DATOS ====================
const cargarTodosLosAlumnos = async () => {
  isLoadingMore.value = true
  errorMessage.value = null

  try {
    const responseInicial = await tutoriasAPI.getByTutor(props.tutorId, 1, 1, '')
    totalAlumnos.value = responseInicial.data.total_tutorias

    const response = await tutoriasAPI.getByTutor(props.tutorId, 1, totalAlumnos.value, '')

    console.log('Response completa:', response.data)

    // Mapear alumnos y SIEMPRE intentar cargar datos existentes
    alumnos.value = await Promise.all(
      response.data.tutorias.map(async (tutoria) => {
        const alumno = {
          nombre: tutoria.alumno
            ? `${tutoria.alumno.nombre || ''} ${tutoria.alumno.apellido_p || ''} ${tutoria.alumno.apellido_m || ''}`.trim()
            : 'Alumno Desconocido',
          num_control: tutoria.alumno?.num_control || 'N/A',
          id_tutoria: tutoria.id_tutoria,
          estado: tutoria.reporte_integral_guardado ? 'guardado' : 'pendiente',
          modoVer: false,
          errores: {},
          datos: {
            tutoria_grupal: 0,
            tutoria_individual: 0,
            seguimiento_1: '',
            seguimiento_2: '',
            seguimiento_3: '',
            jefatura_academica: 0,
            ciencias_basicas: 0,
            psicologia: 0,
            materias_aprobadas: 0,
            materias_no_aprobadas: '',
          },
        }

        // SIEMPRE intentar cargar datos existentes (no solo si reporte_integral_guardado es true)
        try {
          const reporteResponse = await reportesAPI.getIntegralByTutoria(tutoria.id_tutoria)

          if (reporteResponse.status === 200) {
            // Cargar TODOS los datos que existan, incluso si solo tienen seguimiento_1
            alumno.datos = {
              tutoria_grupal: reporteResponse.data.tutoria_grupal || 0,
              tutoria_individual: reporteResponse.data.tutoria_individual || 0,
              seguimiento_1: reporteResponse.data.seguimiento_1 || '',
              seguimiento_2: reporteResponse.data.seguimiento_2 || '',
              seguimiento_3: reporteResponse.data.seguimiento_3 || '',
              jefatura_academica: reporteResponse.data.jefatura_academica || 0,
              ciencias_basicas: reporteResponse.data.ciencias_basicas || 0,
              psicologia: reporteResponse.data.psicologia || 0,
              materias_aprobadas: reporteResponse.data.materias_aprobadas || 0,
              materias_no_aprobadas: reporteResponse.data.materias_no_aprobadas || '',
            }
            alumno.reporte_id = reporteResponse.data.id

            // Si tiene algún dato guardado, marcar el estado apropiado
            if (tutoria.reporte_integral_guardado) {
              alumno.estado = 'guardado'
            } else if (reporteResponse.data.seguimiento_1 || reporteResponse.data.seguimiento_2) {
              // Si tiene seguimientos parciales, mantener como "pendiente" pero con datos cargados
              alumno.estado = 'pendiente'
            }

            console.log(`✅ Datos cargados para ${alumno.nombre}:`, alumno.datos)
          }
        } catch (err) {
          // Si el endpoint devuelve 404, significa que no hay reporte guardado aún
          if (err.response?.status === 404) {
            console.log(`ℹ️ No hay reporte guardado para ${alumno.nombre}`)
          } else {
            console.error(`❌ Error al cargar reporte de ${alumno.nombre}:`, err)
          }
        }

        return alumno
      }),
    )

    console.log(`✅ Cargados ${alumnos.value.length} alumnos con sus datos`)
  } catch (error) {
    console.error('Error al cargar alumnos:', error)
    errorMessage.value = 'No se pudieron cargar todos los alumnos. Intenta de nuevo.'
  } finally {
    isLoadingMore.value = false
  }
}

// ==================== CRUD OPERATIONS ====================

// VER REPORTE (modo lectura)
const verReporte = (alumno) => {
  alumno.modoVer = true
  successMessage.value = `👁️ Mostrando reporte de ${alumno.nombre} (solo lectura)`
  setTimeout(() => {
    successMessage.value = null
  }, 2000)
}

// CERRAR VISTA
const cerrarVistaReporte = (alumno) => {
  alumno.modoVer = false
}

// EDITAR REPORTE
const editarReporte = async (alumno) => {
  // Validar antes de guardar
  validarTutoriaGrupal(alumno)
  validarTutoriaIndividual(alumno)
  validarMateriasAprobadas(alumno)

  if (tieneErrores(alumno)) {
    errorMessage.value = `❌ Corrige los errores en el formulario de ${alumno.nombre} antes de actualizar.`
    return
  }

  alumno.estado = 'guardando'
  errorMessage.value = null

  try {
    const response = await reportesAPI.createIntegral({
      id_tutoria: alumno.id_tutoria,
      ...alumno.datos,
    })

    if (response.status === 201 || response.status === 200) {
      alumno.estado = 'guardado'
      successMessage.value = `✅ Reporte de ${alumno.nombre} actualizado exitosamente.`
      setTimeout(() => {
        successMessage.value = null
      }, 3000)
    }
  } catch (error) {
    console.error('Error al actualizar reporte:', error)
    alumno.estado = 'error'
    errorMessage.value = `❌ Error al actualizar reporte de ${alumno.nombre}. ${error.response?.data?.detail || error.message}`
  }
}

// ELIMINAR REPORTE
const eliminarReporte = async (alumno) => {
  if (
    !confirm(
      `⚠️ ¿Estás seguro de eliminar el reporte de ${alumno.nombre}?\n\nEsta acción no se puede deshacer.`,
    )
  ) {
    return
  }

  try {
    const response = await reportesAPI.deleteIntegral(alumno.reporte_id)

    if (response.status === 200 || response.status === 204) {
      // Reset alumno a estado pendiente
      alumno.estado = 'pendiente'
      alumno.reporte_id = null
      alumno.datos = {
        tutoria_grupal: 0,
        tutoria_individual: 0,
        seguimiento_1: '',
        seguimiento_2: '',
        seguimiento_3: '',
        jefatura_academica: 0,
        ciencias_basicas: 0,
        psicologia: 0,
        materias_aprobadas: 0,
        materias_no_aprobadas: '',
      }
      successMessage.value = `🗑️ Reporte de ${alumno.nombre} eliminado exitosamente.`
      setTimeout(() => {
        successMessage.value = null
      }, 3000)
    }
  } catch (error) {
    console.error('Error al eliminar reporte:', error)
    errorMessage.value = `❌ Error al eliminar reporte de ${alumno.nombre}. ${error.response?.data?.detail || error.message}`
  }
}

// GUARDAR ALUMNO (crear reporte)
const guardarAlumno = async (alumno) => {
  // Validar etapa
  if (reporteIntegralEtapa.value === 0) {
    errorMessage.value = `❌ No puedes guardar reportes. La etapa 1 no ha sido habilitada por el administrador.`
    return
  }

  // Validar antes de guardar
  validarTutoriaGrupal(alumno)
  validarTutoriaIndividual(alumno)
  validarMateriasAprobadas(alumno)

  if (tieneErrores(alumno)) {
    errorMessage.value = `❌ Corrige los errores en el formulario de ${alumno.nombre} antes de guardar.`
    return
  }

  alumno.estado = 'guardando'
  errorMessage.value = null

  try {
    const response = await reportesAPI.createIntegral({
      id_tutoria: alumno.id_tutoria,
      ...alumno.datos,
    })

    if (response.status === 201 || response.status === 200) {
      alumno.estado = 'guardado'
      alumno.reporte_id = response.data.id || alumno.id_tutoria
      successMessage.value = `✅ Reporte de ${alumno.nombre} guardado exitosamente.`
      setTimeout(() => {
        successMessage.value = null
      }, 3000)
    }
  } catch (error) {
    console.error('Error al guardar reporte:', error)
    alumno.estado = 'error'
    errorMessage.value = `❌ Error al guardar reporte de ${alumno.nombre}. ${error.response?.data?.detail || error.message}`
  }
}

// GUARDAR TODO
const guardarTodo = async () => {
  // Validar todos los alumnos primero
  let hayErrores = false
  alumnos.value.forEach((alumno) => {
    if (alumno.estado !== 'guardado') {
      validarTutoriaGrupal(alumno)
      validarTutoriaIndividual(alumno)
      validarMateriasAprobadas(alumno)
      if (tieneErrores(alumno)) {
        hayErrores = true
      }
    }
  })

  if (hayErrores) {
    errorMessage.value =
      '❌ Hay errores de validación en algunos formularios. Corrígelos antes de guardar todo.'
    return
  }

  isSaving.value = true
  errorMessage.value = null
  let errores = 0
  let exitosos = 0

  for (const alumno of alumnos.value) {
    if (alumno.estado !== 'guardado') {
      try {
        await guardarAlumno(alumno)
        exitosos++
        // eslint-disable-next-line
      } catch (error) {
        errores++
      }
    }
  }

  isSaving.value = false

  if (errores === 0) {
    successMessage.value = `🎉 ¡Todos los reportes guardados exitosamente! (${exitosos} reportes)`
    setTimeout(() => {
      emit('success')
    }, 2000)
  } else {
    errorMessage.value = `⚠️ Se guardaron ${exitosos} reportes, pero ${errores} tuvieron errores.`
  }
}

const closeModal = () => {
  emit('close')
}

// ==================== LIFECYCLE ====================
onMounted(async () => {
  await fetchConfiguracion() // Cargar configuración primero
  await cargarTodosLosAlumnos()
})
</script>

<style scoped>
/* Scrollbar personalizado con colores coral */
.overflow-auto::-webkit-scrollbar {
  width: 14px;
  height: 14px;
}

.overflow-auto::-webkit-scrollbar-track {
  background: linear-gradient(to right, #f3f4f6, #e5e7eb);
  border-radius: 10px;
}

.overflow-auto::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #ff6b5b, #ff5242);
  border-radius: 10px;
  border: 2px solid #f3f4f6;
}

.overflow-auto::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #ff5242, #ff3d2a);
}

/* Animaciones suaves */
input:focus {
  transform: scale(1.02);
}
</style>
