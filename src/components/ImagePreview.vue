// src/components/ImagePreview.vue

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
          @load="initializeImageTransform"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useImageTransform } from '@/composables/useImageTransform'; // ✨ 1. 引入新的 Composable
import '@/assets/components/ImagePreview.css';

// --- Props ---
// ✨ 2. Props 中不再需要 transformState
const props = defineProps({
  imageUrl: {
    type: String,
    required: true,
  },
});

// --- Composables ---
// ✨ 3. 直接从 Composable 获取共享状态和方法
const { transformState, updateTransform, resetTransform } = useImageTransform();

// --- 内部状态（仅用于交互过程） ---
const imageEl = ref(null);
const containerEl = ref(null);
const isPanning = ref(false);
const startDrag = ref({ x: 0, y: 0 });

// --- Computed ---
// ✨ 4. 图像样式直接使用来自 Composable 的共享状态
const imageStyle = computed(() => ({
  transform: `scale(${transformState.scale}) translate(${transformState.translateX}px, ${transformState.translateY}px)`,
}));

// --- Methods ---
// ✨ 5. 不再需要 emit 事件，而是直接调用 Composable 中的方法
const initializeImageTransform = () => {
  if (!imageEl.value || !containerEl.value || !imageEl.value.naturalWidth) return;

  const { naturalWidth: imgWidth, naturalHeight: imgHeight } = imageEl.value;
  const { clientWidth: containerWidth, clientHeight: containerHeight } = containerEl.value;

  const scaleX = containerWidth / imgWidth;
  const scaleY = containerHeight / imgHeight;
  const newScale = Math.min(scaleX, scaleY);

  // 直接调用 Composable 的 reset 方法来设置理想的初始状态
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

  // 直接调用 Composable 的 update 方法
  updateTransform({ ...transformState, scale: newScale });
};

const handleMouseDown = (event) => {
  event.preventDefault();
  isPanning.value = true;
  // 直接从 Composable 读取状态
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
    // 直接调用 Composable 的 update 方法
    updateTransform({ ...transformState, translateX: newTranslateX, translateY: newTranslateY });
  }
};

const handleMouseUp = () => { isPanning.value = false; };
const handleMouseLeave = () => { isPanning.value = false; };

// 双击重置，调用 initialize 重新计算并设置
const handleDblClickReset = () => {
  initializeImageTransform();
};
</script>

<style scoped>
/* 样式可以保持不变 */
</style>