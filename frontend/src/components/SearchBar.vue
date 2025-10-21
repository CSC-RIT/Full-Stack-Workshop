<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  statuses: Array,
  owners: Array
})

const emit = defineEmits(['search', 'filterStatus', 'filterOwner'])

const searchTerm = ref('')
const selectedStatus = ref('All')
const selectedOwner = ref('All')

watch(searchTerm, (newVal) => {
  emit('search', newVal)
})

watch(selectedStatus, (newVal) => {
  emit('filterStatus', newVal)
})

watch(selectedOwner, (newVal) => {
  emit('filterOwner', newVal)
})
</script>

<template>
  <div class="search-bar">
    <input
      type="text"
      v-model="searchTerm"
      placeholder="Search tasks by name..."
    />

    <select
      v-model="selectedStatus"
    >
      <option v-for="status in statuses" :key="status" :value="status">{{ status }}</option>
    </select>

    <select
      v-model="selectedOwner"
    >
      <option v-for="owner in owners" :key="owner" :value="owner">{{ owner }}</option>
    </select>
  </div>
</template>