<template>
  <!-- Banner de Advertencia de Contraseña Insegura -->
  <Transition
    enter-active-class="transition ease-out duration-300"
    enter-from-class="opacity-0 translate-y-2"
    enter-to-class="opacity-100 translate-y-0"
    leave-active-class="transition ease-in duration-200"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div
      v-if="show"
      class="mx-4 mb-6 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded-lg shadow-sm"
    >
      <div class="flex items-start">
        <svg
          class="w-6 h-6 text-yellow-400 mr-3 flex-shrink-0"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
          />
        </svg>
        <div class="flex-1">
          <h3 class="text-sm font-bold text-yellow-800">Contraseña Insegura</h3>
          <p class="mt-1 text-sm text-yellow-700">
            Tu contraseña actual no está protegida adecuadamente. Por seguridad, te recomendamos
            cambiarla lo antes posible.
          </p>
          <button
            @click="$emit('change-password')"
            class="mt-3 text-sm font-semibold text-yellow-800 hover:text-yellow-900 underline inline-flex items-center gap-1 transition-colors"
          >
            Cambiar contraseña ahora
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 7l5 5m0 0l-5 5m5-5H6"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
defineProps({
  show: {
    type: Boolean,
    required: true,
  },
})

defineEmits(['change-password'])
</script>
