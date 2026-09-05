<script setup lang="ts">
import { Sparkles, Download } from 'lucide-vue-next'
import TaskCard from './TaskCard.vue'

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

defineProps<{
  result: DecompositionResponse | null
  isLoading: boolean
}>()

const emit = defineEmits<{ (e: 'download'): void }>()
</script>

<template>
  <div class="flex flex-col gap-4 bg-brand-card p-5 md:p-6 rounded-xl border border-brand-border lg:h-[calc(100vh-140px)] lg:overflow-y-auto min-h-[400px] shadow-sm">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 sticky top-0 bg-brand-card pb-3 border-b border-brand-border z-10">
      <h2 class="text-xs font-semibold uppercase tracking-wider text-slate-500 truncate max-w-full">
        Результат: {{ result?.project_name || 'Ожидание ввода' }}
      </h2>
      <button
        v-if="result"
        @click="emit('download')"
        class="w-full sm:w-auto text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 border border-brand-border px-3 py-1.5 rounded-lg flex items-center justify-center gap-1.5 transition-colors cursor-pointer shrink-0 font-medium"
      >
        <Download class="w-3.5 h-3.5" /> Экспорт JSON
      </button>
    </div>

    <!-- Empty State -->
    <div v-if="!result && !isLoading" class="flex-1 flex flex-col items-center justify-center text-center p-6 text-slate-400 min-h-[200px]">
      <Sparkles class="w-12 h-12 mb-3 stroke-1 text-slate-300" />
      <p class="text-xs md:text-sm leading-relaxed">Введите требования слева и нажмите кнопку,<br class="hidden sm:inline" /> чтобы ИИ сформировал готовый бэклог спринта.</p>
    </div>

    <!-- Skeleton Loader -->
    <div v-if="isLoading" class="flex flex-col gap-4 animate-pulse">
      <div v-for="i in 3" :key="i" class="bg-slate-100 h-32 rounded-lg border border-brand-border"></div>
    </div>

    <!-- Tasks List -->
    <div v-if="result" class="flex flex-col gap-4 bg-slate-50/50 p-2 rounded-lg border border-slate-100">
      <TaskCard v-for="(task, index) in result.tasks" :key="index" :task="task" />
    </div>
  </div>
</template>
