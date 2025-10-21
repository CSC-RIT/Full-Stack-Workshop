<script setup>
// Importing the TaskItem component to display individual tasks
import TaskItem from './TaskItem.vue'
import { computed } from 'vue'

const props = defineProps({
  tasks: Array
})

const emit = defineEmits(['update-task-status'])

// Computed property to group tasks by their status
const tasksByStatus = computed(() => {
  const grouped = {
    'To Do': [],
    'In Progress': [],
    'Done': []
  }
  props.tasks.forEach(task => {
    if (grouped[task.status]) {
      grouped[task.status].push(task)
    }
  })
  return grouped
})

const handleMoveTask = (taskId, newStatus) => {
  emit('update-task-status', taskId, newStatus)
}
</script>

<template>
  <div class="task-list-grid">
    <!-- Iterate over each status group (To Do, In Progress, Done) -->
    <div v-for="(statusTasks, status) in tasksByStatus" :key="status" class="task-column">
      <h2>{{ status }} ({{ statusTasks.length }})</h2>
      <div class="task-item-container">
        <!-- Iterate over tasks within each status group and render TaskItem for each -->
        <TaskItem
          v-for="task in statusTasks"
          :key="task.id"
          :task="task"
          @move-task="handleMoveTask"
        />
      </div>
    </div>
  </div>
</template>