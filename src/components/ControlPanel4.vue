// src/components/ControlPanel4.vue

<template>
  <div class="control-panel-container">
    <n-space justify="space-between" align="center" style="width: 100%;">
      <n-space align="center">
        <n-h6 prefix="bar" class="panel-title" style="margin-right: 12px;">层级选择</n-h6>
        <n-button
            strong secondary :type="selectedSteps.includes('step1') ? 'success' : 'error'"
            @click="toggleStep('step1')">
          轮廓增强 (Step 1)
        </n-button>
        <n-button
            strong secondary :type="selectedSteps.includes('step2') ? 'success' : 'error'"
            @click="toggleStep('step2')" :disabled="!selectedSteps.includes('step1')">
          纹理增强 (Step 2)
        </n-button>
        <n-button
            strong secondary :type="selectedSteps.includes('step3') ? 'success' : 'error'"
            @click="toggleStep('step3')" :disabled="!selectedSteps.includes('step1')">
          语义增强 (Step 3)
        </n-button>
      </n-space>

      <n-button v-if="showReportButton" type="primary" @click="emit('show-report')">
        查看报告
      </n-button>
    </n-space>

    <n-collapse>
      <n-collapse-item title="高级参数设置" name="advanced-settings">
        <div class="advanced-options-grid">
          <n-space align="center" item-style="display: flex; align-items: center;">
            <n-text depth="3">放大倍数:</n-text>
            <n-input-number v-model:value="form.scale" size="small" :min="1" :step="1" style="width: 90px" />

            <n-text depth="3" style="margin-left: 12px;">基础通道:</n-text>
            <n-input-number v-model:value="form.baseChannels" size="small" :min="32" :step="32" style="width: 90px" />

            <n-text depth="3" style="margin-left: 12px;">输出格式:</n-text>
            <n-radio-group v-model:value="form.outputFormat" size="small">
              <n-radio-button value="png">PNG</n-radio-button>
              <n-radio-button value="jpg">JPG</n-radio-button>
            </n-radio-group>
          </n-space>

          <n-space align="center" item-style="display: flex; align-items: center;">
            <n-switch v-model:value="form.normalize" size="small" />
            <n-text depth="3">输入标准化</n-text>
            <n-switch v-model:value="form.bilinear" size="small" style="margin-left: 12px;" />
            <n-text depth="3">双线性上采样</n-text>
          </n-space>
        </div>
      </n-collapse-item>
    </n-collapse>
  </div>
</template>

<script setup>
import {
  NButton, NSpace, NH6, NCollapse, NCollapseItem, NInputNumber,
  NSwitch, NRadioGroup, NRadioButton, NText
} from 'naive-ui';
import { reactive, watch, onMounted } from 'vue';

const props = defineProps({
  selectedSteps: { type: Array, default: () => [] },
  advancedSettings: { type: Object, default: () => ({}) },
  showReportButton: { type: Boolean, default: false }
});

const emit = defineEmits(['update:selectedSteps', 'show-report', 'update:advancedSettings']);

const form = reactive({
  scale: 4,
  baseChannels: 64,
  bilinear: false,
  normalize: true,
  outputFormat: 'png'
});

// Watch for changes from the parent (e.g., model selection) and update the local form
watch(() => props.advancedSettings, (newSettings) => {
  if (newSettings) {
    Object.assign(form, newSettings);
  }
}, { deep: true, immediate: true });

// Watch for local user changes and emit them to the parent
watch(form, (newSettings) => {
  emit('update:advancedSettings', { ...newSettings });
}, { deep: true });

const toggleStep = (stepValue) => {
  const stepsSet = new Set(props.selectedSteps);
  if (stepsSet.has(stepValue)) {
    stepsSet.delete(stepValue);
    if (stepValue === 'step1') {
      stepsSet.delete('step2');
      stepsSet.delete('step3');
    }
  } else {
    stepsSet.add(stepValue);
  }
  emit('update:selectedSteps', Array.from(stepsSet));
};

onMounted(() => {
  // Ensure the initial state is emitted
  emit('update:advancedSettings', { ...form });
});
</script>

<style scoped>
.control-panel-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 16px 20px;
  background-color: var(--card-color-cpl-ng);
  border: 1px solid var(--border-color-control-panel);
  border-radius: 12px;
  box-shadow: var(--component-shadow);
  max-width: 720px;
  width: 100%;
  margin: 0 auto;
}

.panel-title {
  margin: 0;
  white-space: nowrap;
}

.advanced-options-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
</style>
