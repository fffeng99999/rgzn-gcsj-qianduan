// src/views/Demo-test5-final.vue

<template>
  <div class="demo-page-container">
    <div class="chat-content-area" :class="{ 'side-by-side': displayState !== 'single' }">
      <div v-if="!isImageUploaded" class="placeholder-box">
        <div class="placeholder-content">
          <n-icon :component="ImageOutline" size="60" />
          <n-text depth="3" style="font-size: 32px;">请上传图片</n-text>
        </div>
      </div>

      <template v-if="isImageUploaded">
        <div class="image-preview-item left-panel-container">
          <Transition name="fade">
            <ImagePreview
                v-if="displayState === 'single'"
                class="image-preview-item"
                :image-url="imageUrl"
                :transform-state="transformState"
                @update:transform="updateTransform"
                @initialized="handleInitialization"/>
          </Transition>

          <template v-if="displayState !== 'single'">
            <Transition name="fade" mode="out-in">
              <StatusDisplayPreviewResult
                  v-if="leftPanelDisplay === 'status'"
                  :progress="processingProgress"
                  :loss-data="lossData" />
              <ImagePreview
                  v-else
                  :image-url="imageUrl"
                  :transform-state="transformState"
                  @update:transform="updateTransform"
                  @initialized="handleInitialization"
              />
            </Transition>
          </template>

          <n-button
              v-if="displayState === 'result'"
              class="view-toggle-button"
              @click="toggleLeftPanel"
              size="small"
              circle
              type="default"
              :title="leftPanelDisplay === 'status' ? '查看原图对比' : '查看处理监控'">
            <template #icon>
              <n-icon :component="SwapHorizontalOutline" />
            </template>
          </n-button>
        </div>

        <Transition name="slide-in-right">
          <div v-if="displayState !== 'single'" class="image-preview-item">
            <ImagePreviewResult
                :image-url="resultImageUrl"
                :transform-state="transformState"
                @update:transform="updateTransform"
                @initialized="handleInitialization"
            />
          </div>
        </Transition>
      </template>
    </div>

    <Transition name="slide-up">
      <div v-if="isImageUploaded" class="controls-wrapper">
        <ControlPanel
            v-model:selected-steps="selectedSteps"
            @show-report="handleShowReport"
            :show-report-button="displayState === 'result'" />
      </div>
    </Transition>

    <div class="input-wrapper">
      <InputBar
          :is-image-uploaded="isImageUploaded"
          :selectedSteps="selectedSteps"
          :is-processing="displayState === 'processing'"
          @send="handleSend"
          @upload="handleUploadClick"
      />
    </div>

    <input ref="fileInputRef" type="file" accept="image/*" style="display: none" @change="handleFileChange"/>
  </div>

  <FileDropOverlay v-if="isDragging" />

  <n-modal
      v-model:show="showReportModal"
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
        :comparison-images="mockComparisonImages"
        :gif-url="mockGifUrl"
        :metrics="mockMetrics"
    />
  </n-modal>
</template>

<script setup>
import { ref, reactive, onUnmounted, computed, watch } from 'vue'; // 引入 watch
import { useMessage, NIcon, NText, NButton, NModal } from 'naive-ui';
import { ImageOutline, SwapHorizontalOutline } from '@vicons/ionicons5';
import ResultsDisplay from '@/components/ResultsDisplay.vue';
import FileDropOverlay from '@/components/FileDropOverlay.vue';
import ImagePreview from '@/components/ImagePreview.vue';
import ImagePreviewResult from "@/components/ImagePreviewResult.vue";
import StatusDisplayPreviewResult from '@/components/StatusDisplayPreviewResult.vue';
import InputBar from '@/components/InputBar2.vue';
import ControlPanel from '@/components/ControlPanel4.vue';
import { useDragAndDrop } from '@/composables/useDragAndDrop.js';
import { useImageUploader } from '@/composables/useImageUploader.js'; // 导入新的 Composable

import '@/assets/views/demo-layout.css'; // CSS 已经单独成文件

// --- Composable Usage ---
const {
  fileInputRef,
  uploadedFile, // 保持引用以便 handleSend 可以访问
  isImageUploaded,
  imageUrl,
  handleUploadClick,
  handleFileChange,
  processAndSetFile, // 暴露给 useDragAndDrop
  cleanup: cleanupUploader // 重命名 cleanup 防止与组件 onUnmounted 钩子内的变量名冲突
} = useImageUploader();

