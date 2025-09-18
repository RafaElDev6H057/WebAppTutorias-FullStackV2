<template>
  <div class="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
    <h2 class="text-2xl font-bold mb-6 text-center text-gray-800">Primer Reporte de Tutoría</h2>

    <form @submit.prevent="enviarFormulario" class="space-y-8">
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
              v-model="formData.nombreTutor"
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
                <option value="otro">Otro</option>
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
                <option value="otro">Otro</option>
              </select>
            </div>

            <div v-if="formData.semestre === 'otro' || formData.grupo === 'otro'" class="mt-2">
              <input
                v-model="formData.semestreGrupoOtro"
                type="text"
                placeholder="Especifica el semestre y grupo"
                class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 bg-white p-2"
              />
            </div>
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
              v-model="formData.totalAlumnos"
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
                  v-model="formData.hayAlumnosDesercion"
                  type="radio"
                  value="Si"
                  class="form-radio h-4 w-4 text-blue-600"
                  required
                />
                <span class="ml-2">Sí</span>
              </label>
              <label class="inline-flex items-center">
                <input
                  v-model="formData.hayAlumnosDesercion"
                  type="radio"
                  value="No"
                  class="form-radio h-4 w-4 text-blue-600"
                  required
                />
                <span class="ml-2">No</span>
              </label>
            </div>
          </div>

          <div v-if="formData.hayAlumnosDesercion === 'Si'" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Cantidad de alumnos en deserción:
              </label>
              <input
                v-model="formData.alumnosDesercion"
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
                  @input="buscarAlumnos"
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
                        {{ alumno.nombre }} {{ alumno.apellidos }}
                      </span>
                      <span class="text-gray-500 ml-2 text-xs"> #{{ alumno.numControl }} </span>
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
                      <span class="font-medium">{{ alumno.nombre }} {{ alumno.apellidos }}</span>
                      <span class="text-gray-500 ml-2 text-sm">#{{ alumno.numControl }}</span>
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
                  v-model="formData.canalizacionesPsicologia"
                  type="radio"
                  value="Si"
                  class="form-radio h-4 w-4 text-blue-600"
                  required
                />
                <span class="ml-2">Sí</span>
              </label>
              <label class="inline-flex items-center">
                <input
                  v-model="formData.canalizacionesPsicologia"
                  type="radio"
                  value="No"
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
                  v-model="formData.alumnosDiscapacidad"
                  type="radio"
                  value="Si"
                  class="form-radio h-4 w-4 text-blue-600"
                  required
                />
                <span class="ml-2">Sí</span>
              </label>
              <label class="inline-flex items-center">
                <input
                  v-model="formData.alumnosDiscapacidad"
                  type="radio"
                  value="No"
                  class="form-radio h-4 w-4 text-blue-600"
                  required
                />
                <span class="ml-2">No</span>
              </label>
            </div>
          </div>

          <div v-if="formData.alumnosDiscapacidad === 'Si'">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Buscar y agregar alumnos con discapacidad:
            </label>
            <div class="relative">
              <input
                v-model="busquedaAlumnoDiscapacidad"
                type="text"
                placeholder="Escribe el nombre del alumno..."
                class="w-full rounded-md border-gray-300 shadow-sm focus:border-green-300 focus:ring focus:ring-green-200 focus:ring-opacity-50 bg-white p-2 pr-10"
                @input="buscarAlumnosDiscapacidad"
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
                      {{ alumno.nombre }} {{ alumno.apellidos }}
                    </span>
                    <span class="text-gray-500 ml-2 text-xs"> #{{ alumno.numControl }} </span>
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
                    <span class="font-medium">{{ alumno.nombre }} {{ alumno.apellidos }}</span>
                    <span class="text-gray-500 ml-2 text-sm">#{{ alumno.numControl }}</span>
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
                  v-model="formData.alumnosReprobados"
                  type="radio"
                  value="Si"
                  class="form-radio h-4 w-4 text-blue-600"
                  required
                />
                <span class="ml-2">Sí</span>
              </label>
              <label class="inline-flex items-center">
                <input
                  v-model="formData.alumnosReprobados"
                  type="radio"
                  value="No"
                  class="form-radio h-4 w-4 text-blue-600"
                  required
                />
                <span class="ml-2">No</span>
              </label>
            </div>
          </div>

          <div v-if="formData.alumnosReprobados === 'Si'">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Buscar y agregar alumnos con 1 materia reprobada:
            </label>
            <div class="relative">
              <input
                v-model="busquedaAlumnoReprobado"
                type="text"
                placeholder="Escribe el nombre del alumno..."
                class="w-full rounded-md border-gray-300 shadow-sm focus:border-purple-300 focus:ring focus:ring-purple-200 focus:ring-opacity-50 bg-white p-2 pr-10"
                @input="buscarAlumnosReprobados"
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
                      {{ alumno.nombre }} {{ alumno.apellidos }}
                    </span>
                    <span class="text-gray-500 ml-2 text-xs"> #{{ alumno.numControl }} </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Lista de alumnos con materias reprobadas -->
            <div v-if="alumnosReprobadosLista.length > 0" class="mt-3">
              <h4 class="text-sm font-medium text-gray-700 mb-2">
                Alumnos con 1 materia reprobada:
              </h4>
              <ul class="bg-white rounded-md border border-gray-200 divide-y divide-gray-200">
                <li
                  v-for="(alumno, index) in alumnosReprobadosLista"
                  :key="alumno.id"
                  class="px-4 py-3 flex justify-between items-center hover:bg-gray-50"
                >
                  <div>
                    <span class="font-medium">{{ alumno.nombre }} {{ alumno.apellidos }}</span>
                    <span class="text-gray-500 ml-2 text-sm">#{{ alumno.numControl }}</span>
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
                @input="buscarAlumnosAsesoria"
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
                      {{ alumno.nombre }} {{ alumno.apellidos }}
                    </span>
                    <span class="text-gray-500 ml-2 text-xs"> #{{ alumno.numControl }} </span>
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
                    {{ alumnoAsesoriaSeleccionado.apellidos }}</span
                  >
                  <span class="text-gray-500 ml-2 text-sm"
                    >#{{ alumnoAsesoriaSeleccionado.numControl }}</span
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
                      >{{ item.alumno.nombre }} {{ item.alumno.apellidos }}</span
                    >
                    <span class="text-gray-500 ml-2 text-sm">#{{ item.alumno.numControl }}</span>
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
                v-model="formData.porcentajeAvance"
                type="range"
                min="10"
                max="100"
                step="10"
                class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
              <span class="text-sm font-medium">{{ formData.porcentajeAvance }}%</span>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Objetivo del proyecto:
            </label>
            <textarea
              v-model="formData.objetivoProyecto"
              rows="3"
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-amber-300 focus:ring focus:ring-amber-200 focus:ring-opacity-50 bg-white p-2"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Descripción del proyecto:
            </label>
            <textarea
              v-model="formData.descripcionProyecto"
              rows="4"
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-amber-300 focus:ring focus:ring-amber-200 focus:ring-opacity-50 bg-white p-2"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Metas del proyecto:
            </label>
            <textarea
              v-model="formData.metasProyecto"
              rows="3"
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-amber-300 focus:ring focus:ring-amber-200 focus:ring-opacity-50 bg-white p-2"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Actividades realizadas hasta este primer corte:
            </label>
            <textarea
              v-model="formData.actividadesRealizadas"
              rows="4"
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-amber-300 focus:ring focus:ring-amber-200 focus:ring-opacity-50 bg-white p-2"
            ></textarea>
          </div>

          <div>
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
          </div>
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
import { reactive, ref, computed, watch } from 'vue'

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
const todosLosAlumnos = [
  { id: 1, nombre: 'Luis', apellidos: 'Martínez Gómez', numControl: '19041234' },
  { id: 2, nombre: 'Ana', apellidos: 'Sánchez Pérez', numControl: '19041235' },
  { id: 3, nombre: 'Carlos', apellidos: 'Rodríguez López', numControl: '19041236' },
  { id: 4, nombre: 'María', apellidos: 'González Hernández', numControl: '19041237' },
  { id: 5, nombre: 'José', apellidos: 'Pérez Martínez', numControl: '19041238' },
  { id: 6, nombre: 'Laura', apellidos: 'Hernández García', numControl: '19041239' },
  { id: 7, nombre: 'Pedro', apellidos: 'López Sánchez', numControl: '19041240' },
  { id: 8, nombre: 'Sofía', apellidos: 'García Rodríguez', numControl: '19041241' },
  { id: 9, nombre: 'Miguel', apellidos: 'Torres Flores', numControl: '19041242' },
  { id: 10, nombre: 'Fernanda', apellidos: 'Flores Torres', numControl: '19041243' },
]

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

