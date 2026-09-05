<script setup lang="ts">
import { Sparkles } from 'lucide-vue-next'
</script>

<template>
  <header class="border-b border-brand-border px-8 py-4 bg-brand-card flex justify-between items-center">
    <div class="flex items-center gap-3">
      <div class="bg-indigo-600 p-2 rounded-lg text-white">
        <Sparkles class="w-5 h-5" />
      </div>
      <div>
        <h1 class="text-xl font-semibold text-slate-900 tracking-tight leading-tight">
          AI Jira Assistant
        </h1>
        <p class="text-xs text-slate-500">Technical PM Automation Tool</p>
      </div>
    </div>
    <div class="text-xs px-3 py-1 bg-green-500/10 text-green-400 rounded-full border border-green-500/20 flex items-center gap-1.5">
      <span class="w-2 bg-green-400 h-2 rounded-full animate-pulse"></span> API Connected
    </div>
  </header>
</template>
