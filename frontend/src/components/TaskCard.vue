<script setup lang="ts">
import { CheckCircle2 } from 'lucide-vue-next'

interface Task {
  title: string
  description: string
  acceptance_criteria: string[]
  priority: 'Low' | 'Medium' | 'High'
}

defineProps<{ task: Task }>()
</script>

<template>
  <div class="bg-brand-card p-4 md:p-5 rounded-lg border border-brand-border flex flex-col gap-3 transition-all hover:border-slate-300 shadow-sm">
    <div class="flex justify-between items-center gap-4">
      <h3 class="font-semibold text-slate-800 text-xs md:text-sm leading-snug break-words flex-1">{{ task.title }}</h3>
      <span :class="{
        'bg-red-50 text-red-600 border-red-200': task.priority === 'High',
        'bg-amber-50 text-amber-600 border-amber-200': task.priority === 'Medium',
        'bg-blue-50 text-blue-600 border-blue-200': task.priority === 'Low',
      }" class="text-[10px] font-bold px-2 py-0.5 rounded border uppercase tracking-wider text-center min-w-[65px] shrink-0">
        {{ task.priority }}
      </span>
    </div>
    <p class="text-xs text-slate-600 leading-relaxed bg-slate-50 p-3 rounded border border-brand-border break-words">
      {{ task.description }}
    </p>
    <div class="flex flex-col gap-2">
      <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Acceptance Criteria:</span>
      <div v-for="(criteria, cIndex) in task.acceptance_criteria" :key="cIndex" class="flex items-start gap-2 text-xs text-slate-700">
        <CheckCircle2 class="w-3.5 h-3.5 text-indigo-600 shrink-0 mt-0.5" />
        <span class="break-words flex-1">{{ criteria }}</span>
      </div>
    </div>
  </div>
</template>