// Variables para la búsqueda de alumnos con discapacidad
const busquedaAlumnoDiscapacidad = ref('')
const resultadosDiscapacidad = ref([])
const alumnosDiscapacidadLista = ref([])

// Variables para la búsqueda de alumnos con materias reprobadas
const busquedaAlumnoReprobado = ref('')
const resultadosReprobados = ref([])
const alumnosReprobadosLista = ref([])

// Variables para la búsqueda de alumnos que requieren asesoría
const busquedaAlumnoAsesoria = ref('')
const resultadosAsesoria = ref([])
const alumnosAsesoriaLista = ref([])
const alumnoAsesoriaSeleccionado = ref(null)
const asignaturaAReforzar = ref('')

// Validación para la cantidad de alumnos en deserción
const validacionDesercion = computed(() => {
  if (formData.alumnosDesercion && alumnosDesercionLista.value.length > 0) {
    if (parseInt(formData.alumnosDesercion) !== alumnosDesercionLista.value.length) {
      return `La cantidad de alumnos (${formData.alumnosDesercion}) no coincide con la lista (${alumnosDesercionLista.value.length})`
    }
  }
  return ''
})

const formData = reactive({
  // Nuevos campos
  nombreTutor: '',
  carrera: '',
  semestre: '',
  grupo: '',
  semestreGrupoOtro: '',
  periodo: '',

  // Campos modificados para deserción
  totalAlumnos: null,
  hayAlumnosDesercion: '',
  alumnosDesercion: null,

  // Otros campos
  canalizacionesPsicologia: '',
  alumnosDiscapacidad: '',
  nombresAlumnosDiscapacidad: '',
  alumnosReprobados: '',
  alumnosUnaReprobada: '',
  alumnosAsesoria: '',
  porcentajeAvance: 10,
  objetivoProyecto: '',
  descripcionProyecto: '',
  metasProyecto: '',
  actividadesRealizadas: '',
  evidencia: null,
  conclusion: '',
  observaciones: '',
})

