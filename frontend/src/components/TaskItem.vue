<script setup>
const props = defineProps({
  task: Object
})

const emit = defineEmits(['move-task'])

const getStatusClass = (status) => {
  switch (status) {
    case 'To Do':
      return 'status-todo'
    case 'In Progress':
      return 'status-in-progress'
    case 'Done':
      return 'status-done'
    default:
      return ''
  }
}

const moveTask = (direction) => {
  let newStatus = props.task.status
  if (direction === 'left') {
    if (props.task.status === 'In Progress') {
      newStatus = 'To Do'
    } else if (props.task.status === 'Done') {
      newStatus = 'In Progress'
    }
  } else if (direction === 'right') {
    if (props.task.status === 'To Do') {
      newStatus = 'In Progress'
    } else if (props.task.status === 'In Progress') {
      newStatus = 'Done'
    }
  }
  if (newStatus !== props.task.status) {
    emit('move-task', props.task.id, newStatus)
  }
}
</script>

<template>
  <div class="task-item">
    <h3>{{ task.name }}</h3>
    <p>Owner: {{ task.owner }}</p>
    <p :class="['status', getStatusClass(task.status)]">
      Status: {{ task.status }}
    </p>
    <div class="task-actions">
      <button
        v-if="task.status === 'In Progress' || task.status === 'Done'"
        @click="moveTask('left')"
        class="move-button move-left"
      >
        &lt; Move Left
      </button>
      <button
        v-if="task.status === 'To Do' || task.status === 'In Progress'"
        @click="moveTask('right')"
        class="move-button move-right"
      >
        Move Right &gt;
      </button>
    </div>
  </div>
</template>
