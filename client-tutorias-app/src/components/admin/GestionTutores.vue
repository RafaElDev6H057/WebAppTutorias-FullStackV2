<template>
  <!-- ==================== PANEL DE TUTORES ==================== -->
  <div class="space-y-6">
    <!-- Header con botones de acción -->
    <div class="flex justify-between items-center">
      <div>
        <h2 class="text-3xl font-bold text-gray-900">Gestión de Tutores</h2>
        <p class="text-sm text-gray-600 mt-1">Administra los tutores del sistema</p>
      </div>
      <div class="flex items-center gap-3">
        <BaseSearchInput v-model="searchQueryTutor" placeholder="Buscar Tutor..." />

        <button @click="openAssignmentModal"
          class="bg-[#0A3B76] hover:bg-[#082F5E] text-white px-4 py-2 rounded-md text-sm font-medium transition duration-150 ease-in-out flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          Asignar Tutorías
        </button>

        <button @click="openModal('add')"
          class="bg-[#ABACAE] hover:bg-[#9A9BA0] text-white px-4 py-2 rounded-md text-sm font-medium transition duration-150 ease-in-out flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Añadir Tutor
        </button>

      </div>
    </div>

    <!-- Estado de carga -->
    <!-- <div v-if="loadingTutor" class="flex justify-center items-center py-12">
      <svg
        class="animate-spin h-8 w-8 text-purple-600"
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
      <span class="ml-3 text-gray-600">Cargando tutores...</span>
    </div> -->

    <!-- Mensaje de error -->
    <Transition enter-active-class="transition ease-out duration-200" enter-from-class="opacity-0 translate-y-1"
      enter-to-class="opacity-100 translate-y-0" leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100" leave-to-class="opacity-0">
      <div v-if="errorTutor" class="bg-red-50 border-l-4 border-red-500 p-4 rounded-md">
        <p class="text-sm text-red-800 font-medium">{{ errorTutor }}</p>
      </div>
    </Transition>

    <!-- Tabla de tutores -->
    <div class="bg-white shadow-md rounded-lg overflow-hidden">
      <table v-if="tutors.length > 0" class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Nombre Completo
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Correo
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Teléfono
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Departamento
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Acciones
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="tutor in tutors" :key="tutor.id_tutor" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="text-sm font-medium text-gray-900">
                  {{ `${tutor.nombre} ${tutor.apellido_p} ${tutor.apellido_m}` }}
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{{ tutor.correo }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-500">---</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-500">---</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <div class="flex items-center gap-2">
                <button @click="editItem(tutor)"
                  class="text-white hover:bg-indigo-900 px-3 py-2 bg-indigo-600 rounded-lg transition-colors duration-200"
                  title="Editar">
                  <EditIcon />
                </button>
                <button @click="deleteTutor(tutor)"
                  class="text-white hover:bg-red-900 px-3 py-2 rounded-lg bg-red-600 transition-colors duration-200"
                  title="Eliminar">
                  <DeleteIcon />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Sin tutores -->
      <div v-if="tutors.length === 0 && !loadingTutor" class="text-center py-12 text-gray-500">
        <svg class="w-16 h-16 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <p class="text-lg font-medium">No hay tutores registrados</p>
        <p class="text-sm mt-1">Comienza agregando tutores al sistema</p>
      </div>
    </div>

    <!-- Paginación Tutores -->
    <div v-if="tutors.length > 0"
      class="bg-white rounded-lg px-4 py-3 flex items-center justify-between border-t border-gray-200 shadow-sm">
      <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
        <div>
          <p class="text-sm text-gray-700">
            Mostrando
            <span class="font-medium">{{ (currentPageTutor - 1) * itemsPerPageTutor + 1 }}</span>
            a
            <span class="font-medium">{{
              Math.min(currentPageTutor * itemsPerPageTutor, totalTutors)
              }}</span>
            de
            <span class="font-medium">{{ totalTutors }}</span>
            resultados
          </p>
        </div>
        <div>
          <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
            <button @click="prevPageTutor" :disabled="currentPageTutor === 1"
              class="relative inline-flex items-center px-4 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
              <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                  clip-rule="evenodd" />
              </svg>
              <span>Anterior</span>
            </button>

            <span
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
              Página {{ currentPageTutor }} de {{ totalPagesTutor }}
            </span>

            <button @click="nextPageTutor" :disabled="currentPageTutor >= totalPagesTutor"
              class="relative inline-flex items-center px-4 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
              <span>Siguiente</span>
              <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                  clip-rule="evenodd" />
              </svg>
            </button>
          </nav>
        </div>
      </div>
    </div>

    <!-- ==================== MODAL AÑADIR/EDITAR TUTOR ==================== -->
    <Transition enter-active-class="transition ease-out duration-300" enter-from-class="opacity-0"
      enter-to-class="opacity-100" leave-active-class="transition ease-in duration-200" leave-from-class="opacity-100"
      leave-to-class="opacity-0">
      <div v-if="showModal" class="fixed z-50 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog"
        aria-modal="true">
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="closeModal"></div>

          <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

          <div
            class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
            <div class="bg-gradient-to-r from-purple-600 to-purple-700 px-6 py-4">
              <h3 class="text-lg leading-6 font-medium text-white" id="modal-title">
                {{ modalMode === 'add' ? 'Añadir' : 'Editar' }} Tutor
              </h3>
            </div>

            <div class="bg-white px-6 pt-5 pb-4">
              <form @submit.prevent="submitForm" class="space-y-6">
                <!-- Nombres -->
                <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
                  <div class="sm:col-span-2">
                    <label for="nombre" class="block text-sm font-medium text-gray-700">
                      Nombre <span class="text-red-500">*</span>
                    </label>
                    <input type="text" id="nombre" v-model="formData.nombre"
                      class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm"
                      :class="{ 'border-red-500': errors.nombre }" />
                    <p v-if="errors.nombre" class="mt-2 text-sm text-red-600">
                      {{ errors.nombre[0] }}
                    </p>
                  </div>

                  <div>
                    <label for="apellido_p" class="block text-sm font-medium text-gray-700">
                      Apellido Paterno <span class="text-red-500">*</span>
                    </label>
                    <input type="text" id="apellido_p" v-model="formData.apellido_p"
                      class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm"
                      :class="{ 'border-red-500': errors.apellido_p }" />
                    <p v-if="errors.apellido_p" class="mt-2 text-sm text-red-600">
                      {{ errors.apellido_p[0] }}
                    </p>
                  </div>

                  <div>
                    <label for="apellido_m" class="block text-sm font-medium text-gray-700">
                      Apellido Materno <span class="text-red-500">*</span>
                    </label>
                    <input type="text" id="apellido_m" v-model="formData.apellido_m"
                      class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm"
                      :class="{ 'border-red-500': errors.apellido_m }" />
                    <p v-if="errors.apellido_m" class="mt-2 text-sm text-red-600">
                      {{ errors.apellido_m[0] }}
                    </p>
                  </div>
                </div>

                <!-- Correo y Contraseña -->
                <div class="grid grid-cols-2 gap-6">
                  <div>
                    <label for="correo" class="block text-sm font-medium text-gray-700">
                      Correo <span class="text-red-500">*</span>
                    </label>
                    <input type="email" id="correo" v-model="formData.correo"
                      class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm"
                      :class="{ 'border-red-500': errors.correo }" />
                    <p v-if="errors.correo" class="mt-2 text-sm text-red-600">
                      {{ errors.correo[0] }}
                    </p>
                  </div>

                  <div>
                    <label for="contraseña" class="block text-sm font-medium text-gray-700">
                      Contraseña <span class="text-red-500">*</span>
                    </label>
                    <div class="relative">
                      <input id="contraseña" v-model="formData.contraseña" :type="showPassword ? 'text' : 'password'"
                        class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm"
                        :class="{ 'border-red-500': errors.contraseña }" />
                      <button type="button" @click="showPassword = !showPassword"
                        class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500">
                        <ShowEye v-if="showPassword" />
                        <HideEye v-else />
                      </button>
                    </div>
                    <p v-if="errors.contraseña" class="mt-2 text-sm text-red-600">
                      {{ errors.contraseña[0] }}
                    </p>
                  </div>
                </div>

                <!-- Botones -->
                <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse gap-3 rounded-b-lg -mx-6 -mb-4">
                  <button type="submit"
                    class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-purple-600 text-base font-medium text-white hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 sm:ml-3 sm:w-auto sm:text-sm">
                    {{ modalMode === 'add' ? 'Añadir' : 'Guardar cambios' }}
                  </button>
                  <button @click="closeModal" type="button"
                    class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
                    Cancelar
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- ==================== MODAL CONFIRMAR ELIMINACIÓN ==================== -->
    <Transition enter-active-class="transition ease-out duration-300" enter-from-class="opacity-0"
      enter-to-class="opacity-100" leave-active-class="transition ease-in duration-200" leave-from-class="opacity-100"
      leave-to-class="opacity-0">
      <div v-if="showDeleteTutorModal" class="fixed z-50 inset-0 overflow-y-auto" aria-labelledby="modal-title"
        role="dialog" aria-modal="true">
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>

          <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

          <div
            class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <div class="sm:flex sm:items-start">
                <div
                  class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                  <svg class="h-6 w-6 text-red-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                  <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                    Eliminar Tutor
                  </h3>
                  <div class="mt-2">
                    <p class="text-sm text-gray-500">
                      ¿Estás seguro de que quieres eliminar a
                      <strong>{{ tutorToDelete?.nombre }} {{ tutorToDelete?.apellido_p }}
                        {{ tutorToDelete?.apellido_m }}</strong>? Esta acción no se puede deshacer.
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse gap-3">
              <button @click="confirmDeleteTutor" type="button"
                class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm">
                Eliminar
              </button>
              <button @click="cancelDeleteTutor" type="button"
                class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
                Cancelar
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- ==================== MODAL ASIGNAR TUTORÍAS ==================== -->
    <AssignmentUploader :show="showAssignmentModal" @close="closeAssignmentModal" @success="handleAssignmentSuccess" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

// IMPORTS - COMPONENTS
import DeleteIcon from '@/components/icons/DeleteIcon.vue'
import EditIcon from '@/components/icons/EditIcon.vue'
import ShowEye from '@/components/icons/ShowEye.vue'
import HideEye from '@/components/icons/HideEye.vue'
import BaseSearchInput from '@/components/ui/BaseSearchInput.vue'
import AssignmentUploader from '@/components/tutor/AssignmentUploader.vue'

// IMPORTS - SERVICES
import TutorService from '@/services/TutorService.js'

// ==================== ROUTER ====================
const router = useRouter()

// ==================== STATE - DATA ====================
const tutors = ref([])
const loadingTutor = ref(true)
const errorTutor = ref(null)
const errors = ref({})

// ==================== STATE - PAGINATION & SEARCH ====================
const currentPageTutor = ref(1)
const itemsPerPageTutor = ref(5)
const searchQueryTutor = ref('')
const hayMasTutores = ref(true)
const totalTutors = ref(0)
const totalPagesTutor = ref(1)
let debounceTimerTutor = null

// ==================== STATE - MODALS ====================
const showModal = ref(false)
const showDeleteTutorModal = ref(false)
const tutorToDelete = ref(null)
const showAssignmentModal = ref(false)
const modalMode = ref('add') // 'add' | 'edit'
const showPassword = ref(false)

// ==================== STATE - FORM ====================
const formData = reactive({
  nombre: '',
  apellido_p: '',
  apellido_m: '',
  correo: '',
  contraseña: '',
})

// ==================== API CALLS ====================
const fetchTutors = async (page = currentPageTutor.value) => {
  try {
    loadingTutor.value = true
    errorTutor.value = null

    const response = await TutorService.getTutores(
      page,
      itemsPerPageTutor.value,
      searchQueryTutor.value,
    )

    tutors.value = response.data.tutores
    hayMasTutores.value = response.data.tutores.length === 5
    totalTutors.value = response.data.total_tutores
    totalPagesTutor.value = Math.ceil(response.data.total_tutores / itemsPerPageTutor.value)
  } catch (err) {
    console.error('Error al obtener los tutores:', err)

    if (err.response?.data?.detail?.[0]?.type === 'string_too_short') {
      errorTutor.value = 'Favor de ingresar mínimo 3 caracteres a buscar'
    } else {
      errorTutor.value = 'No se pudo cargar la lista de tutores'
    }
    tutors.value = []
  } finally {
    loadingTutor.value = false
  }
}

const submitForm = async () => {
  try {
    const token = localStorage.getItem('accessToken')

    if (!token) {
      console.log('No hay token, redirigiendo al login...')
      router.push('/login_admin')
      return
    }

    errors.value = {}
    let response

    if (modalMode.value === 'add') {
      response = await axios.post('http://localhost:8000/api/tutores/', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (response.status === 201) {
        console.log('Tutor agregado exitosamente:', response.data)
        await fetchTutors()
        closeModal()
      }
    } else if (modalMode.value === 'edit') {
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
        console.log('Tutor actualizado exitosamente:', response.data)
        await fetchTutors()
        closeModal()
      }
    }
  } catch (error) {
    console.error('Error al enviar el formulario:', error)

    if (error.response && error.response.data && error.response.data.errors) {
      errors.value = error.response.data.errors
    } else {
      errors.value = { general: 'Ocurrió un error al procesar la solicitud.' }
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
        console.log('Tutor eliminado exitosamente')
        await fetchTutors()
      }
    } catch (error) {
      console.error('Error al eliminar el tutor:', error)
      errorTutor.value = 'No se pudo eliminar el tutor'
    } finally {
      showDeleteTutorModal.value = false
      tutorToDelete.value = null
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
      correo: '',
      contraseña: '',
    })
  }
}

