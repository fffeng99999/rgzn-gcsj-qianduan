// src/components/ImagePreviewResult.vue

<template>
  <div class="image-preview-wrapper">
    <div
        ref="containerEl" class="image-preview-container"
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
          @dblclick="resetTransform"
          @load="initializeImageTransform" />
    </div>
  </div>
</template>

<script setup>
// ✨ 2. 新增：引入 NButton, NIcon, NTooltip 和下载图标
import { ref, computed } from 'vue';
import { NButton, NIcon, NTooltip } from 'naive-ui';
import { DownloadOutline } from '@vicons/ionicons5';

// props 和 emits 定义与 ImagePreview.vue 完全一致
const props = defineProps({
  imageUrl: {
    type: String,
    required: true,
  },
  transformState: {
    type: Object,
    required: true,
    default: () => ({ scale: 1, translateX: 0, translateY: 0 })
  },
});
const emit = defineEmits(['update:transform', 'initialized']);

// --- 内部状态和变换逻辑与 ImagePreview.vue 完全相同 ---
const imageEl = ref(null);
const containerEl = ref(null);
const isPanning = ref(false);
const startDrag = ref({ x: 0, y: 0 });
const imageStyle = computed(() => ({
  transform: `scale(${props.transformState.scale}) translate(${props.transformState.translateX}px, ${props.transformState.translateY}px)`,
}));
const initializeImageTransform = () => {
  if (!imageEl.value || !containerEl.value || !imageEl.value.naturalWidth) return;
  const { naturalWidth: imgWidth, naturalHeight: imgHeight } = imageEl.value;
  const { clientWidth: containerWidth, clientHeight: containerHeight } = containerEl.value;
  const scaleX = containerWidth / imgWidth;
  const scaleY = containerHeight / imgHeight;
  const newScale = Math.min(scaleX, scaleY);
  emit('initialized', { scale: newScale, translateX: 0, translateY: 0 });
};
const handleWheel = (event) => {
  const scaleAmount = 0.1;
  const currentScale = props.transformState.scale;
  const minScale = 0.2;
  const maxScale = 5;
  let newScale;
  if (event.deltaY > 0) {
    newScale = Math.max(minScale, currentScale - scaleAmount);
  } else {
    newScale = Math.min(maxScale, currentScale + scaleAmount);
  }
  emit('update:transform', { ...props.transformState, scale: newScale });
};
const handleMouseDown = (event) => {
  event.preventDefault();
  isPanning.value = true;
  startDrag.value = {
    x: event.clientX - props.transformState.translateX * props.transformState.scale,
    y: event.clientY - props.transformState.translateY * props.transformState.scale,
  };
};
const handleMouseMove = (event) => {
  if (isPanning.value) {
    event.preventDefault();
    const newTranslateX = (event.clientX - startDrag.value.x) / props.transformState.scale;
    const newTranslateY = (event.clientY - startDrag.value.y) / props.transformState.scale;
    emit('update:transform', { ...props.transformState, translateX: newTranslateX, translateY: newTranslateY });
  }
};
const handleMouseUp = () => { isPanning.value = false; };
const handleMouseLeave = () => { isPanning.value = false; };
const resetTransform = () => {
  emit('update:transform', { scale: 1, translateX: 0, translateY: 0 });
};

// ✨ 3. 新增：下载图片的逻辑
const handleDownload = () => {
  if (!props.imageUrl) return;
  const link = document.createElement('a');
  link.href = props.imageUrl;
  const fileName = props.imageUrl.split('/').pop().split('#')[0].split('?')[0] || 'result.png';
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
</script>

<style scoped>
/* ✨ 4. 样式与您提供的 ImagePreview.vue 完全一致，仅增加下载按钮的样式 */
.image-preview-wrapper {
  flex-grow: 1;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 16px 0;
  animation: slide-up-fade-in 0.5s ease-out;
}
.image-preview-container {
  width: 90%;
  max-width: 900px;
  height: 80vh;
  max-height: 600px;
  border: 1px solid var(--n-border-color);
  border-radius: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 16px;
  background-color: var(--card-color-imgpv-bg);
  box-shadow: var(--component-shadow);
  transition: all 0.3s ease;
  overflow: hidden;
  position: relative; /* 为绝对定位的下载按钮提供上下文 */
}
.preview-image {
  border-radius: 8px;
  cursor: grab;
  transition: transform 0.2s ease-out;
  transform-origin: center;
}
.preview-image.is-panning {
  cursor: grabbing;
}
@keyframes slide-up-fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ✨ 5. 新增：下载按钮的样式 */
.download-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 10;
  font-size: 18px;
  background-color: rgba(0, 0, 0, 0.2);
  color: white;
}
.download-btn:hover {
  background-color: rgba(0, 0, 0, 0.4);
}
</style>