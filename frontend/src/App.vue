<script setup lang="ts">
import { ref } from 'vue'
import AppHeader from './components/AppHeader.vue'
import RequirementsInput from './components/RequirementsInput.vue'
import TasksList from './components/TasksList.vue'

interface Task {
  title: string
  description: string
  acceptance_criteria: string[]
  priority: 'Low' | 'Medium' | 'High'
}

interface DecompositionResponse {
  project_name: string
  tasks: Task[]
}

const isLoading = ref(false)
const result = ref<DecompositionResponse | null>(null)

async function handleDecompose(rawRequirements: string) {
  isLoading.value = true
  result.value = null

  try {
    const response = await fetch('http://localhost:8000/api/v1/decompose', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ raw_requirements: rawRequirements })
    })

    if (!response.ok) throw new Error('Ошибка сервера')
    result.value = await response.json()
  } catch (error) {
    alert('Не удалось связаться с бэкендом. Убедись, что FastAPI запущен.')
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

function downloadJiraJson() {
  if (!result.value) return
  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(result.value, null, 2))
  const downloadAnchor = document.createElement('a')
  downloadAnchor.setAttribute("href", dataStr)
  downloadAnchor.setAttribute("download", `${result.value.project_name || 'tasks'}-jira-import.json`)
  document.body.appendChild(downloadAnchor)
  downloadAnchor.click()
  downloadAnchor.remove()
}
</script>

<template>
  <div class="min-h-screen bg-brand-bg text-gray-100 flex flex-col">
    <AppHeader />
    <main class="flex-1 grid grid-cols-1 lg:grid-cols-2 p-4 md:p-8 gap-6 md:gap-8 min-h-0 overflow-y-auto lg:overflow-hidden">
      <RequirementsInput :is-loading="isLoading" @submit="handleDecompose" />
      <TasksList :result="result" :is-loading="isLoading" @download="downloadJiraJson" />
    </main>
  </div>
</template>
