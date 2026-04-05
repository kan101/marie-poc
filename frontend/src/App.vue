<script setup lang="ts">
import Dashboard from './views/Dashboard.vue'
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <header class="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-gray-900 rounded-lg flex items-center justify-center">
          <span class="text-white text-xs font-bold">M</span>
        </div>
        <div>
          <h1 class="text-sm font-semibold text-gray-900">Marie</h1>
          <p class="text-xs text-gray-400">Legal AI Phone Assistant</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-2 h-2 bg-green-400 rounded-full"></div>
        <span class="text-xs text-gray-500">Assistant active</span>
      </div>
    </header>
    <Dashboard />
  </div>
</template>