<script setup>
import {ref} from "vue";

const props = defineProps({
  images: {
    required: true,
    type: Array
  }
})

const currentIndex = ref(0)


</script>

<template>
  <div class="relative" dir="ltr">
    <div class="overflow-hidden">
      <div class="flex transition-transform duration-500" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
        <div v-for="(image, index) in images" :key="index" class="flex-none w-full">
          <img :src="image" class="w-full h-auto min-h-[100px] bg-indigo-50" loading="lazy" @click="e => e.target.src = image + '?' + Date.now()">
        </div>
      </div>
    </div>
    <div class="absolute bottom-1.5 left-1/2 transform -translate-x-1/2 flex space-x-1 px-2 py-1 bg-indigo-50 rounded-full">
      <button
          v-for="(_, index) in images"
          :key="index"
          :class="{'bg-indigo-700': currentIndex === index, 'bg-indigo-300': currentIndex !== index}"
          class="w-3 h-3 rounded-full"
          @click.prevent="currentIndex = index"
      ></button>
    </div>
  </div>
</template>

<style scoped>

</style>