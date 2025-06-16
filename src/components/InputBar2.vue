// src/components/InputBar2.vue

<template>
  <div class="input-bar-container">
    <div class="chat-input-box">
      <div class="textarea-wrapper">
        <n-input
            v-model:value="inputValue"
            type="textarea"
            :placeholder="placeholderText"
            :autosize="{ minRows: 1, maxRows: 5 }"
            @keydown="handleKeydown"
            :disabled="isProcessing"
        />
      </div>

      <div class="actions-wrapper">
        <div class="left-actions">
          <n-tooltip trigger="hover">
            <template #trigger>
              <n-button text class="action-btn upload-btn" @click="emit('upload')">
                <template #icon>
                  <n-icon :component="Add" />
                </template>
              </n-button>
            </template>
            上传图片
          </n-tooltip>

          <n-select
              v-if="props.isImageUploaded"
              size="small"
              :value="props.selectedModel"
              :options="modelOptions"
              placeholder="选择模型"
              style="width: 150px;"
              @update:value="(value) => emit('update:selectedModel', value)"
              :disabled="isProcessing"
          />
        </div>

        <n-button text class="action-btn send-btn" @click="handleSend" :disabled="isProcessing">
          <template #icon>
            <n-icon :component="Send20Filled" />
          </template>
        </n-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { NInput, NIcon, NButton, useMessage, NTooltip, NSelect } from 'naive-ui';
import { Add } from '@vicons/ionicons5';
import { Send20Filled } from '@vicons/fluent';

const props = defineProps({
  selectedSteps: {
    type: Array,
    default: () => []
  },
  isImageUploaded: {
    type: Boolean,
    default: false
  },
  selectedModel: {
    type: String,
    default: null
  },
  // ✨ 2. Added a prop to receive the processing status from the parent component
  isProcessing: {
    type: Boolean,
    default: false,
  }
});

// ✨ 3. Removed 'start-processing' as it's no longer needed.
// The parent component now controls the entire processing flow.
const emit = defineEmits(['send', 'upload', 'update:selectedModel']);

const inputValue = ref('');
const message = useMessage();

const modelOptions = ref([
  {
    label: "通用模型",
    value: "unet_best.pth" // Make sure this value matches your backend model file
  },
  {
    label: "动漫模型",
    value: "RealESRGAN_x4plus_anime_6B.pth"
  }
]);

const placeholderText = computed(() => {
  if (!props.isImageUploaded) {
    return '请先上传图片...';
  }
  return props.selectedSteps.includes('step3')
      ? '输入提示词...'
      : '“语义增强”未开启，可直接点击右侧按钮提交处理';
});

const handleSend = () => {
  if (props.isProcessing) return; // Extra safeguard

  const isSemanticStepEnabled = props.selectedSteps.includes('step3');

  if (isSemanticStepEnabled && !inputValue.value.trim()) {
    message.warning('“语义增强”已开启，请输入文字描述');
    return;
  }

  // The component's only job is to send the prompt value.
  // The parent will handle the API call.
  emit('send', inputValue.value);
  inputValue.value = '';
};

const handleKeydown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    handleSend();
  }
};
</script>

<style scoped>
/* Your original styles are fully preserved */
.input-bar-container {
  width: 100%;
  display: flex;
  justify-content: center;
  flex-shrink: 0;
}

.chat-input-box {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 720px;
  background-color: var(--inputbar-bg);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  padding: 8px 8px 8px 16px;
  box-sizing: border-box;
  box-shadow: var(--component-shadow, 0 2px 12px rgba(0, 0, 0, 0.1));
  transition: all 0.3s ease;
}

.textarea-wrapper {
  padding-right: 8px;
}

:deep(.n-input--textarea) {
  background-color: transparent !important;
}
:deep(.n-input--textarea .n-input__border),
:deep(.n-input--textarea .n-input__state-border) {
  display: none !important;
}
:deep(.n-input--textarea .n-input-wrapper) {
  padding: 0 !important;
}

.actions-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.left-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.action-btn {
  color: var(--n-text-color-disabled);
  transition: color 0.3s;
}
.action-btn:hover {
  color: var(--n-text-color);
}

.send-btn {
  font-size: 25px;
}
.upload-btn {
  font-size: 20px;
}
</style>

<<<<<<< HEAD
=======

>>>>>>> 7a887e08bad3f67f5ba7643fee66ec61202038b4
