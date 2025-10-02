<script setup>
import { ref } from 'vue'

// Variable reactiva para guardar la referencia al archivo seleccionado
const selectedFile = ref(null)

// Definimos el evento que este componente emitirá
const emit = defineEmits(['file-selected'])

// Esta función se ejecuta cuando el usuario elige un archivo del explorador
function handleFileChange(event) {
  selectedFile.value = event.target.files[0]
  // Emitimos el evento con el archivo para que el padre (App.vue) lo reciba
  emit('file-selected', selectedFile.value)
}
</script>

<template>
  <div class="uploader-container">
    <h3>Cargar nueva lista de alumnos</h3>
    <p>Selecciona un archivo Excel. Los datos existentes serán reemplazados.</p>
    <input type="file" @change="handleFileChange" accept=".xlsx, .xls" />
  </div>
</template>

<style scoped>
.uploader-container {
  padding: 1rem;
  border: 1px dashed #ccc;
  border-radius: 8px;
  margin-bottom: 2rem;
  background-color: #fafafa;
}
input[type='file'] {
  margin-top: 0.5rem;
}
</style>
