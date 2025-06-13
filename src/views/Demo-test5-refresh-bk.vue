// src/views/Demo-test5-refresh3.vue

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
import { ref, reactive, onUnmounted, computed } from 'vue';
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

// --- State and Props ---
const message = useMessage();
const fileInputRef = ref(null);
const uploadedFile = ref(null);
const isImageUploaded = ref(false);
const imageUrl = ref(null);
const resultImageUrl = computed(() => imageUrl.value); // 假定结果图与原图URL相同，实际应替换为超分结果URL
const displayState = ref('single'); // 'single', 'processing', 'result'
const leftPanelDisplay = ref('status'); // 'status' or 'original' - 新增状态，控制左侧面板内容
const selectedSteps = ref(['step1']);
const promptText = ref('');
let processingInterval = null;
const processingProgress = ref(0);
const lossData = ref([]);
const transformState = reactive({ scale: 1, translateX: 0, translateY: 0 });
const { isDragging } = useDragAndDrop(processFiles);
const showReportModal = ref(false);

// --- Mock Data for Report ---
const mockComparisonImages = computed(() => [
  { label: '原始图像', src: imageUrl.value },
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
    displayState.value = 'result'; // 处理完成
  }, 5000);
};

// ✨ 新的切换函数：用于切换左侧面板内容
const toggleLeftPanel = () => {
  leftPanelDisplay.value = leftPanelDisplay.value === 'status' ? 'original' : 'status';
};

const updateTransform = (newState) => {
  if (newState) {
    transformState.scale = newState.scale;
    transformState.translateX = newState.translateX;
    transformState.translateY = newState.translateY;
  }
};

const handleInitialization = (initialState) => {
  updateTransform(initialState);
};

const handleUploadClick = () => { fileInputRef.value?.click(); };

const handleFileChange = (e) => {
  processFiles(e.target.files);
  if (e.target) e.target.value = '';
};

function processFiles(files) {
  if (!files || files.length === 0) return;
  const file = files[0];
  if (file && file.type.startsWith('image/')) {
    message.success(`图片 ${file.name} 已接收！`);
    if (imageUrl.value) URL.revokeObjectURL(imageUrl.value);

    // 重置所有状态
    displayState.value = 'single';
    leftPanelDisplay.value = 'status';
    handleInitialization({ scale: 1, translateX: 0, translateY: 0 });

    uploadedFile.value = file;
    imageUrl.value = URL.createObjectURL(file);
    isImageUploaded.value = true;
  } else {
    message.error('请只上传图片文件！');
  }
}

onUnmounted(() => {
  if (imageUrl.value) URL.revokeObjectURL(imageUrl.value);
  if (processingInterval) clearInterval(processingInterval);
});

</script>

<style scoped>
/* ✨ 新增 left-panel-container 样式，使其可以容纳绝对定位的按钮 */
.left-panel-container {
  position: relative;
}

/* ✨ 将切换按钮样式应用到左侧面板 */
.view-toggle-button {
  position: absolute;
  bottom: 16px;
  left: 32px;
  z-index: 10;
  background-color: rgba(255, 255, 255, 0.6) !important;
  backdrop-filter: blur(5px);
  --n-border: 1px solid rgba(0, 0, 0, 0.1) !important;
}

.demo-page-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: var(--n-color);
}

.chat-content-area {
  flex-grow: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: all 0.5s ease-in-out;
}

.chat-content-area.side-by-side {
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
}

.image-preview-item {
  flex-grow: 1;
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  transition: width 0.5s ease-in-out, opacity 0.3s ease;
}

.chat-content-area.side-by-side .image-preview-item {
  width: 50%;
  border-left: 1px solid var(--n-border-color);
}
.chat-content-area.side-by-side .image-preview-item:first-child {
  border-left: none;
}

.placeholder-box {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 24px;
  width: 100%;
  height: 100%;
}

.placeholder-content {
  width: 100%;
  max-width: 900px;
  height: 80vh;
  max-height: 600px;
  border: 2px dashed var(--n-border-color);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 16px;
}

.controls-wrapper {
  flex-shrink: 0;
  padding: 16px 24px 16px 24px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
}

.input-wrapper {
  flex-shrink: 0;
  padding: 8px 24px 24px 24px;
  width: 100%;
  box-sizing: border-box;
  background-color: var(--n-color);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.5s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.slide-in-right-enter-active {
  transition: transform 0.5s ease-out;
}

.slide-in-right-enter-from {
  transform: translateX(100%);
}
</style>