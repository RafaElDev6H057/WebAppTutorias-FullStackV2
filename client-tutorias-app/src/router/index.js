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
      path: '/alumno/dashboard',
      name: 'panel_alumno',
      component: () => import('../views/PanelAlumnoView.vue'),
    },
    {
      path: '/tutor/dashboard',
      name: 'panel_tutor',
      component: () => import('../views/PanelTutorView.vue'),
    },
    {
      path: '/admin/dashboard',
      name: 'panel_admin',
      component: () => import('../views/PanelAdminView.vue'),
    },
    {
      path: '/login_departamento/:departamento',
      name: 'LoginDepartamento',
      component: () => import('../views/LoginDepartamentoView.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/departamento/descargas',
      name: 'DepartamentoDescargas',
      component: () => import('../views/DepartamentoDescargasView.vue'),
      meta: { requiresAuth: true, roles: ['psicologia', 'ciencias_basicas', 'jefatura_academica'] },
    },
  ],
})

export default router
