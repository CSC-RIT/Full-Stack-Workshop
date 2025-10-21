<script setup>
import { ref, onMounted, computed } from 'vue'
// Importing the SearchBar component for filtering and searching tasks
import SearchBar from './components/SearchBar.vue'
// Importing the TaskList component to display the tasks
import TaskList from './components/TaskList.vue'

const tasks = ref([])
const searchTerm = ref('')
const filterStatus = ref('')
const filterOwner = ref('')

// Function to fetch tasks from the backend API
const fetchTasks = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/tasks')
    tasks.value = await response.json()
  } catch (error) {
    console.error('Error fetching tasks:', error)
  }
}

// Fetch tasks when the component is mounted
onMounted(fetchTasks)

// Computed property to filter tasks based on search term, status, and owner
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

// Computed property to get unique statuses for the filter dropdown
const uniqueStatuses = computed(() => {
  const statuses = new Set(tasks.value.map(task => task.status))
  return ['All', ...Array.from(statuses)]
})

// Computed property to get unique owners for the filter dropdown
const uniqueOwners = computed(() => {
  const owners = new Set(tasks.value.map(task => task.owner))
  return ['All', ...Array.from(owners)]
})

// Event handler for search input from SearchBar component
const handleSearch = (term) => {
  searchTerm.value = term
}

// Event handler for status filter selection from SearchBar component
const handleFilterStatus = (status) => {
  filterStatus.value = status === 'All' ? '' : status
}

// Event handler for owner filter selection from SearchBar component
const handleFilterOwner = (owner) => {
  filterOwner.value = owner === 'All' ? '' : owner
}

// Handle updating task status via backend API
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
      fetchTasks() // Re-fetch tasks to update the UI
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

    <!-- SearchBar Component: Handles search input and filter selections -->
    <SearchBar
      @search="handleSearch"
      @filterStatus="handleFilterStatus"
      @filterOwner="handleFilterOwner"
      :statuses="uniqueStatuses"
      :owners="uniqueOwners"
    />

    <!-- TaskList Component: Displays the filtered tasks -->
    <TaskList :tasks="filteredTasks" @update-task-status="handleUpdateTaskStatus" />
  </div>
</template>
