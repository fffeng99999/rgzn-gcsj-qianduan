// src/components/ImagePreview.vue

<template>
  <div class="image-preview-wrapper">
    <div
        ref="containerEl" class="image-preview-container"
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
          @dblclick="resetTransform"
          @load="initializeImageTransform" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// ✨ 1. 新增 props 来接收外部的变换状态
const props = defineProps({
  imageUrl: {
    type: String,
    required: true,
  },
  transformState: {
    type: Object,
    required: true,
    // 提供一个默认值，以防父组件未传递
    default: () => ({ scale: 1, translateX: 0, translateY: 0 })
  },
});

// ✨ 2. 新增 emits 来向父组件报告状态更新
const emit = defineEmits(['update:transform', 'initialized']);

// --- 内部状态（仅用于交互过程，不影响显示） ---
const imageEl = ref(null);
const containerEl = ref(null);
const isPanning = ref(false);
const startDrag = ref({ x: 0, y: 0 });

// ✨ 3. 图像样式现在完全由传入的 props 决定
const imageStyle = computed(() => ({
  transform: `scale(${props.transformState.scale}) translate(${props.transformState.translateX}px, ${props.transformState.translateY}px)`,
}));

// ✨ 4. 初始化函数现在 emit 事件，而不是设置本地状态
const initializeImageTransform = () => {
  if (!imageEl.value || !containerEl.value || !imageEl.value.naturalWidth) return;

  const { naturalWidth: imgWidth, naturalHeight: imgHeight } = imageEl.value;
  const { clientWidth: containerWidth, clientHeight: containerHeight } = containerEl.value;

  const scaleX = containerWidth / imgWidth;
  const scaleY = containerHeight / imgHeight;
  const newScale = Math.min(scaleX, scaleY);

  // 触发 'initialized' 事件，将计算出的理想初始状态传递给父组件
  emit('initialized', { scale: newScale, translateX: 0, translateY: 0 });
};

// ✨ 5. 所有事件处理器现在都 emit 更新，而不是修改本地 state
const handleWheel = (event) => {
  const scaleAmount = 0.1;
  const currentScale = props.transformState.scale;
  // 此处的缩放限制可以更简单，因为父组件可以决定初始缩放值
  const minScale = 0.2;
  const maxScale = 5;

  let newScale;
  if (event.deltaY > 0) {
    newScale = Math.max(minScale, currentScale - scaleAmount);
  } else {
    newScale = Math.min(maxScale, currentScale + scaleAmount);
  }
  // 发送更新请求
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
    // 发送更新请求
    emit('update:transform', { ...props.transformState, translateX: newTranslateX, translateY: newTranslateY });
  }
};

const handleMouseUp = () => { isPanning.value = false; };
const handleMouseLeave = () => { isPanning.value = false; };

const resetTransform = () => {
  // 发送重置请求，父组件可以决定重置到哪个状态
  emit('update:transform', { scale: 1, translateX: 0, translateY: 0 });
};
</script>

<style scoped>
/* 样式与原来保持完全一致 */
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
</style>