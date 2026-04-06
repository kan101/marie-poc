<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
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

// Each stat card is defined here — adding a new stat only requires a new entry in this array
const statCards = computed(() => {
  if (!stats.value) return []
  return [
    {
      label: 'Total calls',
      value: stats.value.total_calls,
      icon: 'phone',
      bg: 'bg-emerald-50 border-emerald-100',
      iconBg: 'bg-emerald-100',
      iconColor: 'text-emerald-600',
      labelColor: 'text-emerald-400',
      valueColor: 'text-emerald-700',
    },
    {
      label: 'Urgent',
      value: stats.value.urgent,
      icon: 'triangle-exclamation',
      bg: 'bg-red-50 border-red-100',
      iconBg: 'bg-red-100',
      iconColor: 'text-red-500',
      labelColor: 'text-red-400',
      valueColor: 'text-red-600',
    },
    {
      label: 'Email sent',
      value: stats.value.email_sent,
      icon: 'envelope',
      bg: 'bg-blue-50 border-blue-100',
      iconBg: 'bg-blue-100',
      iconColor: 'text-blue-400',
      labelColor: 'text-blue-400',
      valueColor: 'text-blue-400',
    },
    {
      label: 'No action',
      value: stats.value.no_action,
      icon: 'ban',
      bg: 'bg-gray-50 border-gray-200',
      iconBg: 'bg-gray-200',
      iconColor: 'text-gray-400',
      labelColor: 'text-gray-400',
      valueColor: 'text-gray-500',
    },
    {
      label: 'Avg duration',
      value: formatDuration(stats.value.avg_duration_seconds),
      icon: 'clock',
      bg: 'bg-purple-50 border-purple-100',
      iconBg: 'bg-purple-100',
      iconColor: 'text-purple-600',
      labelColor: 'text-purple-400',
      valueColor: 'text-purple-700',
    },
  ]
})
</script>

<template>
  <div class="bg-white px-6 py-4">
    <div
      v-if="stats"
      class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3"
    >
      <div
        v-for="card in statCards"
        :key="card.label"
        :class="['border rounded-xl p-4 flex items-start gap-3', card.bg]"
      >
        <div :class="['w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0', card.iconBg]">
          <font-awesome-icon :icon="card.icon" :class="['text-sm', card.iconColor]" />
        </div>
        <div>
          <p :class="['text-xs mb-0.5', card.labelColor]">{{ card.label }}</p>
          <p :class="['text-2xl font-semibold', card.valueColor]">{{ card.value }}</p>
        </div>
      </div>
    </div>
    <div v-else class="text-sm text-gray-400">Loading...</div>
  </div>
</template>