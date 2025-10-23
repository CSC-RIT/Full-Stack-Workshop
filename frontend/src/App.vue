<script setup>
import { ref, onMounted, computed } from 'vue'
import SearchBar from './components/SearchBar.vue'
import TaskList from './components/TaskList.vue'

const tasks = ref([])
const searchTerm = ref('')
const filterStatus = ref('')
const filterOwner = ref('')

const fetchTasks = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/tasks')
    tasks.value = await response.json()
  } catch (error) {
    console.error('Error fetching tasks:', error)
  }
}

onMounted(fetchTasks)

const filteredTasks = computed(() => {
  let filtered = tasks.value

  if (searchTerm.value) {
    filtered = filtered.filter(task =>
      task.name.toLowerCase().includes(searchTerm.value.toLowerCase())
    )
  }

  if (filterStatus.value) {
    filtered = filtered.filter(task =>
      task.status.toLowerCase() === filterStatus.value.toLowerCase()
    )
  }

  if (filterOwner.value) {
    filtered = filtered.filter(task =>
      task.owner.toLowerCase() === filterOwner.value.toLowerCase()
    )
  }

  return filtered
})

const uniqueStatuses = computed(() => {
  const statuses = new Set(tasks.value.map(task => task.status))
  return ['All', ...Array.from(statuses)]
})

// TODO: Implement unique owners for filtering

const handleSearch = (term) => {
  searchTerm.value = term
}

const handleFilterStatus = (status) => {
  filterStatus.value = status === 'All' ? '' : status
}

// TODO: Implement handleFilterOwner

const handleUpdateTaskStatus = async (taskId, newStatus) => {
  try {
    const response = await fetch(`http://127.0.0.1:5000/tasks/${taskId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ status: newStatus }),
    })
    if (response.ok) {
      console.log(`Task ${taskId} status updated to ${newStatus}`)
      fetchTasks()
    } else {
      console.error('Failed to update task status', await response.json())
    }
  } catch (error) {
    console.error('Error updating task status:', error)
  }
}
</script>

<template>
  <div id="app">
    <h1>Task Management App</h1>

    <SearchBar
      @search="handleSearch"
      @filterStatus="handleFilterStatus"
      :statuses="uniqueStatuses"
    />

    <TaskList :tasks="filteredTasks" @update-task-status="handleUpdateTaskStatus" />
  </div>
</template>
