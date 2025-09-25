<template>
  <div class="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md mt-10 border border-gray-200">
    <h2 class="text-2xl font-bold mb-6 text-center text-gray-800">Reporte Integral de Tutoría</h2>
    <div class="flex flex-col bg-gray-100 p-4 rounded-lg mb-4">
      <p class="font-bold">
        Nombre: <span class="font-normal">{{ props.nombre }}</span>
      </p>
      <p class="font-bold">
        Número de Control: <span class="font-normal">{{ props.num_control }}</span>
      </p>
    </div>
    <form @submit.prevent="guardarReporteIntegral" class="space-y-6">
      <!-- Sección: Estudiantes atendidos -->
      <div class="bg-blue-50 p-4 rounded-lg">
        <h3 class="text-lg font-semibold mb-3 text-blue-800">Estudiantes atendidos</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Tutoría Grupal:</label>
            <input
              v-model="datos.tutoria_grupal"
              type="number"
              min="0"
              max="16"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 bg-white p-2"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Tutoría Individual:</label>
            <input
              v-model="datos.tutoria_individual"
              type="number"
              min="0"
              max="2"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 bg-white p-2"
            />
          </div>
        </div>
      </div>

      <!-- Sección: Nombre de asignaturas con unidades reprobadas -->
      <div class="bg-green-50 p-4 rounded-lg">
        <h3 class="text-lg font-semibold mb-3 text-green-800">
          Nombre de asignaturas con unidades reprobadas
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Seguimiento 1:</label>
            <textarea
              v-model="datos.seguimiento_1"
              rows="3"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-300 focus:ring focus:ring-green-200 focus:ring-opacity-50 bg-white p-2"
              placeholder="Ingrese las materias separadas por comas"
            ></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Seguimiento 2:</label>
            <textarea
              v-model="datos.seguimiento_2"
              rows="3"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-300 focus:ring focus:ring-green-200 focus:ring-opacity-50 bg-white p-2"
              placeholder="Ingrese las materias separadas por comas"
            ></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Seguimiento 3:</label>
            <textarea
              v-model="datos.seguimiento_3"
              rows="3"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-300 focus:ring focus:ring-green-200 focus:ring-opacity-50 bg-white p-2"
              placeholder="Ingrese las materias separadas por comas"
            ></textarea>
          </div>
        </div>
      </div>

      <!-- Sección: Área canalizada -->
      <div class="bg-purple-50 p-4 rounded-lg">
        <h3 class="text-lg font-semibold mb-3 text-purple-800">Área canalizada</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Jefatura Académica:</label>
            <input
              v-model="datos.jefatura_academica"
              type="number"
              min="0"
              max="1"
              step="1"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-300 focus:ring focus:ring-purple-200 focus:ring-opacity-50 bg-white p-2"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Ciencias Básicas:</label>
            <input
              v-model="datos.ciencias_basicas"
              type="number"
              min="0"
              max="1"
              step="1"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-300 focus:ring focus:ring-purple-200 focus:ring-opacity-50 bg-white p-2"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Psicología:</label>
            <input
              v-model="datos.psicologia"
              type="number"
              min="0"
              max="1"
              step="1"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-300 focus:ring focus:ring-purple-200 focus:ring-opacity-50 bg-white p-2"
            />
          </div>
        </div>
      </div>

      <!-- Sección: Estatus final de materias detectadas con necesidades académicas -->
      <div class="bg-yellow-50 p-4 rounded-lg">
        <h3 class="text-lg font-semibold mb-3 text-yellow-800">
          Estatus final de materias detectadas con necesidades académicas
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700"
              >Número de materias aprobadas:</label
            >
            <input
              v-model="datos.materias_aprobadas"
              type="number"
              min="0"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-yellow-300 focus:ring focus:ring-yellow-200 focus:ring-opacity-50 bg-white p-2"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700"
              >Nombre de materias No aprobadas:</label
            >
            <textarea
              v-model="datos.materias_no_aprobadas"
              rows="3"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-yellow-300 focus:ring focus:ring-yellow-200 focus:ring-opacity-50 bg-white p-2"
              placeholder="Ingrese las materias separadas por comas"
            ></textarea>
          </div>
        </div>
      </div>

      <div class="mt-6">
        <button
          type="submit"
          class="w-full py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150 ease-in-out"
        >
          Guardar Reporte
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios' // 👈 1. Importa axios

const props = defineProps({
  nombre: {
    type: String,
    required: true,
  },
  num_control: {
    type: String,
    required: true,
  },
})

// Objeto reactivo para almacenar los datos del formulario
const datos = ref({
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
})

// 👇 2. Implementa la función para guardar
const guardarReporteIntegral = async () => {
  try {
    // 3. Realiza la petición POST a tu endpoint de FastAPI
    const response = await axios.post(
      'http://localhost:8000/api/reportes/integral',
      datos.value, // El .value es importante porque 'datos' es una ref
    )

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
</script>
