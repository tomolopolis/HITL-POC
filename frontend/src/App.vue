<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App'
})
</script>

<template>
  <div class="app-container">
    <router-view></router-view>
  </div>
</template>

<style scoped>
.app-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}
</style>