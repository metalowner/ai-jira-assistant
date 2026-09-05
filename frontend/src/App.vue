<script setup lang="ts">
import { ref } from 'vue'
import { Sparkles, Download, Loader2, CheckCircle2 } from 'lucide-vue-next'

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

const rawRequirements = ref('')
const isLoading = ref(false)
const result = ref<DecompositionResponse | null>(null)

async function handleDecompose() {
  if (!rawRequirements.value.trim() || isLoading.value) return
  
  isLoading.value = true
  result.value = null

  try {
    const response = await fetch('http://localhost:8000/api/v1/decompose', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ raw_requirements: rawRequirements.value })
    })

    if (!response.ok) throw new Error('Ошибка сервера')
    result.value = await response.json()
    } catch (error: any) {
    alert(`Ошибка связи с бэкендом: ${error.message}. Проверь консоль браузера.`);
    console.error('Детали ошибки:', error);
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
    <!-- Header -->
    <header class="border-b border-brand-border px-8 py-4 bg-brand-card flex justify-between items-center">
      <div class="flex items-center gap-3">
        <div class="bg-indigo-600 p-2 rounded-lg text-white">
          <Sparkles class="w-5 h-5" />
        </div>
        <div>
          <h1 class="font-bold text-lg leading-tight">AI Jira Assistant</h1>
          <p class="text-xs text-gray-400">Technical PM Automation Tool</p>
        </div>
      </div>
      <div class="text-xs px-3 py-1 bg-green-500/10 text-green-400 rounded-full border border-green-500/20 flex items-center gap-1.5">
        <span class="w-2 bg-green-400 h-2 rounded-full animate-pulse"></span> API Connected
      </div>
    </header>

        <!-- Main Content -->
    <main class="flex-1 grid grid-cols-1 lg:grid-cols-2 p-4 md:p-8 gap-6 md:gap-8 min-h-0 overflow-y-auto lg:overflow-hidden">
      <!-- Left: Input Area -->
      <div class="flex flex-col gap-4 bg-brand-card p-5 md:p-6 rounded-xl border border-brand-border lg:h-[calc(100vh-140px)] min-h-[400px]">
        <h2 class="text-xs font-semibold uppercase tracking-wider text-gray-400">Бизнес-требования / PRD</h2>
        <textarea
          v-model="rawRequirements"
          placeholder="Вставь сюда сырые требования, мысли заказчика или описание фичи из чата..."
          class="flex-1 w-full bg-brand-bg border border-brand-border rounded-lg p-4 text-sm text-gray-200 focus:outline-none focus:border-indigo-500 resize-none transition-colors min-h-[250px] lg:min-h-0"
        ></textarea>
        <button
          @click="handleDecompose"
          :disabled="isLoading || !rawRequirements.trim()"
          class="w-full bg-indigo-600 hover:bg-indigo-500 disabled:bg-gray-800 disabled:text-gray-500 text-white font-medium py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-all cursor-pointer text-sm md:text-base shrink-0"
        >
          <Loader2 v-if="isLoading" class="w-5 h-5 animate-spin" />
          <Sparkles v-else class="w-5 h-5" />
          {{ isLoading ? 'Анализируем требования...' : 'Декомпозировать на User Stories' }}
        </button>
      </div>

      <!-- Right: Output Area -->
      <div class="flex flex-col gap-4 bg-brand-card p-5 md:p-6 rounded-xl border border-brand-border lg:h-[calc(100vh-140px)] lg:overflow-y-auto min-h-[400px]">
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 sticky top-0 bg-brand-card pb-3 border-b border-brand-border z-10">
          <h2 class="text-xs font-semibold uppercase tracking-wider text-gray-400 truncate max-w-full">
            Результат: {{ result?.project_name || 'Ожидание ввода' }}
          </h2>
          <button
            v-if="result"
            @click="downloadJiraJson"
            class="w-full sm:w-auto text-xs bg-gray-800 hover:bg-gray-700 text-gray-200 border border-brand-border px-3 py-1.5 rounded-lg flex items-center justify-center gap-1.5 transition-colors cursor-pointer shrink-0"
          >
            <Download class="w-3.5 h-3.5" /> Экспорт JSON
          </button>
        </div>

        <!-- Empty State -->
        <div v-if="!result && !isLoading" class="flex-1 flex flex-col items-center justify-center text-center p-6 text-gray-500 min-h-[200px]">
          <Sparkles class="w-12 h-12 mb-3 stroke-1" />
          <p class="text-xs md:text-sm leading-relaxed">Введите требования слева и нажмите кнопку,<br class="hidden sm:inline" /> чтобы ИИ сформировал готовый бэклог спринта.</p>
        </div>

        <!-- Skeleton Loader -->
        <div v-if="isLoading" class="flex flex-col gap-4 animate-pulse">
          <div v-for="i in 3" :key="i" class="bg-brand-bg h-32 rounded-lg border border-brand-border"></div>
        </div>

        <!-- Tasks List -->
        <div v-if="result" class="flex flex-col gap-4">
          <div v-for="(task, index) in result.tasks" :key="index" class="bg-brand-bg p-4 md:p-5 rounded-lg border border-brand-border flex flex-col gap-3 transition-all hover:border-brand-border/80">
            <div class="flex justify-between items-center gap-4">
              <h3 class="font-semibold text-gray-100 text-xs md:text-sm leading-snug break-words flex-1">{{ task.title }}</h3>
              <!-- Фиксируем ширину бейджа, чтобы он никогда не деформировался -->
              <span :class="{
                'bg-red-500/10 text-red-400 border-red-500/20': task.priority === 'High',
                'bg-yellow-500/10 text-yellow-400 border-yellow-500/20': task.priority === 'Medium',
                'bg-blue-500/10 text-blue-400 border-blue-500/20': task.priority === 'Low',
              }" class="text-[10px] font-bold px-2 py-0.5 rounded border uppercase tracking-wider text-center min-w-[65px] shrink-0">
                {{ task.priority }}
              </span>
            </div>
            <p class="text-xs text-gray-400 leading-relaxed bg-brand-card/50 p-3 rounded border border-brand-border/40 break-words">
              {{ task.description }}
            </p>
            <div class="flex flex-col gap-2">
              <span class="text-[10px] font-bold text-gray-500 uppercase tracking-wider">Acceptance Criteria:</span>
              <div v-for="(criteria, cIndex) in task.acceptance_criteria" :key="cIndex" class="flex items-start gap-2 text-xs text-gray-300">
                <CheckCircle2 class="w-3.5 h-3.5 text-indigo-500 shrink-0 mt-0.5" />
                <span class="break-words flex-1">{{ criteria }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

  </div>
</template>
