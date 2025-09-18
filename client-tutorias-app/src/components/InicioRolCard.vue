<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  icono: Object,
  titulo: String,
  descripcion: String,
  ruta: String,
})
</script>

<template>
  <RouterLink
    :to="ruta"
    class="group relative overflow-hidden rounded-xl bg-white p-6 shadow-md hover:shadow-xl transition-all duration-300 border border-gray-100"
  >
    <div
      class="absolute inset-0 bg-gradient-to-r from-green-600 to-blue-600 opacity-0 group-hover:opacity-10 transition-opacity duration-300"
    />

    <div class="relative space-y-4">
      <div class="h-14 w-14 rounded-lg bg-green-100 flex items-center justify-center">
        <component :is="icono" class="h-6 w-6 text-green-600"></component>
      </div>

      <div>
        <h3 class="text-lg font-semibold text-gray-900 group-hover:text-gray-900 transition-colors">
          {{ titulo }}
        </h3>
        <p class="mt-1 text-sm text-gray-600">{{ descripcion }}</p>
      </div>

      <div class="pt-2">
        <span
          class="inline-flex items-center text-sm font-medium text-green-600 group-hover:underline"
        >
          Ingresar
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
