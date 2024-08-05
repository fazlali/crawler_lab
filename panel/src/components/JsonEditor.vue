<template>
  <form @submit.prevent.stop>
    <div dir="ltr" class="svelte-jsoneditor-vue" ref="el"/>
  </form>
</template>

<script setup lang="ts">
import { JSONEditor } from "vanilla-jsoneditor";
import {onBeforeUnmount, onMounted, onUpdated, ref, defineProps, computed} from "vue";

const props =defineProps([
  "content",
  "mode",
  "mainMenuBar",
  "navigationBar",
  "statusBar",
  "readOnly",
  "indentation",
  "tabSize",
  "escapeControlCharacters",
  "escapeUnicodeCharacters",
  "validator",
  "onError",
  "onChange",
  "onChangeMode",
  "onClassName",
  "onRenderValue",
  "onRenderMenu",
  "queryLanguages",
  "queryLanguageId",
  "onChangeQueryLanguage",
  "onFocus",
  "onBlur",
]);

const safeProps = computed(() => {
  return Object.fromEntries(Object.entries(props).filter(([,value]) => value !== undefined))
})

const el = ref()
const editor = ref()

onMounted(() => {

  editor.value = new JSONEditor({
    target: el.value,
    props: safeProps.value,
  });
  console.log("create editor", editor.value);
})

onUpdated(() =>{
  editor.value.updateProps(safeProps.value);
})

onBeforeUnmount(() => {
  console.log("destroy editor");
  editor.value.destroy();
  editor.value = null;
})


</script>

<style scoped>
.svelte-jsoneditor-vue {
  display: flex;
  flex: 1;
}
</style>