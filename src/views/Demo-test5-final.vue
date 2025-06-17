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
            v-model:advanced-settings="advancedSettings"
            :show-report-button="displayState === 'result'"
            @show-report="openReport"
        />
      </div>
    </Transition>

    <div class="input-wrapper">
      <InputBar
          :is-image-uploaded="isImageUploaded"
          :selected-steps="selectedSteps"
          :is-processing="isLoading"
          :model-options="modelOptions"
          v-model:selected-model="selectedModel"
          @send="handleSend"
          @upload="handleUploadClick"
      />
    </div>

    <input ref="fileInputRef" type="file" accept="image/*" style="display: none" @change="handleFileChange"/>
    <FileDropOverlay v-if="isDragging" />

<!--    <ReportModal-->
<!--        v-model:show="showReportModal"-->
<!--        :selected-steps="selectedSteps"-->
<!--        :comparison-images="reportData.comparisonImages"-->
<!--        :gif-url="reportData.gifUrl"-->
<!--        :metrics="reportData.metrics"-->
<!--    />-->
    <ReportModal
        v-if="fullReportData"
        v-model:show="showReportModal"
        :selected-steps="selectedSteps"
        :comparison-images="fullReportData.comparisonImages"
        :gif-url="fullReportData.gifUrl"
        :metrics="fullReportData.metrics"
        :pdf-url="fullReportData.pdfUrl"
    />
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue';
import { useMessage } from 'naive-ui';
import { processImageWithMetadata, listAvailableModels, fetchModelParameters } from '@/services/apiService.js';
import { fetchReportData } from '@/services/reportService.js'; // 导入新的 service


// Component Imports
import ImageUploadPlaceholder from '@/components/ImageUploadPlaceholder.vue';
import ImagePreview from '@/components/ImagePreview.vue';
import ImagePreviewResult from '@/components/ImagePreviewResult.vue';
import ControlPanel from '@/components/ControlPanel4.vue';
import InputBar from '@/components/InputBar2.vue';
import FileDropOverlay from '@/components/FileDropOverlay.vue';
import ReportModal from '@/components/ReportModal.vue';

// Composables
import { useImageUploader } from '@/composables/useImageUploader.js';
import { useDragAndDrop } from '@/composables/useDragAndDrop.js';
import { useImageTransform } from '@/composables/useImageTransform.js';
import { useReport } from '@/composables/useReport.js';

import '@/assets/views/demo-layout.css';

// --- State Management ---
const message = useMessage();
const { fileInputRef, uploadedFile, isImageUploaded, imageUrl, handleUploadClick, handleFileChange, processAndSetFile, cleanup: cleanupUploader } = useImageUploader();
const { isDragging } = useDragAndDrop(processAndSetFile);
const { resetTransform } = useImageTransform();




// Real API call state
const displayState = ref('single');
const isLoading = ref(false);
const resultImageUrl = ref(null);

// State for model and parameters
const modelOptions = ref([]);
const modelParametersCache = ref({});
const selectedModel = ref(null); // Default to null, will be set on load
const selectedSteps = ref([]);
const advancedSettings = ref({});




// Report
// const { showReportModal, openReport, reportData } = useReport(displayState, imageUrl, resultImageUrl);

const showReportModal = ref(false); // ✨ 2. 直接在这里管理模态框状态
const fullReportData = ref(null);   // ✨ 3. 新增 ref 用于存储报告数据

// --- Core Logic ---
const handleSend = async (promptText) => {
  if (!selectedSteps.value.includes('step1')) {
    message.warning('必须选择“轮廓增强 (Step 1)”才能提交处理！');
    return;
  }
  if (!uploadedFile.value) return message.warning('请先上传一张图片再发送！');
  if (isLoading.value) return;

  isLoading.value = true;
  displayState.value = 'processing';
  fullReportData.value = null; // 重置旧报告
  const loadingMessage = message.loading('正在处理请求...', { duration: 0 });

  try {
    const fullParameters = {
      steps: selectedSteps.value.reduce((acc, step) => ({ ...acc, [step]: true }), { step1: false, step2: false, step3: false }),
      advancedParams: advancedSettings.value,
      model: selectedModel.value, // Use the actual model file name
      prompt: promptText,
    };

    const metadata = { parameters: fullParameters };

    // const response = await processImageWithMetadata(uploadedFile.value, metadata);
    const processResponse = await processImageWithMetadata(uploadedFile.value, metadata);

    if (processResponse?.status === 'success') {
      resultImageUrl.value = processResponse.processed_image_url;
      displayState.value = 'result';
      message.success(`处理成功！耗时: ${processResponse.processing_time}`);

      // ✨ 4. 立即获取详细报告
      const reportInfo = {
        report_id: processResponse.report_id,
        original_filename: processResponse.original_filename,
        processed_filename: processResponse.processed_filename,
        parameters: processResponse.parameters
      };
      fullReportData.value = await fetchReportData(reportInfo);

    } else {
      throw new Error(processResponse?.error || '后端返回了失败状态。');
    }
  } catch (err) {
    message.error(err.error || err.message || '发生未知错误。');
    displayState.value = 'single';
  } finally {
    loadingMessage.destroy();
    isLoading.value = false;
  }
};

//     if (response?.status === 'success') {
//       resultImageUrl.value = response.processed_image_url;
//       displayState.value = 'result';
//       message.success(`处理成功！耗时: ${response.processing_time}`);
//     } else {
//       throw new Error(response?.error || '后端返回了失败状态。');
//     }
//   } catch (err) {
//     message.error(err.error || err.message || '发生未知错误。');
//     displayState.value = 'single';
//   } finally {
//     loadingMessage.destroy();
//     isLoading.value = false;
//   }
// };

// ✨ 5. 打开报告的逻辑
const openReport = () => {
  if (!fullReportData.value) {
    message.warning('报告数据仍在加载中或加载失败，请稍候。');
    return;
  }
  showReportModal.value = true;
}

// --- Watchers & Lifecycle ---
watch(isImageUploaded, (isNew) => {
  if (isNew) {
    displayState.value = 'single';
    resultImageUrl.value = null;
    resetTransform();
    // When a new image is uploaded, apply the default/current model's parameters
    if(selectedModel.value && modelParametersCache.value[selectedModel.value]) {
      const params = modelParametersCache.value[selectedModel.value];
      advancedSettings.value = params.advancedParams;
      selectedSteps.value = Object.keys(params.steps).filter(key => params.steps[key]);
    }
  }
});

watch(selectedModel, (newModelName) => {
  if (newModelName && modelParametersCache.value[newModelName]) {
    const params = modelParametersCache.value[newModelName];
    advancedSettings.value = params.advancedParams;
    selectedSteps.value = Object.keys(params.steps).filter(key => params.steps[key]);
  }
});

onMounted(async () => {
  try {
    const modelNames = await listAvailableModels();
    if (modelNames && modelNames.length > 0) {
      modelOptions.value = modelNames.map(name => ({ label: name.replace(/_/g, ' '), value: name }));

      // Fetch all parameters and cache them
      const fetchPromises = modelNames.map(name =>
          fetchModelParameters(name).then(params => ({ name, params }))
      );
      const allParams = await Promise.all(fetchPromises);
      allParams.forEach(({ name, params }) => {
        modelParametersCache.value[name] = params;
      });

      // Set the first model as the default
      selectedModel.value = modelNames[0];
    }
  } catch (error) {
    message.error("加载模型列表失败: " + error.message);
  }
});

onUnmounted(() => {
  cleanupUploader();
});
</script>