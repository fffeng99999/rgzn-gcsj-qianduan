// src/views/Demo-test5-final.vue

<template>
  <div class="demo-page-container">
    <div class="chat-content-area" :class="{ 'side-by-side': displayState !== 'single' }">
      <ImageUploadPlaceholder v-if="!isImageUploaded" />

      <template v-if="isImageUploaded">
        <div class="image-preview-item left-panel-container">
          <ImagePreview
              v-if="displayState === 'single'"
              :image-url="imageUrl"
          />

          <template v-if="displayState !== 'single'">
            <Transition name="fade" mode="out-in">
              <StatusDisplayPreviewResult
                  v-if="leftPanelDisplay === 'status'"
                  :progress="processingProgress"
                  :loss-data="lossData"
              />
              <ImagePreview
                  v-else
                  :image-url="imageUrl"
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
              :title="leftPanelDisplay === 'status' ? '查看原图对比' : '查看处理监控'"
          >
            <template #icon><n-icon :component="SwapHorizontalOutline" /></template>
          </n-button>
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
import { SwapHorizontalOutline } from '@vicons/ionicons5';

// --- 导入所有子组件 ---
import ImageUploadPlaceholder from '@/components/ImageUploadPlaceholder.vue';
import ImagePreview from '@/components/ImagePreview.vue';
import ImagePreviewResult from '@/components/ImagePreviewResult.vue';
import StatusDisplayPreviewResult from '@/components/StatusDisplayPreviewResult.vue';
import ControlPanel from '@/components/ControlPanel4.vue';
import InputBar from '@/components/InputBar2.vue';
import FileDropOverlay from '@/components/FileDropOverlay.vue';
import ReportModal from '@/components/ReportModal.vue';

// --- 3. 导入所有 Composables ---
import { useImageUploader } from '@/composables/useImageUploader.js';
import { useDragAndDrop } from '@/composables/useDragAndDrop.js';
import { useProcessing } from '@/composables/useProcessing.js';
import { useImageTransform } from '@/composables/useImageTransform.js';
import { useReport } from '@/composables/useReport.js';

import '@/assets/views/demo-layout.css';


// --- 4. 初始化所有 Composables ---
const message = useMessage();
const { fileInputRef, isImageUploaded, imageUrl, handleUploadClick, handleFileChange, processAndSetFile, cleanup: cleanupUploader } = useImageUploader();
const { isDragging } = useDragAndDrop(processAndSetFile);
const { displayState, processingProgress, lossData, startProcessing, resetProcessingState, cleanup: cleanupProcessing } = useProcessing();
const { resetTransform } = useImageTransform();

// 报告 Composable 依赖 displayState 和 imageUrls
const resultImageUrl = computed(() => imageUrl.value); // 模拟结果图 URL
const { showReportModal, openReport, reportData } = useReport(displayState, imageUrl, resultImageUrl);


// --- 5. 仅保留指挥官角色所需的状态 ---
// 切换左右面板的显示状态
const leftPanelDisplay = ref('status');
// 需要在 ControlPanel 和 InputBar 之间共享的步骤
const selectedSteps = ref(['step1']);


// --- 6. 仅保留指挥官角色的方法 ---
// 负责协调，调用各个 Composable 的功能
const handleSend = () => {
  if (!isImageUploaded.value) return message.warning('请先上传一张图片再发送！');
  if (!selectedSteps.value.length) return message.warning('请至少选择一个处理步骤！');

  // resetTransform(); // 重置图像视图
  leftPanelDisplay.value = 'status';
  startProcessing(); // 开始处理流程
};

const toggleLeftPanel = () => {
  leftPanelDisplay.value = leftPanelDisplay.value === 'status' ? 'original' : 'status';
};


// --- 7. 监听和生命周期钩子 ---
watch(isImageUploaded, (isNew) => {
  if (isNew) {
    resetProcessingState(); // 重置处理状态
    // resetTransform();       // 重置图像视图
  }
});

onUnmounted(() => {
  cleanupUploader();
  cleanupProcessing();
});
</script>