<script setup>
import {ref, watch} from "vue";
import JsonEditor from "@/components/JsonEditor.vue";
import * as api from "@/service.js";
import Product from "@/components/Product.vue";


const props = defineProps({
  website: {
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
  },
  test: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['save'])
const website = ref(props.website)

watch(() => props.website, (value) => {
  website.value = value
})

const scrapeTestResult = ref({
  status_code: 0,
  title: '',
  price: 0,
  selling_price: 0,
  image_urls: [],
  description: '',
  brand: '',
  currency: ''
})

const scrapeTestUrl = ref('')

const extractTestResult = ref([])

async function save() {
  const result = await api.saveWebsite(website.value.domain, website.value)
  emit('save', {website: result.website})
}

async function extract() {
  extractTestResult.value = []
  const result = await api.extract(website.value.extract.start_urls, website.value.extract.config)
  extractTestResult.value = result.product_urls
}

async function scrape() {
  scrapeTestResult.value = {}
  const result = await api.scrape([scrapeTestUrl.value], website.value.scrape.selectors)
  if (result.products.length){
    scrapeTestResult.value = result.products[0]
  } else {
    alert('Error while scraping product info')
  }
}

async function scrapeTest(url) {
  scrapeTestUrl.value = url
  await scrape()
}




</script>

<template>
  <main class="mt-3">
    <form  @submit.prevent="save">
      <div class="container mx-auto p-3">
        <div class="grid grid-cols-[1fr_auto] gap-2">
          <div class="mb-3">
            <input
                class="block w-full rounded-md border-0 py-1.5 px-7 text-gray-900 ring-1 ring-inset ring-gray-300 invalid:ring-red-400"
                type="text"
                v-model="website.domain" placeholder="Domain" pattern="^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$"
                required
            >
          </div>
          <div class="">
            <button type="submit" class="bg-blue-500 text-white py-1 px-2 rounded hover:bg-blue-700">Save</button>
          </div>
        </div>
        <div class="grid md:grid-cols-2 gap-6">
          <div>
            <h2>Extract</h2>
            <label>Start urls</label>
            <json-editor
                :main-menu-bar="false"
                :navigation-bar="false"
                :content="{json: website.extract.start_urls}"
                :on-change="({json}) => website.extract.start_urls = json"
            />
            <label>Config</label>
            <json-editor
                class="mb-2"
                :main-menu-bar="false"
                :navigation-bar="false"
                :content="{json: website.extract.config}"
                :on-change="({json}) => website.extract.config = json"
            />
            <template v-if="test">
              <div class="mb-2">
                <button @click.prevent="extract" class="w-full bg-blue-500 text-white py-1 px-2 rounded hover:bg-blue-700">Test</button>
              </div>
              <div class="mb-2 overflow-auto max-h-[100vh]">
                <table class="table-auto bg-white w-full">
                  <thead>
                  <tr>
                    <th class="py-2 px-4 border-b">#</th>
                    <th class="py-2 px-4 border-b">Product Url</th>
                    <th class="py-2 px-4 border-b">Test</th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr v-for="(url, index) in extractTestResult" :key="index">
                    <td class="py-2 px-4 border-b">
                      {{ index + 1}}
                    </td>
                    <td class="py-2 px-4 border-b">
                      <a :href="url" target="_blank" class="text-blue-500 hover:underline">{{ url }}</a>
                    </td>
                    <td class="py-2 px-4 border-b">
                      <button @click.prevent="scrapeTest(url)" class="bg-blue-500 text-white py-1 px-2 rounded hover:bg-blue-700">Test</button>
                    </td>
                  </tr>
                  </tbody>
                </table>
              </div>
            </template>
          </div>
          <div>
            <h2>Scrape</h2>
            <label>Selectors</label>
            <json-editor
                class="mb-3"
                :main-menu-bar="false"
                :navigation-bar="false"
                :content="{json: website.scrape.selectors}"
                :on-change="({json}) => website.scrape.selectors = json"
            />
            <template v-if="test">
              <div class="grid grid-cols-[1fr_auto] gap-2 mb-3">
                <div>
                  <input
                      class="block w-full rounded-md border-0 py-1.5 px-7 text-gray-900 ring-1 ring-inset ring-gray-300"
                      type="text"
                      v-model="scrapeTestUrl"
                  >
                </div>
                <div>
                  <button @click.prevent="scrape" class="bg-blue-500 text-white py-1 px-2 rounded hover:bg-blue-700">Test</button>
                </div>
              </div>
              <product v-if="scrapeTestResult.status_code" :product="scrapeTestResult"/>
            </template>
          </div>
        </div>
      </div>
    </form>
  </main>
</template>
