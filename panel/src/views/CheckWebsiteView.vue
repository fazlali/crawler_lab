<script setup async>
import {ref} from "vue";
import EditWebsite from "@/components/EditWebsite.vue";
import * as api from "@/service.js";
import {useRoute} from "vue-router";
import Slider from "@/components/Slider.vue";

const route = useRoute()

const website = ref({
  domain: '',
  extract: {
    start_urls: [],
    config: {
      spider: '',
      crawl_allow: [],
      crawl_deny: [],
      product_allow: [],
      product_deny: [],
    }
  },
  scrape: {
    selectors: {
      value: {
        currency: []
      },
      xpath: {
        title: [],
        price: [],
        selling_price: [],
        image_urls: [],
        description: [],
        brand: []
      }
    }
  }
})

const messages = ref([])
const products = ref([])
const showWebsiteDetails = ref(true)
const maxProductCount = ref('')

const result = await api.loadWebsite(route.params.domain)
website.value = result.website

async function startCrawling() {
  products.value = []
  const {product_urls} = await api.extract(website.value.extract.start_urls, website.value.extract.config)
  const sample_urls = product_urls.map(a => [a,Math.random()])
      .sort((a,b) => {return a[1] < b[1] ? -1 : 1;})
      .slice(0, maxProductCount.value)
      .map(a => a[0])
  const response = await api.scrape(sample_urls, website.value.scrape.selectors)
  products.value = response.products
}


</script>

<template>
  <main class="mt-3">
    <div class="container m-auto">
      <div v-if="messages.length" class="flex p-4 mb-4 text-sm text-blue-800 rounded-lg bg-blue-50 dark:bg-gray-800 dark:text-blue-400" role="alert">
        <svg class="flex-shrink-0 inline w-4 h-4 me-3 mt-[2px]" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
          <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
        </svg>
        <span class="sr-only">Info</span>
        <div>
          <span class="font-medium">Crawling website <span class="font-bold uppercase">{{ website.domain }}</span>:</span>
          <ul class="mt-1.5 list-disc list-inside">
            <li v-for="message in messages" :key="message">{{ message }}</li>
          </ul>
        </div>
      </div>
      <div class="p-2 bg-indigo-100 rounded mb-2">
        <div class="grid grid-cols-[auto_1fr_auto] px-3">
          <span class="me-2 uppercase">{{ website.domain }}</span>
          <span class="border-b border-black w-full h-0 p-1.5"></span>
          <span class="ms-1 cursor-pointer" @click="showWebsiteDetails = !showWebsiteDetails">{{ showWebsiteDetails ? '▼' : '▲' }}</span>
        </div>
        <edit-website v-if="showWebsiteDetails" :website="website" @save="({website: updated}) => website = updated" :test="false"/>
      </div>
      <div class="p-2 bg-indigo-100 rounded mb-2">
        <form class="grid grid-cols-[1fr_auto] gap-2" @submit.prevent="startCrawling">
          <div class="mb-3">
            <input
                class="block w-full rounded-md border-0 py-1.5 px-7 text-gray-900 ring-1 ring-inset ring-gray-300 invalid:ring-red-400"
                type="number"
                v-model="maxProductCount" placeholder="Max product Count"
                required
            >
          </div>
          <div class="">
            <button type="submit" class="bg-blue-500 text-white py-1 px-2 rounded hover:bg-blue-700">Start Crawling</button>
          </div>
        </form>
        <table class="table-auto bg-white w-full text-left">
          <thead>
          <tr>
            <th class="py-2 px-4 border-b">#</th>
            <th class="py-2 px-4 border-b">Title</th>
            <th class="py-2 px-4 border-b">Description</th>
            <th class="py-2 px-4 border-b">Price/Currency</th>
            <th class="py-2 px-4 border-b">Images</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(product, index) in products" :key="product.scrape_url">
            <td class="py-2 px-4 border-b">
              {{ index + 1 }}
            </td>
            <td class="py-2 px-4 border-b">
              <a :href="product.scrape_url" target="_blank">
                <h2 v-if="product.title" class="text-2xl">{{ product.title }}</h2>
                <h2 v-else class="text-2xl text-gray-500">No title</h2>
              </a>
            </td>
            <td class="py-2 px-4 border-b">
              <p v-if="product.description">{{ product.description }}</p>
              <p v-else class="text-gray-500">No Description</p>
            </td>
            <td class="py-2 px-4 border-b">
              <span v-if="product.selling_price" class="me-2">{{ product.selling_price }}</span>
              <span class="me-2" :class="{'line-through text-red-700': product.selling_price }">{{ product.price }}</span>
              <span>{{ product.currency }}</span>
            </td>
            <td class="py-2 px-4 border-b">
              <slider class="max-w-[200px]" v-if="product.image_urls" :images="product.image_urls"/>
              <span v-else class="text-gray-500">No images</span>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </main>
</template>
