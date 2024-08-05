<script setup>
import { RouterLink, RouterView } from 'vue-router'
import {ref} from "vue";
import {pendingRequests} from "@/service.js";


const hiddenMenu = ref(true)

const menuItems = ref([
  {route: {name: 'home'}, title: 'Home' },
  {route: {name: 'websites.new'}, title: 'New Website' },
  {route: {name: 'websites.index'}, title: 'All Websites' }
])

</script>

<template>
  <header>
    <div class="wrapper">
      <nav class="bg-blue-500 p-6 shadow-lg" :class="{'bg-red-500': pendingRequests}">
        <div class="container mx-auto flex justify-between items-center">
          <a href="#" class="text-white font-extrabold text-xl">Deed Crawler Lab</a>
          <div class="hidden md:flex space-x-6">
            <router-link
                :to="item.route" v-for="item in menuItems"
                class="block text-white hover:text-gray-200 transition duration-300 py-2"
                :key="item.route"
            >{{ item.title }}</router-link>
          </div>
          <button class="md:hidden text-white" @click="hiddenMenu = !hiddenMenu">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
          </button>
        </div>
        <div class="md:hidden" :class="{hidden: hiddenMenu}">
          <router-link
              :to="item.route" v-for="item in menuItems"
              class="block text-white hover:text-gray-200 transition duration-300 py-2"
              :key="item.route"
          >{{ item.title }}</router-link>
        </div>
      </nav>
    </div>
  </header>

  <suspense>
    <RouterView />
  </suspense>
</template>

<style scoped></style>
