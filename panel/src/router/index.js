import { createRouter, createWebHistory } from 'vue-router'
import NewWebsiteView from '../views/NewWebsiteView.vue'
import EditWebsiteView from "@/views/EditWebsiteView.vue";
import AllWebsiteView from "@/views/AllWebsiteView.vue";
import CheckWebsiteView from "@/views/CheckWebsiteView.vue";
import HomeView from "@/views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/websites',
      name: 'websites.index',
      component: AllWebsiteView
    },
    {
      path: '/websites/new',
      name: 'websites.new',
      component: NewWebsiteView
    },
    {
      path: '/websites/:domain',
      name: 'websites.edit',
      component: EditWebsiteView
    },
    {
      path: '/websites/:domain/check',
      name: 'websites.check',
      component: CheckWebsiteView
    }
  ]
})

export default router
