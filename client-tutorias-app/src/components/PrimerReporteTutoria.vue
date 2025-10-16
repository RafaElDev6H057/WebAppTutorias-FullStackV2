<template>
  <div class="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
    <h2 class="text-2xl font-bold mb-6 text-center text-gray-800">Primer Reporte de Tutoría</h2>

    <form @submit.prevent="guardarReporteGeneral1" class="space-y-8">
      <!-- Sección: Información del Tutor -->
      <div class="bg-indigo-50 p-5 rounded-lg">
        <h3 class="text-lg font-semibold mb-4 text-indigo-800 border-b border-indigo-200 pb-2">
          Información del Tutor
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Selecciona tu nombre según corresponda:
            </label>
            <select
              v-model="formData.nombre_tutor"
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 bg-white p-2"
              required
            >
              <option value="" disabled selected>Selecciona un tutor</option>
              <option v-for="tutor in tutores" :key="tutor.id" :value="tutor.nombre">
                {{ tutor.nombre }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"> Carrera: </label>
            <select
              v-model="formData.carrera"
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 bg-white p-2"
              required
            >
              <option value="" disabled selected>Selecciona una carrera</option>
              <option v-for="carrera in carreras" :key="carrera" :value="carrera">
                {{ carrera }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"> Semestre y grupo: </label>
            <div class="flex space-x-2">
              <select
                v-model="formData.semestre"
                class="w-1/2 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 bg-white p-2"
                required
              >
                <option value="" disabled selected>Semestre</option>
                <option value="1">1er Semestre</option>
                <option value="2">2do Semestre</option>
                <option value="3">3er Semestre</option>
                <option value="4">4to Semestre</option>
                <!-- <option value="5">5to Semestre</option>
                <option value="6">6to Semestre</option>
                <option value="7">7mo Semestre</option>
                <option value="8">8vo Semestre</option>
                <option value="9">9no Semestre</option> -->
                <!-- <option value="otro">Otro</option> -->
              </select>

              <select
                v-model="formData.grupo"
                class="w-1/2 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 bg-white p-2"
                required
              >
                <option value="" disabled selected>Grupo</option>
                <option value="A">A</option>
                <option value="B">B</option>
                <option value="C">C</option>
                <!-- <option value="otro">Otro</option> -->
              </select>
            </div>

            <!-- <div v-if="formData.semestre === 'otro' || formData.grupo === 'otro'" class="mt-2">
              <input
                v-model="formData.semestreGrupoOtro"
                type="text"
                placeholder="Especifica el semestre y grupo"
                class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 bg-white p-2"
              />
            </div> -->
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"> Periodo: </label>
            <select
              v-model="formData.periodo"
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 bg-white p-2"
              required
            >
              <option value="" disabled selected>Selecciona un periodo</option>
              <option v-for="periodo in periodos" :key="periodo" :value="periodo">
                {{ periodo }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- Sección: Información del Grupo -->
      <div class="bg-blue-50 p-5 rounded-lg">
        <h3 class="text-lg font-semibold mb-4 text-blue-800 border-b border-blue-200 pb-2">
          Información del Grupo
        </h3>

        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Total de alumnos/as en el grupo de tutorías:
            </label>
            <input
              v-model="formData.total_alumnos"
              type="number"
              min="0"
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 bg-white p-2"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              ¿Hay alumnos en deserción (baja definitiva)?
            </label>
            <div class="flex space-x-4">
              <label class="inline-flex items-center">
                <input
                  v-model="formData.hay_desercion"
                  type="radio"
                  :value="true"
                  class="form-radio h-4 w-4 text-blue-600"
                  required
                />
                <span class="ml-2">Sí</span>
              </label>
              <label class="inline-flex items-center">
                <input
                  v-model="formData.hay_desercion"
                  type="radio"
                  :value="false"
                  class="form-radio h-4 w-4 text-blue-600"
                  required
                />
                <span class="ml-2">No</span>
              </label>
            </div>
          </div>

          <div v-if="formData.hay_desercion" class="space-y-4">
            <div class="hidden">
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Cantidad de alumnos en deserción:
              </label>
              <input
                v-model="formData.cantidad_desercion"
                type="number"
                min="0"
                class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 bg-white p-2"
                required
              />
              <p v-if="validacionDesercion" class="mt-1 text-sm text-red-600">
                {{ validacionDesercion }}
              </p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Buscar y agregar alumnos en deserción:
              </label>
              <div class="relative">
                <input
                  v-model="busquedaAlumno"
                  type="text"
                  placeholder="Escribe el nombre del alumno..."
                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 bg-white p-2 pr-10"
                  @input="triggerBuscarAlumnos()"
                />
                <button
                  type="button"
                  class="absolute inset-y-0 right-0 px-3 flex items-center bg-blue-500 text-white rounded-r-md hover:bg-blue-600 transition-colors"
                  @click="limpiarBusqueda"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </button>

                <!-- Resultados de búsqueda -->
                <div
                  v-if="resultadosBusqueda.length > 0"
                  class="absolute z-10 mt-1 w-full bg-white shadow-lg max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm"
                >
                  <div
                    v-for="alumno in resultadosBusqueda"
                    :key="alumno.id"
                    class="cursor-pointer select-none relative py-2 pl-3 pr-9 hover:bg-blue-100"
                    @click="agregarAlumnoDesercion(alumno)"
                  >
                    <div class="flex items-center">
                      <span class="font-medium block truncate">
                        {{ alumno.nombre }} {{ alumno.apellido_p }} {{ alumno.apellido_m }}
                      </span>
                      <span class="text-gray-500 ml-2 text-xs"> #{{ alumno.num_control }} </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Lista de alumnos agregados -->
              <div v-if="alumnosDesercionLista.length > 0" class="mt-3">
                <h4 class="text-sm font-medium text-gray-700 mb-2">Alumnos en deserción:</h4>
                <ul class="bg-white rounded-md border border-gray-200 divide-y divide-gray-200">
                  <li
                    v-for="(alumno, index) in alumnosDesercionLista"
                    :key="alumno.id"
                    class="px-4 py-3 flex justify-between items-center hover:bg-gray-50"
                  >
                    <div>
                      <span class="font-medium"
                        >{{ alumno.nombre }} {{ alumno.apellido_p }} {{ alumno.apellido_m }}</span
                      >
                      <span class="text-gray-500 ml-2 text-sm">#{{ alumno.num_control }}</span>
                    </div>
                    <button
                      type="button"
                      class="text-red-500 hover:text-red-700"
                      @click="eliminarAlumnoDesercion(index)"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-5 w-5"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                      >
                        <path
                          fill-rule="evenodd"
                          d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                          clip-rule="evenodd"
                        />
                      </svg>
                    </button>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sección: Canalizaciones y Necesidades Especiales -->
      <div class="bg-green-50 p-5 rounded-lg">
        <h3 class="text-lg font-semibold mb-4 text-green-800 border-b border-green-200 pb-2">
          Canalizaciones y Necesidades Especiales
        </h3>

        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              ¿Tienes canalizaciones a Psicología?
            </label>
            <div class="flex space-x-4">
              <label class="inline-flex items-center">
                <input
                  v-model="formData.canalizacion_psicologia"
                  type="radio"
                  :value="true"
                  class="form-radio h-4 w-4 text-blue-600"
                  required
                />
                <span class="ml-2">Sí</span>
              </label>
              <label class="inline-flex items-center">
                <input
                  v-model="formData.canalizacion_psicologia"
                  type="radio"
                  :value="false"
                  class="form-radio h-4 w-4 text-blue-600"
                  required
                />
                <span class="ml-2">No</span>
              </label>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              ¿Atiendes tutorados con discapacidad?
            </label>
            <div class="flex space-x-4">
              <label class="inline-flex items-center">
                <input
                  v-model="formData.atiende_discapacidad"
                  type="radio"
                  :value="true"
                  class="form-radio h-4 w-4 text-blue-600"
                  required
                />
                <span class="ml-2">Sí</span>
              </label>
              <label class="inline-flex items-center">
                <input
                  v-model="formData.atiende_discapacidad"
                  type="radio"
                  :value="false"
                  class="form-radio h-4 w-4 text-blue-600"
                  required
                />
                <span class="ml-2">No</span>
              </label>
            </div>
          </div>

          <div v-if="formData.atiende_discapacidad">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Buscar y agregar alumnos con discapacidad:
            </label>
            <div class="relative">
              <input
                v-model="busquedaAlumnoDiscapacidad"
                type="text"
                placeholder="Escribe el nombre del alumno..."
                class="w-full rounded-md border-gray-300 shadow-sm focus:border-green-300 focus:ring focus:ring-green-200 focus:ring-opacity-50 bg-white p-2 pr-10"
                @input="triggerBuscarAlumnosDiscapacidad()"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 px-3 flex items-center bg-green-500 text-white rounded-r-md hover:bg-green-600 transition-colors"
                @click="limpiarBusquedaDiscapacidad"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>

              <!-- Resultados de búsqueda -->
              <div
                v-if="resultadosDiscapacidad.length > 0"
                class="absolute z-10 mt-1 w-full bg-white shadow-lg max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm"
              >
                <div
                  v-for="alumno in resultadosDiscapacidad"
                  :key="alumno.id"
                  class="cursor-pointer select-none relative py-2 pl-3 pr-9 hover:bg-green-100"
                  @click="agregarAlumnoDiscapacidad(alumno)"
                >
                  <div class="flex items-center">
                    <span class="font-medium block truncate">
                      {{ alumno.nombre }} {{ alumno.apellido_p }} {{ alumno.apellido_m }}
                    </span>
                    <span class="text-gray-500 ml-2 text-xs"> #{{ alumno.num_control }} </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Lista de alumnos con discapacidad -->
            <div v-if="alumnosDiscapacidadLista.length > 0" class="mt-3">
              <h4 class="text-sm font-medium text-gray-700 mb-2">Alumnos con discapacidad:</h4>
              <ul class="bg-white rounded-md border border-gray-200 divide-y divide-gray-200">
                <li
                  v-for="(alumno, index) in alumnosDiscapacidadLista"
                  :key="alumno.id"
                  class="px-4 py-3 flex justify-between items-center hover:bg-gray-50"
                >
                  <div>
                    <span class="font-medium"
                      >{{ alumno.nombre }} {{ alumno.apellido_p }} {{ alumno.apellido_m }}</span
                    >
                    <span class="text-gray-500 ml-2 text-sm">#{{ alumno.num_control }}</span>
                  </div>
                  <button
                    type="button"
                    class="text-red-500 hover:text-red-700"
                    @click="eliminarAlumnoDiscapacidad(index)"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-5 w-5"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Sección: Rendimiento Académico -->
      <div class="bg-purple-50 p-5 rounded-lg">
        <h3 class="text-lg font-semibold mb-4 text-purple-800 border-b border-purple-200 pb-2">
          Rendimiento Académico
        </h3>

        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              ¿Tienes alumnos o alumnas con materias reprobadas?
            </label>
            <div class="flex space-x-4">
              <label class="inline-flex items-center">
                <input
                  v-model="formData.alumnos_reprobados"
                  type="radio"
                  :value="true"
                  class="form-radio h-4 w-4 text-blue-600"
                  required
                />
                <span class="ml-2">Sí</span>
              </label>
              <label class="inline-flex items-center">
                <input
                  v-model="formData.alumnos_reprobados"
                  type="radio"
                  :value="false"
                  class="form-radio h-4 w-4 text-blue-600"
                  required
                />
                <span class="ml-2">No</span>
              </label>
            </div>
          </div>

          <div v-if="formData.alumnos_reprobados">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Buscar y agregar alumnos con materias reprobadas:
            </label>
            <div class="relative">
              <input
                v-model="busquedaAlumnoReprobado"
                type="text"
                placeholder="Escribe el nombre del alumno..."
                class="w-full rounded-md border-gray-300 shadow-sm focus:border-purple-300 focus:ring focus:ring-purple-200 focus:ring-opacity-50 bg-white p-2 pr-10"
                @input="triggerBuscarAlumnosReprobados()"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 px-3 flex items-center bg-purple-500 text-white rounded-r-md hover:bg-purple-600 transition-colors"
                @click="limpiarBusquedaReprobados"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>

              <!-- Resultados de búsqueda -->
              <div
                v-if="resultadosReprobados.length > 0"
                class="absolute z-10 mt-1 w-full bg-white shadow-lg max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm"
              >
                <div
                  v-for="alumno in resultadosReprobados"
                  :key="alumno.id"
                  class="cursor-pointer select-none relative py-2 pl-3 pr-9 hover:bg-purple-100"
                  @click="agregarAlumnoReprobado(alumno)"
                >
                  <div class="flex items-center">
                    <span class="font-medium block truncate">
                      {{ alumno.nombre }} {{ alumno.apellido_p }} {{ alumno.apellido_m }}
                    </span>
                    <span class="text-gray-500 ml-2 text-xs"> #{{ alumno.num_control }} </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Lista de alumnos con materias reprobadas -->
            <div v-if="alumnosReprobadosLista.length > 0" class="mt-3">
              <h4 class="text-sm font-medium text-gray-700 mb-2">
                Alumnos con materias reprobadas:
              </h4>
              <ul class="bg-white rounded-md border border-gray-200 divide-y divide-gray-200">
                <li
                  v-for="(alumno, index) in alumnosReprobadosLista"
                  :key="alumno.id"
                  class="px-4 py-3 flex justify-between items-center hover:bg-gray-50"
                >
                  <div>
                    <span class="font-medium"
                      >{{ alumno.nombre }} {{ alumno.apellido_p }} {{ alumno.apellido_m }}</span
                    >
                    <span class="text-gray-500 ml-2 text-sm">#{{ alumno.num_control }}</span>
                  </div>
                  <button
                    type="button"
                    class="text-red-500 hover:text-red-700"
                    @click="eliminarAlumnoReprobado(index)"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-5 w-5"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </button>
                </li>
              </ul>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Buscar y agregar alumnos que requieren asesoría académica:
            </label>
            <div class="relative">
              <input
                v-model="busquedaAlumnoAsesoria"
                type="text"
                placeholder="Escribe el nombre del alumno..."
                class="w-full rounded-md border-gray-300 shadow-sm focus:border-purple-300 focus:ring focus:ring-purple-200 focus:ring-opacity-50 bg-white p-2 pr-10"
                @input="triggerBuscarAlumnosAsesoria()"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 px-3 flex items-center bg-purple-500 text-white rounded-r-md hover:bg-purple-600 transition-colors"
                @click="limpiarBusquedaAsesoria"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>

              <!-- Resultados de búsqueda -->
              <div
                v-if="resultadosAsesoria.length > 0"
                class="absolute z-10 mt-1 w-full bg-white shadow-lg max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm"
              >
                <div
                  v-for="alumno in resultadosAsesoria"
                  :key="alumno.id"
                  class="cursor-pointer select-none relative py-2 pl-3 pr-9 hover:bg-purple-100"
                  @click="seleccionarAlumnoAsesoria(alumno)"
                >
                  <div class="flex items-center">
                    <span class="font-medium block truncate">
                      {{ alumno.nombre }} {{ alumno.apellido_p }} {{ alumno.apellido_m }}
                    </span>
                    <span class="text-gray-500 ml-2 text-xs"> #{{ alumno.num_control }} </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Formulario para agregar asignatura a reforzar -->
            <div
              v-if="alumnoAsesoriaSeleccionado"
              class="mt-3 p-3 bg-white rounded-md border border-purple-200"
            >
              <div class="flex flex-col space-y-3">
                <div>
                  <span class="font-medium">Alumno seleccionado: </span>
                  <span
                    >{{ alumnoAsesoriaSeleccionado.nombre }}
                    {{ alumnoAsesoriaSeleccionado.apellido_p }}
                    {{ alumnoAsesoriaSeleccionado.apellido_m }}</span
                  >
                  <span class="text-gray-500 ml-2 text-sm"
                    >#{{ alumnoAsesoriaSeleccionado.num_control }}</span
                  >
                </div>
                <div class="flex space-x-2">
                  <input
                    v-model="asignaturaAReforzar"
                    type="text"
                    placeholder="Asignatura a reforzar (ej: Cálculo Diferencial)"
                    class="flex-1 rounded-md border-gray-300 shadow-sm focus:border-purple-300 focus:ring focus:ring-purple-200 focus:ring-opacity-50 bg-white p-2"
                  />
                  <button
                    type="button"
                    class="px-4 py-2 bg-purple-500 text-white rounded-md hover:bg-purple-600 transition-colors"
                    @click="agregarAlumnoAsesoria"
                    :disabled="!asignaturaAReforzar"
                  >
                    Agregar
                  </button>
                  <button
                    type="button"
                    class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 transition-colors"
                    @click="cancelarSeleccionAsesoria"
                  >
                    Cancelar
                  </button>
                </div>
              </div>
            </div>

            <!-- Lista de alumnos que requieren asesoría -->
            <div v-if="alumnosAsesoriaLista.length > 0" class="mt-3">
              <h4 class="text-sm font-medium text-gray-700 mb-2">
                Alumnos que requieren asesoría académica:
              </h4>
              <ul class="bg-white rounded-md border border-gray-200 divide-y divide-gray-200">
                <li
                  v-for="(item, index) in alumnosAsesoriaLista"
                  :key="index"
                  class="px-4 py-3 flex justify-between items-center hover:bg-gray-50"
                >
                  <div>
                    <span class="font-medium"
                      >{{ item.alumno.nombre }} {{ item.alumno.apellido_p }}
                      {{ item.alumno.apellido_m }}</span
                    >
                    <span class="text-gray-500 ml-2 text-sm">#{{ item.alumno.num_control }}</span>
                    <span class="block text-purple-600 text-sm mt-1"
                      >Asignatura: {{ item.asignatura }}</span
                    >
                  </div>
                  <button
                    type="button"
                    class="text-red-500 hover:text-red-700"
                    @click="eliminarAlumnoAsesoria(index)"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-5 w-5"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Sección: Proyecto Institucional -->
      <div class="bg-amber-50 p-5 rounded-lg">
        <h3 class="text-lg font-semibold mb-4 text-amber-800 border-b border-amber-200 pb-2">
          Proyecto del Programa Institucional de Tutoría
        </h3>

        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Porcentaje de avance del proyecto:
            </label>
            <div class="flex items-center space-x-4">
              <input
                v-model="formData.porcentaje_proyecto"
                type="range"
                min="10"
                max="100"
                step="10"
                class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
              <span class="text-sm font-medium">{{ formData.porcentaje_proyecto }}%</span>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Objetivo del proyecto:
            </label>
            <textarea
              v-model="formData.objetivo_proyecto"
              rows="3"
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-amber-300 focus:ring focus:ring-amber-200 focus:ring-opacity-50 bg-white p-2"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Descripción del proyecto:
            </label>
            <textarea
              v-model="formData.descripcion_proyecto"
              rows="4"
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-amber-300 focus:ring focus:ring-amber-200 focus:ring-opacity-50 bg-white p-2"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Metas del proyecto:
            </label>
            <textarea
              v-model="formData.metas_proyecto"
              rows="3"
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-amber-300 focus:ring focus:ring-amber-200 focus:ring-opacity-50 bg-white p-2"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Actividades realizadas hasta este primer corte:
            </label>
            <textarea
              v-model="formData.actividades_realizadas"
              rows="4"
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-amber-300 focus:ring focus:ring-amber-200 focus:ring-opacity-50 bg-white p-2"
            ></textarea>
          </div>

          <!-- <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Adjunta las evidencias de este primer avance de proyecto:
            </label>
            <div class="flex items-center justify-center w-full">
              <label
                class="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100"
              >
                <div class="flex flex-col items-center justify-center pt-5 pb-6">
                  <svg
                    class="w-8 h-8 mb-4 text-gray-500"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 20 16"
                  >
                    <path
                      stroke="currentColor"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
                    />
                  </svg>
                  <p class="mb-2 text-sm text-gray-500">
                    <span class="font-semibold">Haz clic para subir</span> o arrastra y suelta
                  </p>
                  <p class="text-xs text-gray-500">PDF, DOC, DOCX, JPG, PNG (MAX. 10MB)</p>
                </div>
                <input type="file" class="hidden" @change="handleFileUpload" />
              </label>
            </div>
            <div v-if="formData.evidencia" class="mt-2 text-sm text-gray-600">
              Archivo seleccionado: {{ formData.evidencia.name }}
            </div>
          </div> -->
        </div>
      </div>

      <!-- Sección: Conclusiones -->
      <div class="bg-red-50 p-5 rounded-lg">
        <h3 class="text-lg font-semibold mb-4 text-red-800 border-b border-red-200 pb-2">
          Conclusiones y Observaciones
        </h3>

        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"> Conclusión: </label>
            <textarea
              v-model="formData.conclusion"
              rows="4"
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-red-300 focus:ring focus:ring-red-200 focus:ring-opacity-50 bg-white p-2"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"> Observaciones: </label>
            <textarea
              v-model="formData.observaciones"
              rows="4"
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-red-300 focus:ring focus:ring-red-200 focus:ring-opacity-50 bg-white p-2"
            ></textarea>
          </div>
        </div>
      </div>

      <!-- Botones de acción -->
      <div class="flex justify-end space-x-4 pt-6 border-t">
        <button
          type="button"
          @click="emit('cerrar')"
          class="px-6 py-3 text-base font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
        >
          Cancelar
        </button>
        <button
          type="submit"
          class="px-6 py-3 text-base font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
        >
          Guardar Reporte
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref, computed, watch, onUnmounted } from 'vue'
import axios from 'axios'
import AlumnoService from '@/services/AlumnoService.js'

const emit = defineEmits(['cerrar', 'guardar'])

// Lista de carreras
const carreras = [
  'Ingeniería en Gestión Empresarial',
  'Ingeniería Industrial',
  'Ingeniería en Minería',
  'Ingeniería en Logística',
  'Ingeniería en Sistemas Computacionales',
  'Ingeniería Electrónica',
  'Ingeniería Ambiental',
  'Arquitectura',
  'Ingeniería en Informática',
  'Ingeniería en Semiconductores',
]

// Lista de tutores (simulada - en producción se obtendría de una API)
const tutores = [
  { id: 1, nombre: 'Juan Pérez González' },
  { id: 2, nombre: 'María Rodríguez López' },
  { id: 3, nombre: 'Carlos Sánchez Martínez' },
  { id: 4, nombre: 'Ana García Fernández' },
  { id: 5, nombre: 'Roberto Hernández Torres' },
]

// Lista de alumnos (simulada - en producción se obtendría de una API)

// Generar periodos automáticamente
const generarPeriodos = () => {
  const periodos = []
  const currentYear = new Date().getFullYear()

  // Generar periodos para los próximos 3 años
  for (let year = currentYear; year <= currentYear + 3; year++) {
    periodos.push(`ENERO-JUNIO ${year}`)
    periodos.push(`AGOSTO-DICIEMBRE ${year}`)
  }

  return periodos
}

const periodos = generarPeriodos()

// Variables para la búsqueda de alumnos en deserción
const busquedaAlumno = ref('')
const resultadosBusqueda = ref([])
const alumnosDesercionLista = ref([])
let buscarTimeout = null

// Variables para la búsqueda de alumnos con discapacidad
const busquedaAlumnoDiscapacidad = ref('')
const resultadosDiscapacidad = ref([])
const alumnosDiscapacidadLista = ref([])
let buscarDiscapacidadTimeout = null

// Variables para la búsqueda de alumnos con materias reprobadas
const busquedaAlumnoReprobado = ref('')
const resultadosReprobados = ref([])
const alumnosReprobadosLista = ref([])
let buscarReprobadosTimeout = null

// Variables para la búsqueda de alumnos que requieren asesoría
const busquedaAlumnoAsesoria = ref('')
const resultadosAsesoria = ref([])
const alumnosAsesoriaLista = ref([])
const alumnoAsesoriaSeleccionado = ref(null)
const asignaturaAReforzar = ref('')
let buscarAsesoriaTimeout = null

// const students = ref([])

// Validación para la cantidad de alumnos en deserción
const validacionDesercion = computed(() => {
  if (formData.cantidad_desercion && alumnosDesercionLista.value.length > 0) {
    if (parseInt(formData.cantidad_desercion) !== alumnosDesercionLista.value.length) {
      return `La cantidad de alumnos (${formData.cantidad_desercion}) no coincide con la lista (${alumnosDesercionLista.value.length})`
    }
  }
  return ''
})

const formData = reactive({
  // Nuevos campos
  nombre_tutor: '',
  carrera: '',
  semestre: '',
  grupo: '',
  // semestreGrupoOtro: '',
  periodo: '',

  // Campos modificados para deserción
  total_alumnos: null,
  hay_desercion: '',
  cantidad_desercion: 0,

  // Otros campos
  canalizacion_psicologia: '',
  atiende_discapacidad: '',
  alumnos_reprobados: '',
  porcentaje_proyecto: 10,
  objetivo_proyecto: '',
  descripcion_proyecto: '',
  metas_proyecto: '',
  actividades_realizadas: '',
  conclusion: '',
  observaciones: '',
})

// Funciones para alumnos en deserción
const buscarAlumnos = async () => {
  if (busquedaAlumno.value.length < 2) {
    resultadosBusqueda.value = []
    return
  }

  try {
    // 1. Obtenemos los resultados DIRECTAMENTE del backend, que ya vienen filtrados.
    const response = await AlumnoService.getAlumnos(1, 100, busquedaAlumno.value)
    const alumnosEncontrados = response.data.alumnos

    // 2. Ahora, filtramos esa lista ÚNICAMENTE para quitar los que ya están en la lista de deserción.
    // Esta es la única comprobación que el frontend necesita hacer.
    resultadosBusqueda.value = alumnosEncontrados.filter((alumno) => {
      return !alumnosDesercionLista.value.some((a) => a.id_alumno === alumno.id_alumno)
      // Nota: Asegúrate de usar el mismo campo de ID en ambos lados (ej: id_alumno o id).
    })
  } catch (err) {
    console.log(err)
    resultadosBusqueda.value = [] // Limpiamos en caso de error
  }
}

const triggerBuscarAlumnos = (ms = 350) => {
  if (buscarTimeout) clearTimeout(buscarTimeout)
  buscarTimeout = setTimeout(() => {
    buscarAlumnos()
  }, ms)
}

onUnmounted(() => {
  if (buscarTimeout) clearTimeout(buscarTimeout)
})

const agregarAlumnoDesercion = (alumno) => {
  alumnosDesercionLista.value.push(alumno)
  busquedaAlumno.value = ''
  resultadosBusqueda.value = []

  // Actualizar automáticamente el número de alumnos en deserción
  formData.cantidad_desercion = alumnosDesercionLista.value.length
}

const eliminarAlumnoDesercion = (index) => {
  alumnosDesercionLista.value.splice(index, 1)

  // Actualizar automáticamente el número de alumnos en deserción
  formData.cantidad_desercion = alumnosDesercionLista.value.length
}

const limpiarBusqueda = () => {
  busquedaAlumno.value = ''
  resultadosBusqueda.value = []
}

// Funciones para alumnos con discapacidad
const buscarAlumnosDiscapacidad = async () => {
  // No busca si el texto es muy corto
  if (busquedaAlumnoDiscapacidad.value.length < 2) {
    resultadosDiscapacidad.value = []
    return
  }

  try {
    // 1. Llamamos al servicio para que el backend haga la búsqueda
    const response = await AlumnoService.getAlumnos(1, 100, busquedaAlumnoDiscapacidad.value)
    const alumnosEncontrados = response.data.alumnos

    // 2. Filtramos en el frontend SOLO para quitar los que ya agregamos
    resultadosDiscapacidad.value = alumnosEncontrados.filter((alumno) => {
      // Usamos `some` para verificar si el `id_alumno` ya existe en la lista
      return !alumnosDiscapacidadLista.value.some((a) => a.id_alumno === alumno.id_alumno)
    })
  } catch (err) {
    console.error('Error buscando alumnos para discapacidad:', err)
    resultadosDiscapacidad.value = [] // Limpiamos si hay un error
  }
}

const triggerBuscarAlumnosDiscapacidad = (ms = 350) => {
  // Limpia el temporizador anterior si el usuario sigue escribiendo
  if (buscarDiscapacidadTimeout) clearTimeout(buscarDiscapacidadTimeout)

  // Crea un nuevo temporizador
  buscarDiscapacidadTimeout = setTimeout(() => {
    buscarAlumnosDiscapacidad()
  }, ms)
}

onUnmounted(() => {
  if (buscarDiscapacidadTimeout) clearTimeout(buscarDiscapacidadTimeout)
})

const agregarAlumnoDiscapacidad = (alumno) => {
  alumnosDiscapacidadLista.value.push(alumno)
  busquedaAlumnoDiscapacidad.value = ''
  resultadosDiscapacidad.value = []
}

const eliminarAlumnoDiscapacidad = (index) => {
  alumnosDiscapacidadLista.value.splice(index, 1)
}

const limpiarBusquedaDiscapacidad = () => {
  busquedaAlumnoDiscapacidad.value = ''
  resultadosDiscapacidad.value = []
}

// Funciones para alumnos con materias reprobadas
const buscarAlumnosReprobados = async () => {
  if (busquedaAlumnoReprobado.value.length < 2) {
    resultadosReprobados.value = []
    return
  }

  try {
    // 1. La búsqueda principal la hace el backend
    const response = await AlumnoService.getAlumnos(1, 100, busquedaAlumnoReprobado.value)
    const alumnosEncontrados = response.data.alumnos

    // 2. El frontend solo filtra para no mostrar los alumnos ya agregados
    resultadosReprobados.value = alumnosEncontrados.filter((alumno) => {
      return !alumnosReprobadosLista.value.some((a) => a.id_alumno === alumno.id_alumno)
    })
  } catch (err) {
    console.error('Error buscando alumnos reprobados:', err)
    resultadosReprobados.value = []
  }
}

const triggerBuscarAlumnosReprobados = (ms = 350) => {
  // Limpia el temporizador anterior si el usuario sigue escribiendo
  if (buscarReprobadosTimeout) clearTimeout(buscarReprobadosTimeout)

  // Establece un nuevo temporizador para ejecutar la búsqueda
  buscarReprobadosTimeout = setTimeout(() => {
    buscarAlumnosReprobados()
  }, ms)
}

onUnmounted(() => {
  if (buscarReprobadosTimeout) clearTimeout(buscarReprobadosTimeout)
})

const agregarAlumnoReprobado = (alumno) => {
  alumnosReprobadosLista.value.push(alumno)
  busquedaAlumnoReprobado.value = ''
  resultadosReprobados.value = []
}

const eliminarAlumnoReprobado = (index) => {
  alumnosReprobadosLista.value.splice(index, 1)
}

const limpiarBusquedaReprobados = () => {
  busquedaAlumnoReprobado.value = ''
  resultadosReprobados.value = []
}

// Funciones para alumnos que requieren asesoría
const buscarAlumnosAsesoria = async () => {
  if (busquedaAlumnoAsesoria.value.length < 2) {
    resultadosAsesoria.value = []
    return
  }

  try {
    // 1. Llamamos al servicio para que el backend filtre por nombre/control
    const response = await AlumnoService.getAlumnos(1, 100, busquedaAlumnoAsesoria.value)
    const alumnosEncontrados = response.data.alumnos

    // 2. Filtramos en el frontend solo para quitar a los alumnos ya agregados
    resultadosAsesoria.value = alumnosEncontrados.filter((alumno) => {
      // La lógica aquí es un poco diferente porque tu lista guarda objetos { alumno, asignatura }
      return !alumnosAsesoriaLista.value.some((item) => item.alumno.id_alumno === alumno.id_alumno)
    })
  } catch (err) {
    console.error('Error buscando alumnos para asesoría:', err)
    resultadosAsesoria.value = []
  }
}

const triggerBuscarAlumnosAsesoria = (ms = 350) => {
  if (buscarAsesoriaTimeout) clearTimeout(buscarAsesoriaTimeout)

  buscarAsesoriaTimeout = setTimeout(() => {
    buscarAlumnosAsesoria()
  }, ms)
}

onUnmounted(() => {
  if (buscarAsesoriaTimeout) clearTimeout(buscarAsesoriaTimeout)
})

const seleccionarAlumnoAsesoria = (alumno) => {
  alumnoAsesoriaSeleccionado.value = alumno
  busquedaAlumnoAsesoria.value = ''
  resultadosAsesoria.value = []
}

const agregarAlumnoAsesoria = () => {
  if (alumnoAsesoriaSeleccionado.value && asignaturaAReforzar.value) {
    alumnosAsesoriaLista.value.push({
      alumno: alumnoAsesoriaSeleccionado.value,
      asignatura: asignaturaAReforzar.value,
    })

    // Limpiar selección
    alumnoAsesoriaSeleccionado.value = null
    asignaturaAReforzar.value = ''
  }
}

const eliminarAlumnoAsesoria = (index) => {
  alumnosAsesoriaLista.value.splice(index, 1)
}

const cancelarSeleccionAsesoria = () => {
  alumnoAsesoriaSeleccionado.value = null
  asignaturaAReforzar.value = ''
}

const limpiarBusquedaAsesoria = () => {
  busquedaAlumnoAsesoria.value = ''
  resultadosAsesoria.value = []
}

// Observar cambios en hayAlumnosDesercion para resetear valores cuando cambia a "No"
watch(
  () => formData.hay_desercion,
  (newValue) => {
    if (newValue === false) {
      formData.cantidad_desercion = null
      alumnosDesercionLista.value = []
    }
  },
)

// Observar cambios en alumnosDiscapacidad para resetear valores cuando cambia a "No"
watch(
  () => formData.atiende_discapacidad,
  (newValue) => {
    if (newValue === false) {
      alumnosDiscapacidadLista.value = []
    }
  },
)

// Observar cambios en alumnosReprobados para resetear valores cuando cambia a "No"
watch(
  () => formData.alumnos_reprobados,
  (newValue) => {
    if (newValue === false) {
      alumnosReprobadosLista.value = []
    }
  },
)

const guardarReporteGeneral1 = async () => {
  try {
    const datosEnviar = {
      ...formData,
      alumnos_desercion: JSON.stringify(alumnosDesercionLista.value),
      alumnos_discapacidad: JSON.stringify(alumnosDiscapacidadLista.value),
      alumnos_materias_reprobadas: JSON.stringify(alumnosReprobadosLista.value),
      alumnos_asesoria: JSON.stringify(alumnosAsesoriaLista.value),
    }
    // 3. Realiza la petición POST a tu endpoint de FastAPI
    const response = await axios.post('http://localhost:8000/api/reportes/general-1', datosEnviar)

    // 4. Maneja la respuesta exitosa
    if (response.status === 201) {
      console.log('Reporte guardado exitosamente:', response.data)
      // Aquí puedes mostrar una notificación de éxito al usuario
      alert('¡Reporte guardado con éxito!')
      // Opcional: limpiar el formulario o redirigir al usuario
    }
  } catch (error) {
    // 5. Maneja cualquier error que ocurra
    console.error('Error al guardar el reporte:', error)
    // Muestra una notificación de error al usuario
    alert('Ocurrió un error al guardar el reporte. Inténtalo de nuevo.')
  }
}

// const fetchStudents = async (page) => {
//   try {
//     const response = await AlumnoService.getAlumnos(page, 100, busquedaAlumno.value)
//     students.value = response.data.alumnos
//     // hayMasAlumnos.value = response.data.alumnos.length === 5
//     // totalStudents.value = response.data.total_alumnos
//     // totalPages.value = Math.ceil(response.data.total_alumnos / itemsPerPage.value)
//     // error.value = ''
//   } catch (err) {
//     console.error('Error al obtener los estudiantes:', err.response.data.detail[0].type)
//     if (err.response.data.detail[0].type == 'string_too_short') {
//       console.log('Favor de ingresar mínimo 3 carácteres a buscar')
//       // error.value = 'Favor de ingresar mínimo 3 carácteres a buscar'
//     } else {
//       console.log('No se pudo cargar la lista de estudiantes')
//       // error.value = 'No se pudo cargar la lista de estudiantes'
//     }
//     students.value = []
//   } finally {
//     // loading.value = false
//   }
// }
</script>

<style scoped>
/* Estilos adicionales si son necesarios */
input[type='range']::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
}

input[type='range']::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
}
</style>
