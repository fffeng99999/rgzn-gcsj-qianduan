// src/components/ImagePreviewResult.vue

<template>
  <div class="image-preview-wrapper">
    <div
        ref="containerEl"
        class="image-preview-container"
        @mousedown="handleMouseDown"
        @mousemove="handleMouseMove"
        @mouseup="handleMouseUp"
        @mouseleave="handleMouseLeave"
    >
      <n-tooltip trigger="hover">
        <template #trigger>
          <n-button
              class="download-btn"
              circle
              quaternary
              @click.stop="handleDownload"
          >
            <template #icon>
              <n-icon :component="DownloadOutline" />
            </template>
          </n-button>
        </template>
        下载图片
      </n-tooltip>

      <img
          ref="imageEl"
          v-if="imageUrl"
          :src="imageUrl"
          alt="Image preview"
          class="preview-image"
          :style="imageStyle"
          :class="{ 'is-panning': isPanning }"
          @wheel.prevent="handleWheel"
          @dblclick="handleDblClickReset"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { NButton, NIcon, NTooltip } from 'naive-ui';
import { DownloadOutline } from '@vicons/ionicons5';
import { useImageTransform } from '@/composables/useImageTransform';
import '@/assets/components/ImagePreviewResult.css';

// --- Props ---
const props = defineProps({
  imageUrl: {
    type: String,
    required: true,
  },
});

// --- Composables ---
const { transformState, updateTransform, resetTransform } = useImageTransform();

// --- 内部状态（仅用于交互过程） ---
const imageEl = ref(null);
const containerEl = ref(null);
const isPanning = ref(false);
const startDrag = ref({ x: 0, y: 0 });

// --- Computed ---
const imageStyle = computed(() => ({
  transform: `scale(${transformState.scale}) translate(${transformState.translateX}px, ${transformState.translateY}px)`,
}));

// --- Methods ---
const reinitializeTransform = () => {
  if (!imageEl.value || !containerEl.value || !imageEl.value.naturalWidth) return;
  const { naturalWidth: imgWidth, naturalHeight: imgHeight } = imageEl.value;
  const { clientWidth: containerWidth, clientHeight: containerHeight } = containerEl.value;
  const scaleX = containerWidth / imgWidth;
  const scaleY = containerHeight / imgHeight;
  const newScale = Math.min(scaleX, scaleY);
  resetTransform({ scale: newScale, translateX: 0, translateY: 0 });
};

const handleWheel = (event) => {
  const scaleAmount = 0.1;
  const currentScale = transformState.scale;
  const minScale = 0.2;
  const maxScale = 5;

  let newScale;
  if (event.deltaY > 0) {
    newScale = Math.max(minScale, currentScale - scaleAmount);
  } else {
    newScale = Math.min(maxScale, currentScale + scaleAmount);
  }

  updateTransform({ ...transformState, scale: newScale });
};

const handleMouseDown = (event) => {
  event.preventDefault();
  isPanning.value = true;
  startDrag.value = {
    x: event.clientX - transformState.translateX * transformState.scale,
    y: event.clientY - transformState.translateY * transformState.scale,
  };
};

const handleMouseMove = (event) => {
  if (isPanning.value) {
    event.preventDefault();
    const newTranslateX = (event.clientX - startDrag.value.x) / transformState.scale;
    const newTranslateY = (event.clientY - startDrag.value.y) / transformState.scale;
    updateTransform({ ...transformState, translateX: newTranslateX, translateY: newTranslateY });
  }
};

const handleMouseUp = () => { isPanning.value = false; };
const handleMouseLeave = () => { isPanning.value = false; };

const handleDblClickReset = () => {
  reinitializeTransform();
};

