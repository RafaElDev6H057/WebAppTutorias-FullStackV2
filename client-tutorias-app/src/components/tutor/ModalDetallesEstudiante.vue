<template>
  <!-- Modal de detalles del estudiante -->
  <Transition
    enter-active-class="transition ease-out duration-300"
    enter-from-class="opacity-0 scale-95"
    enter-to-class="opacity-100 scale-100"
    leave-active-class="transition ease-in duration-200"
    leave-from-class="opacity-100 scale-100"
    leave-to-class="opacity-0 scale-95"
  >
    <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto">
      <div
        class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
      >
        <div class="fixed inset-0 transition-opacity" aria-hidden="true">
          <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
        </div>

        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true"
          >&#8203;</span
        >

        <div
          v-if="student"
          class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
        >
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
  <div class="absolute top-4 right-4">
    <button
      @click="$emit('close')"
      class="text-[#0A3B76] hover:text-blue-800 transition-colors"
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M6 18L18 6M6 6l12 12"
        />
      </svg>
    </button>
  </div>

  <h2 class="text-2xl font-bold mb-6 text-[#0A3B76] border-b pb-2">
    Detalles del Estudiante
  </h2>

  <div class="space-y-6">
    <!-- Información del Alumno -->
    <div class="bg-gray-50 p-4 rounded-lg">
      <h3 class="text-lg font-semibold text-[#0A3B76] mb-3">Información del Alumno</h3>
      <div class="space-y-2">
        <div class="grid grid-cols-3 gap-2">
          <span class="text-gray-600 font-medium">Nombre:</span>
          <span class="col-span-2 text-gray-900">
            {{ student.nombre }} {{ student.apellido_p }} {{ student.apellido_m }}
          </span>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <span class="text-gray-600 font-medium">Número de Control:</span>
          <span class="col-span-2 text-gray-900">{{ student.num_control }}</span>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <span class="text-gray-600 font-medium">Carrera:</span>
          <span class="col-span-2 text-gray-900">{{ student.carrera }}</span>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <span class="text-gray-600 font-medium">Semestre Actual:</span>
          <span class="col-span-2 text-gray-900">{{ student.semestre_actual }}°</span>
        </div>
      </div>
    </div>

    <!-- Información de la Tutoría -->
    <div class="bg-gray-50 p-4 rounded-lg">
      <h3 class="text-lg font-semibold text-[#0A3B76] mb-3">Información de la Tutoría</h3>
      <div class="space-y-2">
        <div class="grid grid-cols-3 gap-2">
          <span class="text-gray-600 font-medium">Nivel de Tutoría:</span>
          <span class="col-span-2 text-gray-900">{{ student.tutoring.semestre }}°</span>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <span class="text-gray-600 font-medium">Periodo:</span>
          <span class="col-span-2 text-gray-900">{{ student.tutoring.periodo }}</span>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <span class="text-gray-600 font-medium">Día:</span>
          <span class="col-span-2 text-gray-900">{{ capitalizedDay }}</span>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <span class="text-gray-600 font-medium">Hora:</span>
          <span class="col-span-2 text-gray-900">{{ formattedHour }}</span>
        </div>
        <div class="mt-4">
          <span class="text-gray-600 font-medium block mb-1">Observaciones:</span>
          <p class="text-gray-900 bg-white p-3 rounded border">
            {{ student.tutoring.observaciones || 'Sin observaciones' }}
          </p>
        </div>
      </div>
    </div>
  </div>

  <div class="mt-6 flex justify-end">
    <button
      @click="$emit('close')"
      class="bg-[#0A3B76] hover:bg-blue-800 text-white font-medium py-2 px-6 rounded-lg transition-colors duration-200"
    >
      Cerrar
    </button>
  </div>
</div>

        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { computed } from 'vue'

// ==================== PROPS ====================
const props = defineProps({
  show: {
    type: Boolean,
    required: true,
  },
  student: {
    type: Object,
    default: null,
  },
})

// ==================== EMITS ====================
defineEmits(['close'])

// ==================== COMPUTED ====================
const capitalizedDay = computed(() => {
  if (props.student?.tutoring?.dia) {
    return props.student.tutoring.dia.charAt(0).toUpperCase() + props.student.tutoring.dia.slice(1)
  }
  return 'No especificado'
})

const formattedHour = computed(() => {
  if (props.student?.tutoring?.hora) {
    const [horas, minutos] = props.student.tutoring.hora.split(':').map(Number)
    const ampm = horas < 12 ? 'AM' : 'PM'
    const horaFormateada = `${horas % 12 || 12}:${minutos.toString().padStart(2, '0')} ${ampm}`
    return horaFormateada
  }
  return 'No especificada'
})
</script>

<style scoped>
.text-coral-600 {
  color: #ff5242;
}

.bg-coral-500 {
  background-color: #ff6b5b;
}

.hover\:bg-coral-600:hover {
  background-color: #ff5242;
}
</style>
