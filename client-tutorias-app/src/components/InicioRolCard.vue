<script setup>
import { RouterLink } from 'vue-router'
import { computed } from 'vue'

const props = defineProps({
  icono: Object,
  titulo: String,
  descripcion: String,
  ruta: String,
  color: {
    type: String,
    default: 'green',
  },
  isDepartamento: {
    type: Boolean,
    default: false,
  },
})

const colorClasses = computed(() => {
  const colors = {
    green: {
      bg: 'bg-green-100',
      icon: 'text-green-600',
      gradient: 'from-green-600 to-blue-600',
      text: 'text-green-600',
    },
    blue: {
      bg: 'bg-blue-100',
      icon: 'text-blue-600',
      gradient: 'from-blue-600 to-cyan-600',
      text: 'text-blue-600',
    },
    purple: {
      bg: 'bg-purple-100',
      icon: 'text-purple-600',
      gradient: 'from-purple-600 to-pink-600',
      text: 'text-purple-600',
    },
    teal: {
      bg: 'bg-teal-100',
      icon: 'text-teal-600',
      gradient: 'from-teal-600 to-cyan-600',
      text: 'text-teal-600',
    },
    indigo: {
      bg: 'bg-indigo-100',
      icon: 'text-indigo-600',
      gradient: 'from-indigo-600 to-purple-600',
      text: 'text-indigo-600',
    },
    rose: {
      bg: 'bg-rose-100',
      icon: 'text-rose-600',
      gradient: 'from-rose-600 to-pink-600',
      text: 'text-rose-600',
    },
  }
  return colors[props.color] || colors.green
})
</script>

<template>
  <RouterLink
    :to="ruta"
    class="group relative overflow-hidden rounded-xl bg-white p-6 shadow-md hover:shadow-xl transition-all duration-300 border border-gray-100 transform hover:-translate-y-1"
  >
    <div
      class="absolute inset-0 bg-gradient-to-r opacity-0 group-hover:opacity-10 transition-opacity duration-300"
      :class="`${colorClasses.gradient}`"
    />

    <div class="relative space-y-4">
      <div class="h-14 w-14 rounded-lg flex items-center justify-center" :class="colorClasses.bg">
        <component :is="icono" class="h-6 w-6" :class="colorClasses.icon"></component>
      </div>

      <div>
        <h3 class="text-lg font-semibold text-gray-900 group-hover:text-gray-900 transition-colors">
          {{ titulo }}
        </h3>
        <p class="mt-1 text-sm text-gray-600">{{ descripcion }}</p>
      </div>

      <div class="pt-2">
        <span
          class="inline-flex items-center text-sm font-medium group-hover:underline"
          :class="colorClasses.text"
        >
          {{ isDepartamento ? 'Acceder' : 'Ingresar' }}
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-4 w-4 ml-1 transition-transform group-hover:translate-x-1"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5l7 7-7 7"
            />
          </svg>
        </span>
      </div>
    </div>
  </RouterLink>
</template>