// --- 下载逻辑（此组件特有功能）---
const handleDownload = () => {
  if (!props.imageUrl) return;

  // Create a temporary anchor element
  const link = document.createElement('a');
  link.href = props.imageUrl;
  // Set the download attribute to force download and optionally specify a filename
  // You might want to extract the filename from the imageUrl or provide a default
  link.download = 'downloaded_image.png'; // You can customize the filename here
  link.target = '_blank'; // Open in a new tab

  // Append to body, click, and remove
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
</script>

<style scoped>
/* 样式可以保持不变 */
</style>

<!--<template>-->
<!--  <div class="image-preview-wrapper">-->
<!--    <div-->
<!--        ref="containerEl"-->
<!--        class="image-preview-container"-->
<!--        @mousedown="handleMouseDown"-->
<!--        @mousemove="handleMouseMove"-->
<!--        @mouseup="handleMouseUp"-->
<!--        @mouseleave="handleMouseLeave"-->
<!--    >-->
<!--      <n-tooltip trigger="hover">-->
<!--        <template #trigger>-->
<!--          <n-button-->
<!--              class="download-btn"-->
<!--              circle-->
<!--              quaternary-->
<!--              @click.stop="handleDownload"-->
<!--          >-->
<!--            <template #icon>-->
<!--              <n-icon :component="DownloadOutline" />-->
<!--            </template>-->
<!--          </n-button>-->
<!--        </template>-->
<!--        下载图片-->
<!--      </n-tooltip>-->

<!--      <img-->
<!--          ref="imageEl"-->
<!--          v-if="imageUrl"-->
<!--          :src="imageUrl"-->
<!--          alt="Image preview"-->
<!--          class="preview-image"-->
<!--          :style="imageStyle"-->
<!--          :class="{ 'is-panning': isPanning }"-->
<!--          @wheel.prevent="handleWheel"-->
<!--          @dblclick="handleDblClickReset"-->
<!--      />-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<script setup>-->
<!--import { ref, computed } from 'vue';-->
<!--import { NButton, NIcon, NTooltip } from 'naive-ui';-->
<!--import { DownloadOutline } from '@vicons/ionicons5';-->
<!--import { useImageTransform } from '@/composables/useImageTransform'; // ✨ 1. 引入共享的 Composable-->
<!--import '@/assets/components/ImagePreviewResult.css';-->

<!--// -&#45;&#45; Props -&#45;&#45;-->
<!--// ✨ 2. Props 中不再需要 transformState-->
<!--const props = defineProps({-->
<!--  imageUrl: {-->
<!--    type: String,-->
<!--    required: true,-->
<!--  },-->
<!--});-->

<!--// -&#45;&#45; Composables -&#45;&#45;-->
<!--// ✨ 3. 和 ImagePreview.vue 一样，直接从 Composable 获取共享状态和方法-->
<!--const { transformState, updateTransform, resetTransform } = useImageTransform();-->

<!--// -&#45;&#45; 内部状态（仅用于交互过程） -&#45;&#45;-->
<!--const imageEl = ref(null);-->
<!--const containerEl = ref(null);-->
<!--const isPanning = ref(false);-->
<!--const startDrag = ref({ x: 0, y: 0 });-->

<!--// -&#45;&#45; Computed -&#45;&#45;-->
<!--// ✨ 4. 图像样式直接使用来自 Composable 的共享状态-->
<!--const imageStyle = computed(() => ({-->
<!--  transform: `scale(${transformState.scale}) translate(${transformState.translateX}px, ${transformState.translateY}px)`,-->
<!--}));-->

<!--// -&#45;&#45; Methods -&#45;&#45;-->
<!--// ✨ 5. 不再需要 emit 事件，而是直接调用 Composable 中的方法-->
<!--// 注意：此组件不需要 `initializeImageTransform`，因为状态由 ImagePreview 初始化。-->
<!--// 但我们保留重置逻辑，以便双击时能恢复视图。-->
<!--const reinitializeTransform = () => {-->
<!--  if (!imageEl.value || !containerEl.value || !imageEl.value.naturalWidth) return;-->
<!--  const { naturalWidth: imgWidth, naturalHeight: imgHeight } = imageEl.value;-->
<!--  const { clientWidth: containerWidth, clientHeight: containerHeight } = containerEl.value;-->
<!--  const scaleX = containerWidth / imgWidth;-->
<!--  const scaleY = containerHeight / imgHeight;-->
<!--  const newScale = Math.min(scaleX, scaleY);-->
<!--  resetTransform({ scale: newScale, translateX: 0, translateY: 0 });-->
<!--};-->

<!--const handleWheel = (event) => {-->
<!--  const scaleAmount = 0.1;-->
<!--  const currentScale = transformState.scale;-->
<!--  const minScale = 0.2;-->
<!--  const maxScale = 5;-->

<!--  let newScale;-->
<!--  if (event.deltaY > 0) {-->
<!--    newScale = Math.max(minScale, currentScale - scaleAmount);-->
<!--  } else {-->
<!--    newScale = Math.min(maxScale, currentScale + scaleAmount);-->
<!--  }-->

<!--  updateTransform({ ...transformState, scale: newScale });-->
<!--};-->

<!--const handleMouseDown = (event) => {-->
<!--  event.preventDefault();-->
<!--  isPanning.value = true;-->
<!--  startDrag.value = {-->
<!--    x: event.clientX - transformState.translateX * transformState.scale,-->
<!--    y: event.clientY - transformState.translateY * transformState.scale,-->
<!--  };-->
<!--};-->

<!--const handleMouseMove = (event) => {-->
<!--  if (isPanning.value) {-->
<!--    event.preventDefault();-->
<!--    const newTranslateX = (event.clientX - startDrag.value.x) / transformState.scale;-->
<!--    const newTranslateY = (event.clientY - startDrag.value.y) / transformState.scale;-->
<!--    updateTransform({ ...transformState, translateX: newTranslateX, translateY: newTranslateY });-->
<!--  }-->
<!--};-->

<!--const handleMouseUp = () => { isPanning.value = false; };-->
<!--const handleMouseLeave = () => { isPanning.value = false; };-->

<!--const handleDblClickReset = () => {-->
<!--  reinitializeTransform();-->
<!--};-->

<!--// -&#45;&#45; 下载逻辑（此组件特有功能）-&#45;&#45;-->
<!--const handleDownload = () => {-->
<!--  if (!props.imageUrl) return;-->
<!--  const link = document.createElement('a');-->
<!--  link.href = props.imageUrl;-->

<!--  // 尝试生成一个更有意义的文件名-->
<!--  const baseName = props.imageUrl.split('/').pop().split('#')[0].split('?')[0] || 'result';-->
<!--  const fileName = baseName.includes('.')-->
<!--      ? `${baseName.substring(0, baseName.lastIndexOf('.'))}_result.${baseName.substring(baseName.lastIndexOf('.') + 1)}`-->
<!--      : `${baseName}_result.png`;-->

<!--  link.download = fileName;-->
<!--  document.body.appendChild(link);-->
<!--  link.click();-->
<!--  document.body.removeChild(link);-->
<!--};-->
<!--</script>-->

<!--<style scoped>-->
<!--/* 样式可以保持不变 */-->
<!--</style>-->