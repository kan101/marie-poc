<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { fetchCalls, type CallSummary } from "../api";
import CallCard from "./CallCard.vue";
import CallFilters from "./CallFilters.vue";

defineProps<{
  selectedId: number | null;
}>();

const emit = defineEmits<{
  select: [id: number];
}>();

const calls = ref<CallSummary[]>([]);
const count = ref(0);
const loading = ref(false);
const search = ref("");
const urgentFilter = ref("");
const callerTypeFilter = ref("");
const page = ref(1);

async function load() {
  loading.value = true;
  // Only include params that have values
  const params: Record<string, string> = { page: page.value.toString() };
  if (search.value) params.search = search.value;
  if (urgentFilter.value) params.urgent = urgentFilter.value;
  if (callerTypeFilter.value) params.caller_type = callerTypeFilter.value;

  const res = await fetchCalls(params);
  calls.value = res.results;
  count.value = res.count;
  loading.value = false;
}

onMounted(load);

// Re-fetch from page 1 whenever filters change
watch([search, urgentFilter, callerTypeFilter], () => {
  page.value = 1;
  load();
});
</script>

<template>
  <div>
    <!-- Toolbar -->
    <CallFilters
      v-model:search="search"
      v-model:callerTypeFilter="callerTypeFilter"
      v-model:urgentFilter="urgentFilter"
    />

    <!-- Cards -->
    <div class="flex flex-col gap-4">
      <CallCard
        v-for="call in calls"
        :key="call.id"
        :call="call"
        :selected="selectedId === call.id"
        @select="emit('select', $event)"
      />
      <div
        v-if="!loading && calls.length === 0"
        class="text-center py-12 text-sm text-gray-400"
      >
        No calls found
      </div>
    </div>

    <!-- Pagination -->
    <div class="flex items-center justify-between mt-4">
      <p class="text-xs text-gray-400">{{ count }} calls total</p>
      <div class="flex gap-2">
        <button
          @click="
            page--;
            load();
          "
          :disabled="page === 1"
          :class="{'cursor-pointer': page !== 1}"
          class="px-3 py-1 text-xs border border-gray-200 rounded-lg disabled:opacity-40 hover:bg-gray-50"
        >
          Previous
        </button>
        <button
          @click="
            page++;
            load();
          "
          :disabled="page * 20 >= count"
          :class="{'cursor-pointer': !(page * 20 >= count)}"
          class="px-3 py-1 text-xs border border-gray-200 rounded-lg disabled:opacity-40 hover:bg-gray-50"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>
