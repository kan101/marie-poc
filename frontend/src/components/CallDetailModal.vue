<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { fetchCall, updateNotes, type CallDetail } from '../api'

const props = defineProps<{
  callId: number | null
}>()

const emit = defineEmits<{
  close: []
}>()

const call = ref<CallDetail | null>(null)
const notes = ref('')
const saving = ref(false)
const saved = ref(false)

watch(() => props.callId, async (id) => {
  if (!id) return
  call.value = null
  const data = await fetchCall(id)
  call.value = data
  notes.value = data.notes
}, { immediate: true })

async function saveNotes() {
  if (!call.value) return
  saving.value = true
  await updateNotes(call.value.id, notes.value)
  saving.value = false
  saved.value = true
  setTimeout(() => saved.value = false, 2000)
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') emit('close')
}

onMounted(() => {
  document.addEventListener('keydown', onKeydown)
  document.body.style.overflow = 'hidden'
})

onUnmounted(() => {
  document.removeEventListener('keydown', onKeydown)
  document.body.style.overflow = ''
})

function callerTypeLabel(type: string): string {
  return ({
    new_client: 'New client',
    existing_client: 'Existing client',
    opposing_party: 'Opposing party',
    unknown: 'Unknown',
  } as Record<string, string>)[type] ?? type
}

function callerTypeBadgeClass(type: string): string {
  return ({
    new_client: 'bg-emerald-100 text-emerald-800 ring-1 ring-emerald-200',
    existing_client: 'bg-blue-100 text-blue-800 ring-1 ring-blue-200',
    opposing_party: 'bg-orange-100 text-orange-800 ring-1 ring-orange-200',
    unknown: 'bg-gray-100 text-gray-500 ring-1 ring-gray-200',
  } as Record<string, string>)[type] ?? 'bg-gray-100 text-gray-400'
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function initials(name: string): string {
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}
</script>

<template>
    <div
      class="fixed inset-0 z-50 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
    >
      <!-- Overlay -->
      <div
        class="absolute inset-0 bg-black/50 backdrop-blur-sm"
        @click="emit('close')"
      />

      <!-- Modal -->
      <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] flex flex-col overflow-hidden z-10">

        <!-- Loading -->
        <div v-if="!call" class="flex items-center justify-center py-20">
          <div class="w-6 h-6 border-2 border-gray-300 border-t-gray-900 rounded-full animate-spin" />
        </div>

        <template v-else>
          <!-- Header -->
          <div class="px-6 py-5 border-b border-gray-100 flex items-start justify-between gap-4 flex-shrink-0">
            <div class="flex items-center gap-3">
              <div class="w-11 h-11 rounded-full bg-gray-200 flex items-center justify-center text-sm font-extrabold text-gray-700 flex-shrink-0">
                {{ initials(call.caller.full_name) }}
              </div>
              <div>
                <div class="flex items-center gap-2 flex-wrap">
                  <h2 class="text-base font-bold text-gray-900">{{ call.caller.full_name }}</h2>
                  <span :class="['inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium', callerTypeBadgeClass(call.caller_type)]">
                    {{ callerTypeLabel(call.caller_type) }}
                  </span>
                </div>
                <div class="flex items-center gap-3 text-xs text-gray-400 mt-1 flex-wrap">
                  <span class="flex items-center gap-1">
                    <font-awesome-icon icon="phone" class="text-[10px]" />
                    {{ call.caller.phone_number }}
                  </span>
                  <span v-if="call.caller.email" class="flex items-center gap-1">
                    <font-awesome-icon icon="envelope" class="text-[10px]" />
                    {{ call.caller.email }}
                  </span>
                  <span class="flex items-center gap-1">
                    <font-awesome-icon icon="clock" class="text-[10px]" />
                    {{ formatDate(call.called_at) }} · {{ call.duration_display }}
                  </span>
                </div>
              </div>
            </div>
            <button
              @click="emit('close')"
              class="text-gray-400 hover:text-gray-600 transition-colors p-1.5 rounded-lg hover:bg-gray-100 flex-shrink-0"
            >
              <font-awesome-icon icon="xmark" />
            </button>
          </div>

          <!-- Scrollable body -->
          <div class="flex-1 overflow-y-auto px-6 py-5 flex flex-col gap-5">

            <!-- Urgency reason -->
            <div v-if="call.urgent && call.urgent_reason" class="bg-red-50 border border-red-200 rounded-xl p-4 flex gap-3">
              <font-awesome-icon icon="triangle-exclamation" class="text-red-500 mt-0.5 flex-shrink-0" />
              <div>
                <p class="text-xs font-semibold text-red-700 mb-0.5">Urgent — callback required</p>
                <p class="text-xs text-red-600 leading-relaxed">{{ call.urgent_reason }}</p>
              </div>
            </div>

            <!-- Audio -->
            <div>
              <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Recording</p>
              <audio :src="`/media/${call.audio_file}`" controls class="w-full" />
            </div>

            <!-- Summary -->
            <div v-if="call.summary">
              <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Summary</p>
              <p class="text-sm text-gray-700 leading-relaxed bg-gray-50 rounded-xl p-4">{{ call.summary }}</p>
            </div>

            <!-- Transcript -->
            <div v-if="call.transcript">
              <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Transcript</p>
              <div class="bg-gray-50 rounded-xl p-4 max-h-48 overflow-y-auto">
                <p class="text-sm text-gray-600 leading-relaxed whitespace-pre-wrap">{{ call.transcript }}</p>
              </div>
            </div>

            <!-- Notes -->
            <div>
              <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Notes</p>
              <textarea
                v-model="notes"
                rows="4"
                placeholder="Add notes about this call..."
                class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900 resize-none"
              />
              <div class="flex items-center justify-between mt-2">
                <span v-if="saved" class="text-xs text-emerald-600 flex items-center gap-1">
                  <font-awesome-icon icon="circle-check" class="text-xs" />
                  Saved
                </span>
                <span v-else class="text-xs text-gray-400" />
                <button
                  @click="saveNotes"
                  :disabled="saving"
                  class="px-4 py-2 bg-gray-900 text-white text-xs rounded-lg hover:bg-gray-700 disabled:opacity-40 transition-colors"
                >
                  {{ saving ? 'Saving...' : 'Save notes' }}
                </button>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>
</template>