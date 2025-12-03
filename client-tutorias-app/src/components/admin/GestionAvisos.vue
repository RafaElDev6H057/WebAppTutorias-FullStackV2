<template>
  <!-- ==================== CONTAINER GESTIÓN AVISOS ==================== -->
  <div class="bg-white rounded-lg shadow-md p-6 border-l-4" style="border-color: #0a3b76">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-xl font-bold text-gray-900 flex items-center gap-2">
          <svg
            class="w-6 h-6"
            :style="{ color: '#0A3B76' }"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
            />
          </svg>
          Gestión de Avisos
        </h2>
        <p class="text-sm text-gray-600 mt-1">Administra los avisos que verán los alumnos</p>
      </div>

      <!-- Botón Crear Aviso -->
      <button
        @click="openModal('create')"
        class="text-white px-4 py-2 rounded-md text-sm font-medium transition duration-150 ease-in-out flex items-center gap-2"
        :style="{ background: '#0A3B76' }"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 4v16m8-8H4"
          />
        </svg>
        Crear Aviso
      </button>
    </div>

    <!-- ==================== MENSAJES ==================== -->
    <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 translate-y-1"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="successMessage"
        class="mb-4 p-3 rounded border-l-4"
        style="background: #e8f5ff; border-color: #0a3b76"
      >
        <p class="text-sm font-medium" :style="{ color: '#0A3B76' }">{{ successMessage }}</p>
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
      <div v-if="errorMessage" class="mb-4 p-3 bg-red-50 border-l-4 border-red-500 rounded">
        <p class="text-sm text-red-800 font-medium">{{ errorMessage }}</p>
      </div>
    </Transition>

    <!-- ==================== LOADING ==================== -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <svg
        class="animate-spin h-8 w-8"
        :style="{ color: '#0A3B76' }"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        ircle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </svg>
      <span class="ml-2 text-gray-600">Cargando avisos...</span>
    </div>

    <!-- ==================== LISTA DE AVISOS ==================== -->
    <div v-else-if="avisos.length > 0" class="space-y-4">
      <div
        v-for="aviso in avisos"
        :key="aviso.id"
        class="border rounded-lg p-4 hover:shadow-md transition-shadow duration-200"
        :style="
          aviso.is_activo
            ? { background: '#e8f5ff', borderColor: '#0A3B76' }
            : { background: '#f3f3f5', borderColor: '#ABACAE' }
        "
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <div class="flex items-center gap-3 mb-2">
              <h3 class="text-lg font-bold text-gray-900">{{ aviso.titulo }}</h3>

              <span
                class="px-2 py-1 text-xs font-semibold rounded-full"
                :style="
                  aviso.is_activo
                    ? { background: '#cfe6ff', color: '#0A3B76' }
                    : { background: '#dddde2', color: '#4a4a4a' }
                "
              >
                {{ aviso.is_activo ? 'Activo' : 'Inactivo' }}
              </span>
            </div>

            <p class="text-sm text-gray-700 mb-2">{{ aviso.descripcion }}</p>

            <div v-if="aviso.link" class="flex items-center gap-2 mb-2">
              <svg
                class="w-4 h-4"
                :style="{ color: '#0A3B76' }"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"
                />
              </svg>
              <a
                :href="aviso.link"
                target="_blank"
                class="text-sm hover:underline"
                :style="{ color: '#0A3B76' }"
              >
                {{ aviso.link }}
              </a>
            </div>

            <div class="flex items-center gap-4 text-xs text-gray-500">
              <span>Creado: {{ formatDate(aviso.created_at) }}</span>
              <span v-if="aviso.updated_at !== aviso.created_at">
                Actualizado: {{ formatDate(aviso.updated_at) }}
              </span>
            </div>
          </div>

          <!-- Botones -->
          <div class="flex items-center gap-2 ml-4">
            <button
              @click="openModal('edit', aviso)"
              class="p-2 rounded-lg transition-colors duration-200"
              :style="{ color: '#0A3B76', background: '#e8f5ff' }"
              title="Editar"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                />
              </svg>
            </button>

            <button
              @click="confirmDelete(aviso)"
              class="p-2 text-red-600 hover:bg-red-100 rounded-lg transition-colors duration-200"
              title="Eliminar"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Sin avisos -->
    <div v-else class="text-center py-12">
      <svg
        class="w-16 h-16 text-gray-400 mx-auto mb-4"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
        />
      </svg>

      <p class="text-gray-600">No hay avisos creados aún</p>

      <button
        @click="openModal('create')"
        class="mt-4 font-medium hover:underline"
        :style="{ color: '#0A3B76' }"
      >
        Crear el primer aviso
      </button>
    </div>

    <!-- ==================== MODAL CREAR/EDITAR ==================== -->
    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="showModal"
        class="fixed inset-0 bg-gray-900 bg-opacity-75 overflow-y-auto z-50 flex items-center justify-center p-4"
      >
        <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full" @click.stop>
          <!-- Header -->
          <div class="px-6 py-4 rounded-t-lg" :style="{ background: '#0A3B76' }">
            <h3 class="text-xl font-bold text-white">
              {{ modalMode === 'create' ? 'Crear Nuevo Aviso' : 'Editar Aviso' }}
            </h3>
          </div>

          <!-- Body -->
          <form @submit.prevent="saveAviso" class="p-6 space-y-4">
            <div>
              <label for="titulo" class="block text-sm font-medium text-gray-700 mb-1">
                Título *
              </label>
              <input
                v-model="formData.titulo"
                type="text"
                id="titulo"
                required
                class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2"
                :style="{
                  borderColor: '#ABACAE',
                  '--tw-ring-color': '#0A3B76',
                }"
                placeholder="Ej: Convocatoria de Becas 2025"
              />
            </div>

            <div>
              <label for="descripcion" class="block text-sm font-medium text-gray-700 mb-1">
                Descripción *
              </label>
              <textarea
                v-model="formData.descripcion"
                id="descripcion"
                required
                rows="4"
                class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2"
                :style="{
                  borderColor: '#ABACAE',
                  '--tw-ring-color': '#0A3B76',
                }"
                placeholder="Describe el aviso..."
              ></textarea>
            </div>

            <div>
              <label for="link" class="block text-sm font-medium text-gray-700 mb-1">
                Link (opcional)
              </label>
              <input
                v-model="formData.link"
                type="url"
                id="link"
                class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2"
                :style="{
                  borderColor: '#ABACAE',
                  '--tw-ring-color': '#0A3B76',
                }"
                placeholder="https://ejemplo.com/informacion"
              />
            </div>

            <div class="flex items-center">
              <input
                v-model="formData.is_activo"
                type="checkbox"
                id="is_activo"
                class="w-4 h-4 rounded focus:ring-2"
                :style="{
                  color: '#0A3B76',
                  '--tw-ring-color': '#0A3B76',
                  borderColor: '#ABACAE',
                }"
              />
              <label for="is_activo" class="ml-2 text-sm font-medium text-gray-700">
                Aviso activo (visible para alumnos)
              </label>
            </div>

            <!-- Footer -->
            <div class="flex justify-end gap-3 pt-4 border-t">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 rounded-md transition-colors"
                :style="{ background: '#dddde2', color: '#333' }"
              >
                Cancelar
              </button>

              <button
                type="submit"
                :disabled="isSaving"
                class="px-4 py-2 text-white rounded-md transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                :style="{ background: '#0A3B76' }"
              >
                {{
                  isSaving
                    ? 'Guardando...'
                    : modalMode === 'create'
                      ? 'Crear Aviso'
                      : 'Actualizar Aviso'
                }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>

    <!-- ==================== MODAL ELIMINAR ==================== -->
    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="showDeleteModal"
        class="fixed inset-0 bg-gray-900 bg-opacity-75 z-50 flex items-center justify-center p-4"
        @click="cancelDelete"
      >
        <div class="bg-white rounded-lg shadow-xl max-w-md w-full" @click.stop>
          <!-- Header -->
          <div class="px-6 py-4 bg-red-600 rounded-t-lg">
            <h3 class="text-xl font-bold text-white flex items-center gap-2">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
              Confirmar Eliminación
            </h3>
          </div>

          <!-- Body -->
          <div class="p-6">
            <p class="text-gray-700 mb-4">
              ¿Estás seguro de que deseas eliminar el aviso
              <strong>"{{ avisoToDelete?.titulo }}"</strong>?
            </p>
            <p class="text-sm text-red-600 font-medium">Esta acción no se puede deshacer.</p>
          </div>

          <!-- Footer -->
          <div class="px-6 py-4 bg-gray-50 rounded-b-lg flex justify-end gap-3">
            <button
              @click="cancelDelete"
              :disabled="isDeleting"
              class="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 transition-colors disabled:opacity-50"
            >
              Cancelar
            </button>
            <button
              @click="deleteAviso"
              :disabled="isDeleting"
              class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <svg
                v-if="isDeleting"
                class="animate-spin h-4 w-4"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                ircle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                stroke-width="4" />
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              {{ isDeleting ? 'Eliminando...' : 'Eliminar' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { avisosAPI } from '@/api/avisos'
import { ref, onMounted } from 'vue'

// ==================== STATE ====================
const avisos = ref([])
const isLoading = ref(false)
const isSaving = ref(false)
const isDeleting = ref(false)
const showModal = ref(false)
const showDeleteModal = ref(false)
const modalMode = ref('create') // 'create' | 'edit'
const avisoToDelete = ref(null)
const successMessage = ref(null)
const errorMessage = ref(null)

const formData = ref({
  titulo: '',
  descripcion: '',
  link: '',
  is_activo: false,
})

const currentAvisoId = ref(null)

// ==================== API CALLS ====================
const fetchAvisos = async () => {
  isLoading.value = true
  errorMessage.value = null

  try {
    const response = await avisosAPI.getAll()

    avisos.value = response.data
    console.log('✅ Avisos cargados:', avisos.value.length)
  } catch (error) {
    console.error('❌ Error al cargar avisos:', error)
    errorMessage.value = 'No se pudieron cargar los avisos. Intenta de nuevo.'
  } finally {
    isLoading.value = false
  }
}

const saveAviso = async () => {
  isSaving.value = true
  errorMessage.value = null
  successMessage.value = null

  try {
    const payload = {
      titulo: formData.value.titulo,
      descripcion: formData.value.descripcion,
      link: formData.value.link || null,
      is_activo: formData.value.is_activo,
    }

    let response
    if (modalMode.value === 'create') {
      response = await avisosAPI.create(payload)
      successMessage.value = '✅ Aviso creado exitosamente'
    } else {
      //eslint-disable-next-line no-unused-vars
      response = await avisosAPI.update(currentAvisoId.value, payload)
      successMessage.value = '✅ Aviso actualizado exitosamente'
    }

    await fetchAvisos()
    closeModal()

    setTimeout(() => {
      successMessage.value = null
    }, 3000)
  } catch (error) {
    console.error('❌ Error al guardar aviso:', error)
    errorMessage.value = `No se pudo ${modalMode.value === 'create' ? 'crear' : 'actualizar'} el aviso. Intenta de nuevo.`

    setTimeout(() => {
      errorMessage.value = null
    }, 3000)
  } finally {
    isSaving.value = false
  }
}

const deleteAviso = async () => {
  if (!avisoToDelete.value) return

  isDeleting.value = true
  errorMessage.value = null

  try {
    await avisosAPI.delete(avisoToDelete.value.id)

    successMessage.value = '✅ Aviso eliminado exitosamente'
    await fetchAvisos()
    cancelDelete()

    setTimeout(() => {
      successMessage.value = null
    }, 3000)
  } catch (error) {
    console.error('❌ Error al eliminar aviso:', error)
    errorMessage.value = 'No se pudo eliminar el aviso. Intenta de nuevo.'
    cancelDelete()

    setTimeout(() => {
      errorMessage.value = null
    }, 3000)
  } finally {
    isDeleting.value = false
  }
}

// ==================== MODAL HANDLERS ====================
const openModal = (mode, aviso = null) => {
  modalMode.value = mode
  showModal.value = true

  if (mode === 'edit' && aviso) {
    currentAvisoId.value = aviso.id
    formData.value = {
      titulo: aviso.titulo,
      descripcion: aviso.descripcion,
      link: aviso.link || '',
      is_activo: aviso.is_activo,
    }
  } else {
    resetForm()
  }
}

const closeModal = () => {
  showModal.value = false
  resetForm()
}

const confirmDelete = (aviso) => {
  avisoToDelete.value = aviso
  showDeleteModal.value = true
}

const cancelDelete = () => {
  showDeleteModal.value = false
  avisoToDelete.value = null
}

const resetForm = () => {
  formData.value = {
    titulo: '',
    descripcion: '',
    link: '',
    is_activo: false,
  }
  currentAvisoId.value = null
}

// ==================== UTILITY FUNCTIONS ====================
const formatDate = (dateString) => {
  const date = new Date(dateString)
  const utcMinus6 = new Date(date.getTime() - 6 * 60 * 60 * 1000)
  return utcMinus6.toLocaleDateString('es-MX', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// ==================== LIFECYCLE ====================
onMounted(() => {
  fetchAvisos()
})
</script>
