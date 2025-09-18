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
    <form @submit.prevent="generarPDF" class="space-y-6">
      <!-- Sección: Estudiantes atendidos -->
      <div class="bg-blue-50 p-4 rounded-lg">
        <h3 class="text-lg font-semibold mb-3 text-blue-800">Estudiantes atendidos</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Tutoría Grupal:</label>
            <input
              v-model="datos.A1"
              type="number"
              min="0"
              max="16"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 bg-white p-2"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Tutoría Individual:</label>
            <input
              v-model="datos.A2"
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
              v-model="datos.B1"
              rows="3"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-300 focus:ring focus:ring-green-200 focus:ring-opacity-50 bg-white p-2"
              placeholder="Ingrese las materias separadas por comas"
            ></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Seguimiento 2:</label>
            <textarea
              v-model="datos.B2"
              rows="3"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-300 focus:ring focus:ring-green-200 focus:ring-opacity-50 bg-white p-2"
              placeholder="Ingrese las materias separadas por comas"
            ></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Seguimiento 3:</label>
            <textarea
              v-model="datos.B3"
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
              v-model="datos.C1"
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
              v-model="datos.C2"
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
              v-model="datos.C3"
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
              v-model="datos.D1"
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
              v-model="datos.D2"
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
import { PDFDocument, rgb } from 'pdf-lib'

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

const datos = ref({
  A1: 0, // Tutoría Grupal
  A2: 0, // Tutoría Individual
  B1: '', // Seguimiento 1
  B2: '', // Seguimiento 2
  B3: '', // Seguimiento 3
  C1: 0, // Jefatura Académica
  C2: 0, // Ciencias Básicas
  C3: 0, // Psicología
  D1: 0, // Materias aprobadas
  D2: '', // Materias no aprobadas
})

const celdaAncho = 100
const celdaAlto = 20
const offsetX = 100
const offsetY = 700

const calcularPosicion = (celda) => {
  let columna = celda.charCodeAt(0) - 65
  let fila = parseInt(celda.substring(1)) - 1
  let x = offsetX + columna * celdaAncho
  let y = offsetY - fila * celdaAlto
  return { x, y }
}

const generarPDF = async () => {
  const existingPdfBytes = await fetch('/formato.pdf').then((res) => res.arrayBuffer())
  const pdfDoc = await PDFDocument.load(existingPdfBytes)
  const page = pdfDoc.getPages()[0]

  for (let celda in datos.value) {
    let { x, y } = calcularPosicion(celda)
    let valor = datos.value[celda]
    if (typeof valor === 'number') {
      valor = valor.toString()
    }
    page.drawText(valor, { x, y, size: 12, color: rgb(0, 0, 0) })
  }

  const pdfBytes = await pdfDoc.save()
  const blob = new Blob([pdfBytes], { type: 'application/pdf' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = 'reporte_integral_tutoria.pdf'
  link.click()
}
</script>
