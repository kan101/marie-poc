<script setup lang="ts">
import Dashboard from "./views/Dashboard.vue";
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <header class="bg-gray-900 px-6 py-4 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div
          class="w-8 h-8 bg-white rounded-lg flex items-center justify-center"
        >
          <span class="text-gray-900 text-xs font-bold">M</span>
        </div>
        <div>
          <h1 class="text-sm font-semibold text-white">Marie</h1>
          <p class="text-xs text-gray-400">Legal AI Phone Assistant</p>
        </div>
      </div>
      <div class="flex items-center gap-2 bg-gray-800 px-3 py-1.5 rounded-full">
        <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
        <span class="text-xs text-gray-300">Assistant active</span>
      </div>
    </header>
    <Dashboard />
  </div>
</template>
