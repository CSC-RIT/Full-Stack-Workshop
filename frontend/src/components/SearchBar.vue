<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  statuses: Array
  // TODO: Add a prop for owners
})

const emit = defineEmits(['search', 'filterStatus'])

const searchTerm = ref('')
const selectedStatus = ref('All')

watch(searchTerm, (newVal) => {
  emit('search', newVal)
})

watch(selectedStatus, (newVal) => {
  emit('filterStatus', newVal)
})

// TODO: Implement owner filtering

</script>

<template>
  <div class="search-bar">
    <input
      type="text"
      v-model="searchTerm"
      placeholder="Search tasks by name..."
    />

    <select v-model="selectedStatus">
      <option v-for="status in statuses" :key="status" :value="status">
        {{ status }}
      </option>
    </select>

    <!-- TODO: Add a selection dropdown for owners -->
  </div>
</template>
