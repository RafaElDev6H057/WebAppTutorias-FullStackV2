<template>
  <div class="space-y-6">
    <!-- Pestañas -->
    <div class="border-b border-[#ABACAE]">
  <nav class="-mb-px flex space-x-8">
    <a
      v-for="tab in tabs"
      :key="tab.id"
      href="#"
      @click.prevent="currentTab = tab.id"
      :class="[
        currentTab === tab.id
          ? 'border-[#0A3B76] text-[#0A3B76]'
          : 'border-transparent text-gray-600 hover:text-[#0A3B76] hover:border-[#ABACAE]',
        'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm',
      ]"
    >
      {{ tab.name }}
    </a>
  </nav>
</div>


    <!-- Tabla de estudiantes -->
    <div class="flex flex-col">
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
            <table
              v-else-if="filteredStudents.length > 0"
              class="min-w-full divide-y divide-gray-200"
            >
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
                  v-for="student in filteredStudents"
                  :key="student.id"
                  class="hover:bg-gray-50 transition-colors"
                >
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div>
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
      ? 'bg-[#0A3B76]/20 text-[#0A3B76]'
      : 'bg-[#0A3B76]/40 text-[#0A3B76]/70'
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
  @click.prevent="$emit('view-details', student)"
  class="text-[#0A3B76] hover:text-[#082C54] mx-4"
>
  Ver detalles
</a>

                    <button
  @click="$emit('delete-tutoria', student)"
  class="px-4 py-2 text-white rounded-md transition duration-150 ease-in-out inline-flex items-center gap-2 ml-2"
  style="background-color: #ABACAE; hover:bg-gray-400;"
  title="Eliminar tutoría"
>
  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
            <div
              v-else-if="!loading && filteredStudents.length === 0"
              class="text-center py-12 px-4"
            >
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
              <h3 class="mt-4 text-lg font-medium text-gray-900">No se encontraron estudiantes</h3>
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
      v-if="!loading && filteredStudents.length > 0"
      class="py-3 flex items-center justify-between bg-white rounded-lg px-4"
    >
      <div class="flex-1 flex justify-between sm:hidden">
        <button
          @click="$emit('prev-page')"
          :disabled="currentPage === 1 || loading"
          class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Anterior
        </button>
        <button
          @click="$emit('next-page')"
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
            <span class="font-medium">{{ Math.min(currentPage * itemsPerPage, totalItems) }}</span>
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
              @click="$emit('prev-page')"
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
  @click="$emit('go-to-page', page)"
  :disabled="loading"
  :class="[
    currentPage === page
      ? 'z-10 bg-[#0A3B76]/10 border-[#0A3B76] text-[#0A3B76]'
      : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50',
    'relative inline-flex items-center px-4 py-2 border text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed',
  ]"
>
  {{ page }}
</button>

            <button
              @click="$emit('next-page')"
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
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// ==================== PROPS ====================
const props = defineProps({
  students: {
    type: Array,
    required: true,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
  searchQuery: {
    type: String,
    default: '',
  },
  currentPage: {
    type: Number,
    default: 1,
  },
  totalPages: {
    type: Number,
    default: 1,
  },
  totalItems: {
    type: Number,
    default: 0,
  },
  itemsPerPage: {
    type: Number,
    default: 5,
  },
})

// ==================== EMITS ====================
defineEmits(['view-details', 'delete-tutoria', 'prev-page', 'next-page', 'go-to-page'])

// ==================== STATE ====================
const currentTab = ref('current')

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

// ==================== COMPUTED ====================
const filteredStudents = computed(() => {
  return props.students.filter((student) => {
    if (currentTab.value === 'current') {
      return student.status === 'A'
    } else {
      return student.status === 'completada'
    }
  })
})
</script>

<style scoped>
.bg-coral-50 {
  background-color: #fff1f0;
}

.border-coral-500 {
  border-color: #ff6b5b;
}

.text-coral-600 {
  color: #ff5242;
}

.hover\:text-coral-900:hover {
  color: #cc2d1d;
}

.text-coral-500 {
  color: #ff6b5b;
}
</style>
