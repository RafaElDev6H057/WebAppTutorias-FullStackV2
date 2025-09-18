<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <Transition
    enter-active-class="transition-opacity ease-in-out duration-[0.9s]"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition-opacity ease-in-out duration-[0.9s]"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <RouterView />
  </Transition>
</template>

<style>
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';
</style>
