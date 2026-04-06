<script setup lang="ts">
defineProps<{
  search: string;
  callerTypeFilter: string;
  urgentFilter: string;
}>();

const emit = defineEmits<{
  "update:search": [value: string];
  "update:callerTypeFilter": [value: string];
  "update:urgentFilter": [value: string];
}>();
</script>

<template>
  <div class="flex items-center gap-3 mb-4 flex-wrap">
    <div class="relative flex-1 min-w-[200px]">
      <font-awesome-icon
        icon="phone"
        class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-xs"
      />
      <input
        :value="search"
        @input="
          emit('update:search', ($event.target as HTMLInputElement).value)
        "
        type="text"
        placeholder="Search by name, email, phone..."
        class="w-full pl-8 pr-3 py-3 bg-[#f5f5f5] rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-900"
      />
    </div>
    <select
      :value="callerTypeFilter"
      @change="
        emit(
          'update:callerTypeFilter',
          ($event.target as HTMLSelectElement).value
        )
      "
      class="border border-gray-200 cursor-pointer rounded-lg px-3 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900"
    >
      <option value="">All types</option>
      <option value="new_client">New client</option>
      <option value="existing_client">Existing client</option>
      <option value="opposing_party">Opposing party</option>
    </select>
    <select
      :value="urgentFilter"
      @change="
        emit('update:urgentFilter', ($event.target as HTMLSelectElement).value)
      "
      class="border border-gray-200 cursor-pointer rounded-lg px-3 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900"
    >
      <option value="">All calls</option>
      <option value="true">Urgent only</option>
    </select>
  </div>
</template>
