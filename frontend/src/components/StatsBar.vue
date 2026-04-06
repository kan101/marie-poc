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
  <div class="bg-white px-6 py-4">
    <div
      v-if="stats"
      class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3"
    >
     <!-- Total calls -->
<div
  class="bg-orange-50 border border-orange-100 rounded-xl p-4 flex items-start gap-3"
>
  <div
    class="w-9 h-9 rounded-lg bg-orange-100 flex items-center justify-center flex-shrink-0"
  >
    <font-awesome-icon icon="phone" class="text-orange-600 text-sm" />
  </div>
  <div>
    <p class="text-xs text-orange-400 mb-0.5">Total calls</p>
    <p class="text-2xl font-semibold text-orange-700">
      {{ stats.total_calls }}
    </p>
  </div>
</div>

      <!-- Urgent -->
      <div
        class="bg-red-50 border border-red-100 rounded-xl p-4 flex items-start gap-3"
      >
        <div
          class="w-9 h-9 rounded-lg bg-red-100 flex items-center justify-center flex-shrink-0"
        >
          <font-awesome-icon
            icon="triangle-exclamation"
            class="text-red-500 text-sm"
          />
        </div>
        <div>
          <p class="text-xs text-red-400 mb-0.5">Urgent</p>
          <p class="text-2xl font-semibold text-red-600">{{ stats.urgent }}</p>
        </div>
      </div>

      <!-- Email sent -->
      <div
        class="bg-blue-50 border border-blue-100 rounded-xl p-4 flex items-start gap-3"
      >
        <div
          class="w-9 h-9 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0"
        >
          <font-awesome-icon icon="envelope" class="text-blue-500 text-sm" />
        </div>
        <div>
          <p class="text-xs text-blue-400 mb-0.5">Email sent</p>
          <p class="text-2xl font-semibold text-blue-600">
            {{ stats.email_sent }}
          </p>
        </div>
      </div>

      <!-- No action -->
      <div
        class="bg-gray-50 border border-gray-200 rounded-xl p-4 flex items-start gap-3"
      >
        <div
          class="w-9 h-9 rounded-lg bg-gray-200 flex items-center justify-center flex-shrink-0"
        >
          <font-awesome-icon icon="ban" class="text-gray-400 text-sm" />
        </div>
        <div>
          <p class="text-xs text-gray-400 mb-0.5">No action</p>
          <p class="text-2xl font-semibold text-gray-500">
            {{ stats.no_action }}
          </p>
        </div>
      </div>

      <!-- Avg duration -->
      <div
        class="bg-purple-50 border border-purple-100 rounded-xl p-4 flex items-start gap-3"
      >
        <div
          class="w-9 h-9 rounded-lg bg-purple-100 flex items-center justify-center flex-shrink-0"
        >
          <font-awesome-icon icon="clock" class="text-purple-600 text-sm" />
        </div>
        <div>
          <p class="text-xs text-purple-400 mb-0.5">Avg duration</p>
          <p class="text-2xl font-semibold text-purple-700">
            {{ formatDuration(stats.avg_duration_seconds) }}
          </p>
        </div>
      </div>
    </div>
    <div v-else class="text-sm text-gray-400">Loading...</div>
  </div>
</template>
