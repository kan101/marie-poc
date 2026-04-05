<script setup lang="ts">
import { ref } from 'vue'
import StatsBar from '../components/StatsBar.vue'
import CallList from '../components/CallList.vue'
import CallDetail from '../components/CallDetail.vue'

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
    <div class="flex flex-1 overflow-hidden relative">
      <main :class="['flex-1 overflow-y-auto p-4 md:p-6', selectedCallId ? 'hidden md:block' : '']">
        <CallList @select="onCallSelected" :selected-id="selectedCallId" />
      </main>
      <CallDetail
        v-if="selectedCallId"
        :call-id="selectedCallId"
        @close="onClose"
        class="absolute inset-0 md:relative md:inset-auto md:w-[420px]"
      />
    </div>
  </div>
</template>