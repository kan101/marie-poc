<script setup lang="ts">
import { ref, watch } from "vue";
import { fetchCall, updateNotes, type CallDetail } from "../api";

const props = defineProps<{
  callId: number;
}>();

const emit = defineEmits<{
  close: [];
}>();

const call = ref<CallDetail | null>(null);
const notes = ref("");
const saving = ref(false);
const saved = ref(false);

async function load() {
  call.value = null;
  const data = await fetchCall(props.callId);
  call.value = data;
  notes.value = data.notes;
}

watch(() => props.callId, load, { immediate: true });

async function saveNotes() {
  if (!call.value) return;
  saving.value = true;
  await updateNotes(call.value.id, notes.value);
  saving.value = false;
  saved.value = true;
  setTimeout(() => (saved.value = false), 2000);
}

function callerTypeLabel(type: string): string {
  return (
    {
      new_client: "New client",
      existing_client: "Existing client",
      opposing_party: "Opposing party",
      unknown: "Unknown",
    }[type] ?? type
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
  <aside
    class="w-[420px] bg-white border-l border-gray-200 flex flex-col overflow-hidden"
  >
    <!-- Header -->
    <div
      class="flex items-center justify-between px-5 py-4 border-b border-gray-100"
    >
      <h2 class="text-sm font-semibold text-gray-900">Call detail</h2>
      <button
        @click="emit('close')"
        class="text-gray-400 hover:text-gray-600 text-lg leading-none"
      >
        ✕
      </button>
    </div>

    <div
      v-if="!call"
      class="flex-1 flex items-center justify-center text-sm text-gray-400"
    >
      Loading...
    </div>

    <div v-else class="flex-1 overflow-y-auto p-5 flex flex-col gap-5">
      <!-- Caller info -->
      <div>
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-base font-semibold text-gray-900">
            {{ call.caller.full_name }}
          </h3>
        </div>
        <div class="flex flex-col gap-1 text-sm text-gray-500">
          <p>{{ call.caller.phone_number }}</p>
          <p>{{ call.caller.email }}</p>
          <p>
            {{ callerTypeLabel(call.caller_type) }} ·
            {{ formatDate(call.called_at) }} · {{ call.duration_display }}
          </p>
        </div>
      </div>

      <!-- Audio player -->
      <div>
        <p class="text-xs font-medium text-gray-400 mb-2">Recording</p>
        <audio :src="`/media/${call.audio_file}`" controls class="w-full" />
      </div>

      <!-- Summary -->
      <div v-if="call.summary">
        <p class="text-xs font-medium text-gray-400 mb-2">Summary</p>
        <p class="text-sm text-gray-700 leading-relaxed">{{ call.summary }}</p>
      </div>

      <!-- Transcript -->
      <div v-if="call.transcript">
        <p class="text-xs font-medium text-gray-400 mb-2">Transcript</p>
        <p class="text-sm text-gray-600 leading-relaxed whitespace-pre-wrap">
          {{ call.transcript }}
        </p>
      </div>

      <!-- Notes -->
      <div>
        <p class="text-xs font-medium text-gray-400 mb-2">Notes</p>
        <textarea
          v-model="notes"
          rows="4"
          placeholder="Add notes about this call..."
          class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900 resize-none"
        />
        <div class="flex items-center justify-between mt-2">
          <span v-if="saved" class="text-xs text-green-600">Saved</span>
          <span v-else class="text-xs text-gray-400"></span>
          <button
            @click="saveNotes"
            :disabled="saving"
            class="px-3 py-1.5 bg-gray-900 text-white text-xs rounded-lg hover:bg-gray-700 disabled:opacity-40"
          >
            {{ saving ? "Saving..." : "Save notes" }}
          </button>
        </div>
      </div>
    </div>
  </aside>
</template>
