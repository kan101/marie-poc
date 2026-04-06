<script setup lang="ts">
defineProps<{
  icon: string;
  text: string;
  variant: string;
}>();

const variantClass: Record<string, string> = {
  orange: "bg-orange-50 text-orange-700 ring-1 ring-orange-200",
  blue: "bg-blue-50 text-blue-400 ring-1 ring-blue-100",
  violet: "bg-violet-50 text-violet-700 ring-1 ring-violet-200",
  slate: "bg-slate-50 text-slate-500 ring-1 ring-slate-200",
  emerald: "bg-emerald-50 text-emerald-700 ring-1 ring-emerald-200",
  purple: "bg-purple-50 text-purple-700 ring-1 ring-purple-200",
  green: "bg-green-50 text-green-700 ring-1 ring-green-200"
};
</script>

<template>
  <span
    :class="[
      'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs',
      variantClass[variant],
    ]"
  >
    <font-awesome-icon :icon="icon" class="text-sm" />
    {{ text }}
  </span>
</template>
