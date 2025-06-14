<template>
  <div class="demo-page-container">
    <div class="chat-content-area" :class="{ 'side-by-side': displayState !== 'single' }">
      <ImageUploadPlaceholder v-if="!isImageUploaded" />

      <template v-if="isImageUploaded">
        <div class="image-preview-item left-panel-container">
          <ImagePreview :image-url="imageUrl" />
        </div>

        <Transition name="slide-in-right">
          <div v-if="displayState !== 'single'" class="image-preview-item">
            <ImagePreviewResult :image-url="resultImageUrl" />
          </div>
        </Transition>
      </template>
    </div>

    <Transition name="slide-up">
      <div v-if="isImageUploaded" class="controls-wrapper">
        <ControlPanel
            v-model:selected-steps="selectedSteps"
            :show-report-button="displayState === 'result'"
            @show-report="openReport"
        />
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
    <FileDropOverlay v-if="isDragging" />

    <ReportModal
        v-model:show="showReportModal"
        :selected-steps="selectedSteps"
        :comparison-images="reportData.comparisonImages"
        :gif-url="reportData.gifUrl"
        :metrics="reportData.metrics"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from 'vue';
import { useMessage, NButton, NIcon } from 'naive-ui';
// 2. 移除不再需要的图标
// import { SwapHorizontalOutline } from '@vicons/ionicons5';

// --- 导入所有子组件 ---
import ImageUploadPlaceholder from '@/components/ImageUploadPlaceholder.vue';
import ImagePreview from '@/components/ImagePreview.vue';
import ImagePreviewResult from '@/components/ImagePreviewResult.vue';
// 2. 移除不再需要的组件
// import StatusDisplayPreviewResult from '@/components/StatusDisplayPreviewResult.vue';
import ControlPanel from '@/components/ControlPanel4.vue';
import InputBar from '@/components/InputBar2.vue';
import FileDropOverlay from '@/components/FileDropOverlay.vue';
import ReportModal from '@/components/ReportModal.vue';

// --- 导入所有 Composables ---
import { useImageUploader } from '@/composables/useImageUploader.js';
import { useDragAndDrop } from '@/composables/useDragAndDrop.js';
import { useProcessing } from '@/composables/useProcessing.js';
import { useImageTransform } from '@/composables/useImageTransform.js';
import { useReport } from '@/composables/useReport.js';

import '@/assets/views/demo-layout.css';


// --- 初始化所有 Composables ---
const message = useMessage();
const { fileInputRef, isImageUploaded, imageUrl, handleUploadClick, handleFileChange, processAndSetFile, cleanup: cleanupUploader } = useImageUploader();
const { isDragging } = useDragAndDrop(processAndSetFile);
// 2. 从 useProcessing 中解构出的 progress 和 lossData 不再需要在模板中使用，但逻辑可保留
const { displayState, processingProgress, lossData, startProcessing, resetProcessingState, cleanup: cleanupProcessing } = useProcessing();
const { resetTransform } = useImageTransform();
const resultImageUrl = computed(() => imageUrl.value);
const { showReportModal, openReport, reportData } = useReport(displayState, imageUrl, resultImageUrl);


// 3. 移除不再需要的状态
// const leftPanelDisplay = ref('status');
const selectedSteps = ref(['step1']);


// --- 方法 ---
const handleSend = () => {
  if (!isImageUploaded.value) return message.warning('请先上传一张图片再发送！');
  if (!selectedSteps.value.length) return message.warning('请至少选择一个处理步骤！');

  // 3. 移除对 leftPanelDisplay 的设置
  // leftPanelDisplay.value = 'status';
  startProcessing();
};

// 3. 移除不再需要的方法
// const toggleLeftPanel = () => { ... };


// --- 监听和生命周期钩子 ---
watch(isImageUploaded, (isNew) => {
  if (isNew) {
    resetProcessingState();
  }
});

onUnmounted(() => {
  cleanupUploader();
  cleanupProcessing();
});
</script>