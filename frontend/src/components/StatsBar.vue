<script setup lang="ts">
import { ref, onMounted } from "vue";
import { fetchStats, type Stats } from "../api";

const stats = ref<Stats | null>(null);

onMounted(async () => {
  stats.value = await fetchStats();
});

function formatDuration(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${s.toString().padStart(2, "0")}`;
}
</script>

<template>
  <div class="bg-white border-b border-gray-200 px-6 py-4">
    <div v-if="stats" class="flex flex-wrap gap-4 md:gap-8">
      <div>
        <p class="text-xs text-gray-400 mb-1">Total calls</p>
        <p class="text-2xl font-semibold text-gray-900">
          {{ stats.total_calls }}
        </p>
      </div>
      <div>
        <p class="text-xs text-gray-400 mb-1">Urgent</p>
        <p class="text-2xl font-semibold text-red-500">{{ stats.urgent }}</p>
      </div>
      <div>
        <p class="text-xs text-gray-400 mb-1">Email sent</p>
        <p class="text-2xl font-semibold text-blue-500">
          {{ stats.email_sent }}
        </p>
      </div>
      <div>
        <p class="text-xs text-gray-400 mb-1">No action</p>
        <p class="text-2xl font-semibold text-gray-400">
          {{ stats.no_action }}
        </p>
      </div>
      <div>
        <p class="text-xs text-gray-400 mb-1">Avg duration</p>
        <p class="text-2xl font-semibold text-gray-900">
          {{ formatDuration(stats.avg_duration_seconds) }}
        </p>
      </div>
    </div>
    <div v-else class="text-sm text-gray-400">Loading...</div>
  </div>
</template>