// 将图片处理函数传递给拖拽处理 Composable
const { isDragging } = useDragAndDrop(processAndSetFile);


// --- State and Props ---
const message = useMessage();
const resultImageUrl = computed(() => imageUrl.value); // 假定结果图与原图URL相同，实际应替换为超分结果URL
const displayState = ref('single'); // 'single', 'processing', 'result'
const leftPanelDisplay = ref('status'); // 'status' or 'original' - 控制左侧面板内容
const selectedSteps = ref(['step1']);
const promptText = ref('');
let processingInterval = null;
const processingProgress = ref(0);
const lossData = ref([]);
const transformState = reactive({ scale: 1, translateX: 0, translateY: 0 });
const showReportModal = ref(false);

// --- Mock Data for Report ---
const mockComparisonImages = computed(() => [
  { label: '原始图像', src: imageUrl.value }, // imageUrl 现在来自 useImageUploader
  { label: 'Step 1 结果', src: resultImageUrl.value },
  { label: 'Step 2 结果', src: resultImageUrl.value },
  { label: 'Step 3 结果', src: resultImageUrl.value },
]);
const mockGifUrl = ref("https://via.placeholder.com/400x300.gif?text=Processing+GIF");
const mockMetrics = ref({
  psnr: 32.8,
  ssim: 0.95,
  clipScore: 0.88,
});

// --- Methods ---

const handleShowReport = () => {
  if (displayState.value !== 'result') {
    message.error('请先提交并等待处理结果出现后，再查看报告！');
    return;
  }
  showReportModal.value = true;
};

const handleSend = (text) => {
  // isImageUploaded 和 uploadedFile 现在来自 useImageUploader
  if (!isImageUploaded.value || !uploadedFile.value) {
    message.warning('请先上传一张图片再发送！');
    return;
  }
  if (!selectedSteps.value.includes('step1')) {
    message.warning('请至少选择一个处理步骤才能提交！');
    return;
  }
  promptText.value = text;
  displayState.value = 'processing';
  leftPanelDisplay.value = 'status'; // 提交后，左侧默认显示状态监控
  processingProgress.value = 0;
  lossData.value = [];

  // 开始处理时重置图像的变换状态
  handleInitialization({ scale: 1, translateX: 0, translateY: 0 });

  if (processingInterval) clearInterval(processingInterval);
  processingInterval = setInterval(() => {
    if (processingProgress.value < 100) {
      processingProgress.value += 20;
      const newLoss = Math.random() * (0.8 - lossData.value.length * 0.1) + 0.1;
      lossData.value.push(parseFloat(newLoss.toFixed(2)));
    } else {
      clearInterval(processingInterval);
    }
  }, 900);

  message.loading('请求已提交，正在处理中...', { duration: 5000 });
  setTimeout(() => {
    clearInterval(processingInterval);
    processingProgress.value = 100;
    displayState.value = 'result'; // 模拟处理完成
  }, 5000);
};

// 切换左侧面板显示内容（状态监控 vs 原图）
const toggleLeftPanel = () => {
  leftPanelDisplay.value = leftPanelDisplay.value === 'status' ? 'original' : 'status';
};

// 更新图片预览的变换状态
const updateTransform = (newState) => {
  if (newState) {
    transformState.scale = newState.scale;
    transformState.translateX = newState.translateX;
    transformState.translateY = newState.translateY;
  }
};

// 初始化图片预览的变换状态
const handleInitialization = (initialState) => {
  updateTransform(initialState);
};

// 监听 isImageUploaded 状态的变化，在新图片上传后重置视图相关状态
watch(isImageUploaded, (newValue, oldValue) => {
  if (newValue && !oldValue) { // 仅当从无图片变为有图片时触发
    displayState.value = 'single'; // 新图片上传后默认显示单图模式
    leftPanelDisplay.value = 'status'; // 左侧面板默认显示状态
    handleInitialization({ scale: 1, translateX: 0, translateY: 0 }); // 重置图片变换状态
    // 重置模拟处理相关的状态，以便新图片有新的处理过程
    if (processingInterval) clearInterval(processingInterval);
    processingProgress.value = 0;
    lossData.value = [];
  }
});

// 组件卸载时进行清理
onUnmounted(() => {
  // 调用 useImageUploader 提供的清理函数来释放 Blob URL 资源
  cleanupUploader();
  // 清理模拟处理的定时器
  if (processingInterval) clearInterval(processingInterval);
});

</script>

<style scoped>
/* 样式内容保持不变，因为它已在 src/assets/views/demo-layout.css 中 */
</style>