<script setup async>
import {ref} from "vue";
import {loadWebsites} from "@/service.js";

const websites = ref([])

const result = await loadWebsites()
websites.value = result.websites

</script>

<template>
  <main class="mt-3">
    <div class="container m-auto">
      <table class="w-full table-auto bg-white table-auto text-left">
        <thead>
        <tr>
          <th class="py-2 px-4 border-b">#</th>
          <th class="py-2 px-4 border-b">Domain</th>
          <th class="py-2 px-4 border-b">Actions</th>
        </tr>
        </thead>
        <tr v-for="(domain, index) in websites">
          <td class="py-2 px-4 border-b">{{index + 1}}</td>
          <td class="py-2 px-4 border-b">
            <a :href="'http://' + domain" target="_blank">{{domain}}</a>
          </td>
          <td class="py-2 px-4 border-b">
            <router-link class="me-2 bg-blue-500 text-white py-1 px-2 rounded hover:bg-blue-700" :to="{name: 'websites.edit', params: {domain}}">Edit</router-link>
            <router-link class="bg-blue-500 text-white py-1 px-2 rounded hover:bg-blue-700" :to="{name: 'websites.check', params: {domain}}">Check</router-link>
          </td>
        </tr>
      </table>
    </div>

  </main>
</template>
