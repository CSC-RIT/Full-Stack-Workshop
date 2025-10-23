<script setup>
import TaskItem from './TaskItem.vue'
import { computed } from 'vue'

const props = defineProps({
  tasks: Array
})

const emit = defineEmits(['update-task-status'])

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
    <div v-for="(statusTasks, status) in tasksByStatus" :key="status" class="task-column">
      <h2>{{ status }} ({{ statusTasks.length }})</h2>
      <div class="task-item-container">
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