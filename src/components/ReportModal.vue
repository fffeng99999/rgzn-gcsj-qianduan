<template>
  <n-modal
      :show="show"
      @update:show="emit('update:show', $event)"
      class="custom-card-modal"
      preset="card"
      style="width: 80%; max-width: 900px;"
      title="详细结果报告"
      :bordered="false"
      size="huge"
      closable
  >
    <ResultsDisplay
        :selected-steps="selectedSteps"
        :comparison-images="comparisonImages"
        :gif-url="gifUrl"
        :metrics="metrics"
    />
  </n-modal>
</template>

<script setup>
import { NModal } from 'naive-ui';
import ResultsDisplay from '@/components/ResultsDisplay.vue';

// 定义 props 来接收父组件传递的数据
defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  selectedSteps: {
    type: Array,
    default: () => [],
  },
  comparisonImages: {
    type: Array,
    default: () => [],
  },
  gifUrl: {
    type: String,
    default: '',
  },
  metrics: {
    type: Object,
    default: () => ({}),
  },
});

// 定义 emit 事件，用于 v-model:show 的双向绑定
const emit = defineEmits(['update:show']);
</script>

<style scoped>
/* 如果有特定于此模态框的样式，可以放在这里 */
</style>