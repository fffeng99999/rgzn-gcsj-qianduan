// src/views/Demo-test5-final.vue

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
            @update:advanced-settings="advancedSettings = $event"
        />
      </div>
    </Transition>

    <div class="input-wrapper">
      <InputBar
          :is-image-uploaded="isImageUploaded"
          :selectedSteps="selectedSteps"
          :is-processing="isLoading"
          v-model:selected-model="selectedModel"
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
import { ref, watch, onUnmounted } from 'vue';
import { useMessage } from 'naive-ui';

// ✨ 1. Import the new API service
import { processImageWithMetadata } from '@/services/apiService.js';

// --- Component Imports (preserved) ---
import ImageUploadPlaceholder from '@/components/ImageUploadPlaceholder.vue';
import ImagePreview from '@/components/ImagePreview.vue';
import ImagePreviewResult from '@/components/ImagePreviewResult.vue';
import ControlPanel from '@/components/ControlPanel4.vue';
import InputBar from '@/components/InputBar2.vue';
import FileDropOverlay from '@/components/FileDropOverlay.vue';
import ReportModal from '@/components/ReportModal.vue';

// --- Composables Imports (simplified) ---
import { useImageUploader } from '@/composables/useImageUploader.js';
import { useDragAndDrop } from '@/composables/useDragAndDrop.js';
import { useImageTransform } from '@/composables/useImageTransform.js';
import { useReport } from '@/composables/useReport.js';

import '@/assets/views/demo-layout.css';


// --- Composables Initialization ---
const message = useMessage();
// ✨ 'uploadedFile' is crucial for the API call
const { fileInputRef, uploadedFile, isImageUploaded, imageUrl, handleUploadClick, handleFileChange, processAndSetFile, cleanup: cleanupUploader } = useImageUploader();
const { isDragging } = useDragAndDrop(processAndSetFile);
const { resetTransform } = useImageTransform();

// ✨ 2. State management is rewritten for real API calls
const displayState = ref('single');
const isLoading = ref(false);
const resultImageUrl = ref(null); // This is now a ref to hold the backend response URL

// ✨ 3. Add state to hold all data from child components before sending
const selectedSteps = ref(['step1']);
const advancedSettings = ref({});
const selectedModel = ref('unet_best.pth'); // A default value

// The useReport composable now gets a proper ref for resultImageUrl
const { showReportModal, openReport, reportData } = useReport(displayState, imageUrl, resultImageUrl);

// --- Methods ---
/**
 * ✨ 4. The handleSend function is completely replaced with real logic.
 * This is the core of the fix.
 * @param {string} promptText The prompt from the InputBar component.
 */
const handleSend = async (promptText) => {
  if (!selectedSteps.value.includes('step1')) {
    message.warning('必须选择“轮廓增强 (Step 1)”才能提交处理！');
    return; // Stop the function from proceeding
  }

  if (!uploadedFile.value) return message.warning('请先上传一张图片再发送！');
  if (isLoading.value) return; // Prevent duplicate requests

  isLoading.value = true;
  displayState.value = 'processing';
  const loadingMessage = message.loading('正在处理请求...', { duration: 0 });

  try {
    // A. GATHER all data into the required JSON format.
    const metadata = {
      steps: selectedSteps.value.reduce((acc, step) => ({ ...acc, [step]: true }), { step1: false, step2: false, step3: false }),
      advancedParams: advancedSettings.value,
      model: selectedModel.value,
      prompt: promptText,
    };

    // B. CALL the API service with the file and metadata.
    const response = await processImageWithMetadata(uploadedFile.value, metadata);

    // C. HANDLE a successful response.
    if (response?.status === 'success') {
      resultImageUrl.value = response.processed_image_url;
      displayState.value = 'result';
      message.success(`处理成功！耗时: ${response.processing_time}`);
    } else {
      throw new Error(response?.error || '后端返回了失败状态。');
    }
  } catch (err) {
    // D. HANDLE any kind of error during the process.
    message.error(err.error || err.message || '发生未知错误。');
    displayState.value = 'single';
  } finally {
    // E. ALWAYS reset the loading state.
    loadingMessage.destroy();
    isLoading.value = false;
  }
};


// --- Watchers & Lifecycle ---
watch(isImageUploaded, (isNew) => {
  if (isNew) {
    // Reset the view when a new image is uploaded
    displayState.value = 'single';
    resultImageUrl.value = null;
    resetTransform();
  }
});

onUnmounted(() => {
  cleanupUploader();
});
</script>
<<<<<<< HEAD
=======




>>>>>>> 7a887e08bad3f67f5ba7643fee66ec61202038b4
