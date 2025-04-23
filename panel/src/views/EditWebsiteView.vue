<script setup async>
import {ref} from "vue";
import EditWebsite from "@/components/EditWebsite.vue";
import * as api from "@/service.js";
import {useRoute} from "vue-router";

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
        brand: [],
        out_of_stock: []
      }
    }
  }
})

const result = await api.loadWebsite(route.params.domain)
website.value = result.website

</script>

<template>
  <main class="mt-3">
    <edit-website v-if="website.domain" :website="website"/>
    <div v-else class="text-center">No Website</div>
  </main>
</template>
