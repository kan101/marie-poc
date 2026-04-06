<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { fetchCalls, type CallSummary } from "../api";
import CallCard from "./CallCard.vue";

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
watch([search, urgentFilter, callerTypeFilter], () => {
  page.value = 1;
  load();
});

</script>

<template>
  <div>
    <!-- Toolbar -->
    <div class="flex items-center gap-3 mb-4 flex-wrap">
      <div class="relative flex-1 min-w-[200px]">
        <font-awesome-icon
          icon="phone"
          class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-xs"
        />
        <input
          v-model="search"
          type="text"
          placeholder="Search by name, email, phone..."
          class="w-full pl-8 pr-3 py-3 bg-[#f5f5f5] rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-900"
        />
      </div>
      <select
        v-model="callerTypeFilter"
        class="border border-gray-200 rounded-lg px-3 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900"
      >
        <option value="">All types</option>
        <option value="new_client">New client</option>
        <option value="existing_client">Existing client</option>
        <option value="opposing_party">Opposing party</option>
      </select>
      <select
        v-model="urgentFilter"
        class="border border-gray-200 rounded-lg px-3 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900"
      >
        <option value="">All calls</option>
        <option value="true">Urgent only</option>
      </select>
    </div>

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
          class="px-3 py-1 text-xs border border-gray-200 rounded-lg disabled:opacity-40 hover:bg-gray-50"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>
