<script setup lang="ts">
import { ref } from 'vue'
import StatsBar from '../components/StatsBar.vue'
import CallList from '../components/CallList.vue'
import CallDetailModal from '../components/CallDetailModal.vue'

const selectedCallId = ref<number | null>(null)

function onCallSelected(id: number) {
  selectedCallId.value = id
}

function onClose() {
  selectedCallId.value = null
}
</script>

<template>
  <div class="flex flex-col flex-1 overflow-hidden">
    <StatsBar />
    <main class="flex-1 overflow-y-auto p-6">
      <CallList @select="onCallSelected" :selected-id="selectedCallId" />
    </main>
    <CallDetailModal
      v-if="selectedCallId"
      :call-id="selectedCallId"
      @close="onClose"
    />
  </div>
</template>