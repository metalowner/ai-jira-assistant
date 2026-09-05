<script setup lang="ts">
import { ref } from 'vue'
import { Sparkles, Loader2 } from 'lucide-vue-next'

defineProps<{ isLoading: boolean }>()
const emit = defineEmits<{ (e: 'submit', text: string): void }>()

const text = ref('')

function handleSubmit() {
  if (!text.value.trim()) return
  emit('submit', text.value)
}
</script>

<template>
  <div class="flex flex-col gap-4 bg-brand-card p-5 md:p-6 rounded-xl border border-brand-border lg:h-[calc(100vh-140px)] min-h-[400px]">
    <h2 class="text-xs font-semibold uppercase tracking-wider text-slate-500">Бизнес-требования / PRD</h2>
    <textarea
      v-model="text"
      placeholder="Вставь сюда сырые требования, мысли заказчика или описание фичи из чата..."
      class="flex-1 w-full bg-brand-bg border border-brand-border rounded-lg p-4 text-sm text-slate-800 focus:outline-none focus:border-indigo-500 resize-none transition-colors min-h-[250px] lg:min-h-0"
    ></textarea>
    <button
      @click="handleSubmit"
      :disabled="isLoading || !text.trim()"
      class="w-full bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-200 disabled:text-slate-400 text-white font-medium py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-all cursor-pointer text-sm md:text-base shrink-0"
    >
      <Loader2 v-if="isLoading" class="w-5 h-5 animate-spin" />
      <Sparkles v-else class="w-5 h-5" />
      {{ isLoading ? 'Анализируем требования...' : 'Декомпозировать на User Stories' }}
    </button>
  </div>
</template>
