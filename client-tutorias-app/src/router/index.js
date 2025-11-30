import { createRouter, createWebHistory } from 'vue-router'
import InicioView from '@/views/InicioView.vue'
// import LoginAdminView from '@/views/LoginAdminView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'inicio',
      component: InicioView,
    },
    {
      path: '/login_admin',
      name: 'login_admin',
      component: () => import('../views/LoginAdminView.vue'),
    },
    {
      path: '/login_alumno',
      name: 'login_alumno',
      component: () => import('../views/LoginAlumnoView.vue'),
    },
    {
      path: '/login_tutor',
      name: 'login_tutor',
      component: () => import('../views/LoginTutorView.vue'),
    },
    {
      path: '/login_alumno/dashboard',
      name: 'panel_alumno',
      component: () => import('../views/PanelAlumnoView.vue'),
    },
    {
      path: '/login_tutor/dashboard',
      name: 'panel_tutor',
      component: () => import('../views/PanelTutorView.vue'),
    },
    {
      path: '/login_admin/dashboard',
      name: 'panel_admin',
      component: () => import('../views/PanelAdminView.vue'),
    },
    {
      path: '/login_admin/descargas',
      name: 'descargas-admin',
      component: () => import('../views/DescargasView.vue'),
    },
  ],
})

export default router
