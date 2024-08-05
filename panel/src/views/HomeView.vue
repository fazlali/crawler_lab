<script setup>

import {ref} from "vue";

const style = ref({
  background: 'radial-gradient(at center, #3498db, #9b59b6)'
})

function trackMouse(event){
  const x = Math.round(event.pageX / event.target.clientWidth * 100);
  const y = Math.round(event.pageY / event.target.clientWidth * 100);
  style.value.background = `radial-gradient(at ${x}% ${y}%, #3498db, #9b59b6)`
}


</script>

<template>
  <main
      class="radial-gradient absolute top-0 bottom-0 left-0 right-0"
      :style="style"
      @mousemove="trackMouse"
  >
  </main>
</template>

<style>
.radial-gradient {
    z-index: -1;
}
</style>