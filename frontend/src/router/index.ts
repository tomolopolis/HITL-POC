import { createRouter, createWebHistory } from 'vue-router'
import ProjectList from '../components/ProjectList.vue'
import TextAnnotation from '../components/TextAnnotation.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/home',
      name: 'home',
      component: ProjectList
    },
    {
      path: '/annotations/:projectId',
      name: 'annotations',
      component: TextAnnotation,
      props: route => ({ projectId: Number(route.params.projectId) })
    }
  ]
})

export default router