// Funciones para alumnos en deserción
const buscarAlumnos = () => {
  if (busquedaAlumno.value.length < 2) {
    resultadosBusqueda.value = []
    return
  }

  const termino = busquedaAlumno.value.toLowerCase()
  resultadosBusqueda.value = todosLosAlumnos.filter((alumno) => {
    // Filtrar alumnos que ya están en la lista
    const yaAgregado = alumnosDesercionLista.value.some((a) => a.id === alumno.id)
    if (yaAgregado) return false

    // Buscar por nombre, apellidos o número de control
    return (
      alumno.nombre.toLowerCase().includes(termino) ||
      alumno.apellidos.toLowerCase().includes(termino) ||
      alumno.numControl.includes(termino)
    )
  })
}

const agregarAlumnoDesercion = (alumno) => {
  alumnosDesercionLista.value.push(alumno)
  busquedaAlumno.value = ''
  resultadosBusqueda.value = []

  // Actualizar automáticamente el número de alumnos en deserción
  formData.alumnosDesercion = alumnosDesercionLista.value.length
}

const eliminarAlumnoDesercion = (index) => {
  alumnosDesercionLista.value.splice(index, 1)

  // Actualizar automáticamente el número de alumnos en deserción
  formData.alumnosDesercion = alumnosDesercionLista.value.length
}

const limpiarBusqueda = () => {
  busquedaAlumno.value = ''
  resultadosBusqueda.value = []
}