const closeModal = () => {
  showModal.value = false
  showPassword.value = false
  clearErrors()
}

const editItem = (tutor) => {
  openModal('edit', tutor)
}

const deleteTutor = (tutor) => {
  tutorToDelete.value = tutor
  showDeleteTutorModal.value = true
}

const cancelDeleteTutor = () => {
  showDeleteTutorModal.value = false
  tutorToDelete.value = null
}

const openAssignmentModal = () => {
  showAssignmentModal.value = true
}

const closeAssignmentModal = () => {
  showAssignmentModal.value = false
}

const handleAssignmentSuccess = () => {
  console.log('✅ Asignaciones procesadas exitosamente')
  closeAssignmentModal()
}

// ==================== UTILITY FUNCTIONS ====================
const clearErrors = () => {
  errors.value = {}
}

// ==================== PAGINATION ====================
const nextPageTutor = () => {
  if (hayMasTutores.value) {
    currentPageTutor.value++
    fetchTutors(currentPageTutor.value)
  }
}

const prevPageTutor = () => {
  if (currentPageTutor.value > 1) {
    currentPageTutor.value--
    fetchTutors(currentPageTutor.value)
  }
}

// ==================== WATCHERS ====================
watch(searchQueryTutor, () => {
  clearTimeout(debounceTimerTutor)
  debounceTimerTutor = setTimeout(() => {
    currentPageTutor.value = 1
    fetchTutors()
  }, 500)
})

// ==================== LIFECYCLE HOOKS ====================
onMounted(async () => {
  await fetchTutors(currentPageTutor.value)
})
</script>
