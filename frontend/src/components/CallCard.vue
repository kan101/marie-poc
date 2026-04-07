<script setup lang="ts">
import type { CallSummary } from "../api";
import Badge from "./Badge.vue";

const props = defineProps<{
  call: CallSummary;
  selected: boolean;
}>();

const emit = defineEmits<{
  select: [id: number];
}>();

// Left border color indicates caller type; urgent overrides all other types
function borderClass(): string {
  if (props.call.urgent) return "border-l-[3px] border-l-orange-500";
  if (props.call.caller_type === "new_client")
    return "border-l-[3px] border-l-emerald-500";
  if (props.call.caller_type === "existing_client")
    return "border-l-[3px] border-l-blue-500";
  if (props.call.caller_type === "opposing_party")
    return "border-l-[3px] border-l-purple-400";
  return "border-l-[3px] border-l-slate-300";
}

/**
 * Maps caller_type string to badge display props
 * Using a lookup object avoids a chain of if/else statements 
 */
function callerTypeBadge(type: string): {
  icon: string;
  text: string;
  variant: string;
} {
  return (
    (
      {
        new_client: { icon: "user", text: "New Client", variant: "emerald" },
        existing_client: {
          icon: "user-check",
          text: "Existing client",
          variant: "blue",
        },
        opposing_party: {
          icon: "user-slash",
          text: "Opposing party",
          variant: "purple",
        },
        unknown: { icon: "user-question", text: "Unknown", variant: "slate" },
      } as Record<string, { icon: string; text: string; variant: string }>
    )[type] ?? { icon: "user", text: "Unknown", variant: "slate" }
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

function initials(name: string): string {
  return name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);
}

// Avatar background matches the caller type color scheme
function avatarBg(): string {
  if (props.call.urgent) return "bg-orange-200 text-orange-800";
  if (props.call.caller_type === "new_client")
    return "bg-emerald-200 text-emerald-800";
  if (props.call.caller_type === "existing_client")
    return "bg-blue-200 text-blue-800";
  if (props.call.caller_type === "opposing_party")
    return "bg-purple-200 text-purple-800";
  return "bg-slate-200 text-slate-700";
}

function formatAppointment(iso: string): string {
  return (
    new Date(iso).toLocaleString("de-DE", {
      timeZone: "Europe/Berlin",
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }) + " (Berlin)"
  );
}
</script>

<template>
  <div
    @click="emit('select', call.id)"
    :class="[
      'group bg-white rounded-2xl overflow-hidden cursor-pointer',
      'transition-all duration-200 hover:shadow-lg hover:-translate-y-0.5',
      borderClass(),
      selected ? ' shadow-lg' : 'shadow-sm',
    ]"
  >
    <!-- Header -->
    <div :class="['px-5 pt-5 pb-4 bg-slate-50']">
      <div class="flex items-start gap-3">
        <!-- Avatar -->
        <div
          :class="[
            'w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0',
            avatarBg(),
          ]"
        >
          {{ initials(call.caller.full_name) }}
        </div>

        <!-- Caller info -->
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 flex-wrap mb-1">
            <span class="font-bold text-gray-900 text-sm truncate">{{
              call.caller.full_name
            }}</span>
            <Badge
              :icon="callerTypeBadge(call.caller_type).icon"
              :text="callerTypeBadge(call.caller_type).text"
              :variant="callerTypeBadge(call.caller_type).variant"
            />
          </div>

          <div class="flex items-center gap-4 mt-2 text-xs text-gray-500 flex-wrap">
            <span class="flex items-center gap-1.5">
              <font-awesome-icon
                icon="phone"
                class="text-emerald-400 text-sm"
              />
              {{ call.caller.phone_number }}
            </span>
            <span
              v-if="call.caller.email"
              class="flex items-center gap-1.5 truncate"
            >
              <font-awesome-icon
                icon="envelope"
                class="text-blue-400 text-sm"
              />
              {{ call.caller.email }}
            </span>
          </div>
        </div>

        <!-- Date + duration top right -->
        <div class="text-right flex-shrink-0">
          <p class="text-xs text-gray-500">{{ formatDate(call.called_at) }}</p>
          <p
            class="text-xs text-slate-500 mt-0.5 flex items-center justify-end gap-1"
          >
            <font-awesome-icon
              icon="clock"
              class="text-slate-400 text-sm"
            />
            {{ call.duration_display }}
          </p>
        </div>
      </div>
    </div>

    <!--Badges-->
    <div class="px-5 py-3 bg-white">
      <div class="flex items-center gap-2 flex-shrink-0 flex-wrap">
        <Badge
          v-if="call.urgent"
          icon="triangle-exclamation"
          text="Callback needed"
          variant="orange"
        />
        <Badge
          v-if="call.follow_up_sent"
          icon="paper-plane"
          text="Email Sent"
          variant="blue"
        />
        <Badge
          v-if="call.proposed_appointment"
          icon="calendar"
          :text="'Appointment:  ' + formatAppointment(call.proposed_appointment!)"
          variant="blue"
        />
        <Badge
          v-if="!call.urgent && !call.follow_up_sent"
          icon="ban"
          text="No action"
          variant="slate"
        />
      </div>
    </div>

    <!-- Summary -->
    <div v-if="call.summary" class="px-5 py-3 bg-white">
      <div
        class="rounded-xl bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50 border border-emerald-100/80 p-4"
      >
        <div data-v-019ba636="" class="flex items-start gap-3">
          <div
            data-v-019ba636=""
            class="shrink-0 w-8 h-8 rounded-lg bg-emerald-100 flex items-center justify-center"
          >
            <font-awesome-icon
              icon="fa-wand-magic-sparkles"
              class="text-green-500 text-xs"
            />
          </div>
          <div data-v-019ba636="" class="flex-1 min-w-0">
            <p
              data-v-019ba636=""
              class="text-sm text-emerald-900/80 leading-relaxed md:line-clamp-none"
            >
              {{ call.summary }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div
      class="px-5 py-3 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between"
    >
      <!-- Audio player -->
      <audio
        :src="`/media/${call.audio_file}`"
        controls
        class="h-7 w-full sm:flex-1 sm:max-w-[260px] opacity-80 group-hover:opacity-100 transition-opacity"
        @click.stop
      />

      <!-- Bottom row: appointment + action badge -->
      <div
        class="flex items-center justify-between gap-2 p-2 mr-2 sm:justify-end"
      >
      </div>
    </div>
  </div>
</template>
