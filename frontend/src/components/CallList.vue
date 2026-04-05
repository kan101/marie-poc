<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { fetchCalls, type CallSummary } from "../api";

const props = defineProps<{
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
const page = ref(1);

async function load() {
  loading.value = true;
  const params: Record<string, string> = { page: page.value.toString() };
  if (search.value) params.search = search.value;
  if (urgentFilter.value) params.urgent = urgentFilter.value;
  const res = await fetchCalls(params);
  calls.value = res.results;
  count.value = res.count;
  loading.value = false;
}

onMounted(load);
watch([search, urgentFilter], () => {
  page.value = 1;
  load();
});

function callerTypeLabel(type: string): string {
  return (
    (
      {
        new_client: "New client",
        existing_client: "Existing client",
        opposing_party: "Opposing party",
        unknown: "Unknown",
      } as Record<string, string>
    )[type] ?? type
  );
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}
</script>

<template>
  <div>
    <!-- Toolbar -->
    <div class="flex items-center gap-3 mb-4 flex-wrap">
      <input
        v-model="search"
        type="text"
        placeholder="Search by name, email, phone..."
        class="flex-1 min-w-[200px] border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900"
      />
      <select
        v-model="urgentFilter"
        class="border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900"
      >
        <option value="">All calls</option>
        <option value="true">Urgent only</option>
      </select>
    </div>

    <!-- Table -->
    <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm min-w-[640px]">
          <thead>
            <tr class="border-b border-gray-100 text-left">
              <th class="px-4 py-3 text-xs font-medium text-gray-400">
                Caller
              </th>
              <th class="px-4 py-3 text-xs font-medium text-gray-400">Type</th>
              <th class="px-4 py-3 text-xs font-medium text-gray-400">Phone</th>
              <th class="px-4 py-3 text-xs font-medium text-gray-400">
                Date & time
              </th>
              <th class="px-4 py-3 text-xs font-medium text-gray-400">
                Duration
              </th>
              <th class="px-4 py-3 text-xs font-medium text-gray-400">
                Action
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="call in calls"
              :key="call.id"
              @click="emit('select', call.id)"
              :class="[
                'border-b border-gray-50 cursor-pointer transition-colors hover:bg-gray-50',
                selectedId === call.id ? 'bg-gray-50' : '',
                call.urgent ? 'border-l-2 border-l-red-400' : '',
              ]"
            >
              <td class="px-4 py-3 font-medium text-gray-900">
                <div class="flex items-center gap-2">
                  <span
                    v-if="call.urgent"
                    class="w-2 h-2 rounded-full bg-red-500 flex-shrink-0"
                  ></span>
                  {{ call.caller.full_name }}
                </div>
              </td>
              <td class="px-4 py-3 text-gray-500">
                {{ callerTypeLabel(call.caller_type) }}
              </td>
              <td class="px-4 py-3 text-gray-500">
                {{ call.caller.phone_number }}
              </td>
              <td class="px-4 py-3 text-gray-500">
                {{ formatDate(call.called_at) }}
              </td>
              <td class="px-4 py-3 text-gray-500">
                {{ call.duration_display }}
              </td>
              <td class="px-4 py-3">
                <div class="flex flex-col gap-1">
                  <span
                    v-if="call.urgent"
                    class="px-5 py-2 rounded-full text-xs font-medium bg-red-100 text-red-700 w-fit"
                  >
                    Urgent
                  </span>
                  <span
                    v-if="call.follow_up_sent"
                    class="px-5 py-2 rounded-full text-xs font-medium bg-blue-100 text-blue-700 w-fit"
                  >
                    Email sent
                  </span>
                  <span
                    v-else
                    class="px-5 py-2 rounded-full text-xs font-medium bg-gray-100 text-gray-500 w-fit"
                  >
                    No action
                  </span>
                </div>
              </td>
            </tr>
            <tr v-if="!loading && calls.length === 0">
              <td colspan="7" class="px-4 py-8 text-center text-gray-400">
                No calls found
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div
        class="flex items-center justify-between px-4 py-3 border-t border-gray-100"
      >
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
  </div>
</template>
