<script setup>
import Slider from "@/components/Slider.vue";

const props = defineProps({
  product: {
    required: true,
    type: {
      title: '',
      price: 0,
      selling_price: 0,
      image_urls: [],
      description: '',
      brand: '',
      currency: '',
      scrape_url: ''

    }
  }
})
</script>

<template>
  <div class="product outline outline-3 outline-indigo-300 rounded p-2 bg-indigo-100" dir="rtl">
    <div class="mb-3">
      <slider v-if="product.image_urls" :images="product.image_urls"/>
      <span v-else class="text-gray-500">No images</span>
    </div>
    <div class="title mb-2" title="Title">
      <a :href="product.scrape_url" target="_blank">
        <h2 v-if="product.title" class="text-2xl">{{ product.title }}</h2>
        <h2 v-else class="text-2xl text-gray-500">No title</h2>
      </a>
    </div>
    <div class="description mb-2" title="Description">
      <p v-if="product.description">{{ product.description }}</p>
      <p v-else class="text-gray-500">No Description</p>
    </div>
    <div class="price" title="Price">
      <span v-if="product.selling_price" class="me-2">{{ product.selling_price }}</span>
      <span class="me-2" :class="{'line-through text-red-700': product.selling_price }">{{ product.price }}</span>
      <span>{{ product.currency }}</span>
    </div>
  </div>
</template>

<style scoped>

</style>