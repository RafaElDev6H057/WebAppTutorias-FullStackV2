// import './assets/main.css'
import './assets/style.css'
import '@fontsource/poppins/400.css'
import '@fontsource/poppins/700.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)

app.mount('#app')
