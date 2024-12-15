import ImportantView from '../views/ImportantView.vue'
import TransmissionsView from '../views/TransmissionView.vue'
import BodysView from '../views/BodysView.vue'
import EnginesView from '../views/EnginesView.vue'
import DrivesView from '../views/DrivesView.vue'
import CarsView from '../views/CarsView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/", 
      name: "CarsView",
      component: CarsView
    },
    {
      path: "/drives", 
      name: "DrivesView",
      component: DrivesView
    },
    {
      path: "/engines", 
      name: "EnginesView",
      component: EnginesView
    },
    {
      path: "/bodys", 
      name: "BodysView",
      component: BodysView
    },
    {
      path: "/Transmissions", 
      name: "TransmissionsView",
      component: TransmissionsView
    },
    {
      path: "/important", 
      name: "ImportantView",
      component: ImportantView
    },
    {
      path: "/users",
      name: "LoginView",
      component: Login,
    }
    // {
    //   path: '/login',
    //   name: 'login',
    //   component: Login
    // }
    
  ]
})

export default router
