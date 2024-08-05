<script setup>
import {ref} from "vue";
import EditWebsite from "@/components/EditWebsite.vue";
import {useRouter} from "vue-router";

const router = useRouter()

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

async function gotoEdit({website: w}) {
  await router.push({name: 'websites.edit', params: {domain: w.domain}})
}

</script>

<template>
  <main class="mt-3">
    <edit-website :website="website" @save="gotoEdit"/>
  </main>
</template>