// Funciones para alumnos con discapacidad
const buscarAlumnosDiscapacidad = () => {
  if (busquedaAlumnoDiscapacidad.value.length < 2) {
    resultadosDiscapacidad.value = []
    return
  }

  const termino = busquedaAlumnoDiscapacidad.value.toLowerCase()
  resultadosDiscapacidad.value = todosLosAlumnos.filter((alumno) => {
    // Filtrar alumnos que ya están en la lista
    const yaAgregado = alumnosDiscapacidadLista.value.some((a) => a.id === alumno.id)
    if (yaAgregado) return false

    // Buscar por nombre, apellidos o número de control
    return (
      alumno.nombre.toLowerCase().includes(termino) ||
      alumno.apellidos.toLowerCase().includes(termino) ||
      alumno.numControl.includes(termino)
    )
  })
}

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
const buscarAlumnosReprobados = () => {
  if (busquedaAlumnoReprobado.value.length < 2) {
    resultadosReprobados.value = []
    return
  }

  const termino = busquedaAlumnoReprobado.value.toLowerCase()
  resultadosReprobados.value = todosLosAlumnos.filter((alumno) => {
    // Filtrar alumnos que ya están en la lista
    const yaAgregado = alumnosReprobadosLista.value.some((a) => a.id === alumno.id)
    if (yaAgregado) return false

    // Buscar por nombre, apellidos o número de control
    return (
      alumno.nombre.toLowerCase().includes(termino) ||
      alumno.apellidos.toLowerCase().includes(termino) ||
      alumno.numControl.includes(termino)
    )
  })
}

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
const buscarAlumnosAsesoria = () => {
  if (busquedaAlumnoAsesoria.value.length < 2) {
    resultadosAsesoria.value = []
    return
  }

  const termino = busquedaAlumnoAsesoria.value.toLowerCase()
  resultadosAsesoria.value = todosLosAlumnos.filter((alumno) => {
    // Filtrar alumnos que ya están en la lista
    const yaAgregado = alumnosAsesoriaLista.value.some((item) => item.alumno.id === alumno.id)
    if (yaAgregado) return false

    // Buscar por nombre, apellidos o número de control
    return (
      alumno.nombre.toLowerCase().includes(termino) ||
      alumno.apellidos.toLowerCase().includes(termino) ||
      alumno.numControl.includes(termino)
    )
  })
}

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
  () => formData.hayAlumnosDesercion,
  (newValue) => {
    if (newValue === 'No') {
      formData.alumnosDesercion = null
      alumnosDesercionLista.value = []
    }
  },
)

// Observar cambios en alumnosDiscapacidad para resetear valores cuando cambia a "No"
watch(
  () => formData.alumnosDiscapacidad,
  (newValue) => {
    if (newValue === 'No') {
      alumnosDiscapacidadLista.value = []
    }
  },
)

// Observar cambios en alumnosReprobados para resetear valores cuando cambia a "No"
watch(
  () => formData.alumnosReprobados,
  (newValue) => {
    if (newValue === 'No') {
      alumnosReprobadosLista.value = []
    }
  },
)

// Función para manejar la carga de archivos
const handleFileUpload = (event) => {
  formData.evidencia = event.target.files[0]
}

// Función para enviar el formulario
const enviarFormulario = () => {
  // Validar que la cantidad de alumnos en deserción coincida con la lista
  if (
    formData.hayAlumnosDesercion === 'Si' &&
    parseInt(formData.alumnosDesercion) !== alumnosDesercionLista.value.length
  ) {
    alert('La cantidad de alumnos en deserción no coincide con la lista de alumnos agregados.')
    return
  }

  // Preparar datos para enviar
  const datosEnviar = {
    ...formData,
    alumnosDesercionDetalle: alumnosDesercionLista.value,
    alumnosDiscapacidadDetalle: alumnosDiscapacidadLista.value,
    alumnosReprobadosDetalle: alumnosReprobadosLista.value,
    alumnosAsesoriaDetalle: alumnosAsesoriaLista.value,
  }

  // Aquí iría la lógica para enviar el formulario
  emit('guardar', datosEnviar)
  console.log('Datos del formulario:', datosEnviar)
}
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
