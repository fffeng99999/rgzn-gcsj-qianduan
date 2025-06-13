src/components/StatusDisplayPreviewResult.vue

<template>
  <div class="result-preview-wrapper">
    <div class="result-preview-container">
      <StatusDisplay
          class="status-display-content"
          :progress="progress"
          :loss-data="lossData"
      />
    </div>
  </div>
</template>

<script setup>
// 导入您想要展示的 StatusDisplay 组件
import StatusDisplay from './StatusDisplay.vue';

// 定义 props，用于接收进度和 Loss 数据，并传递给子组件
defineProps({
  progress: {
    type: Number,
    required: true,
  },
  lossData: {
    type: Array,
    required: true,
  }
});
</script>

<style scoped>
/* --- 图框样式 --- */
/* 这些样式完全复制自 ImagePreview.vue 以确保外观一致 */
.result-preview-wrapper {
  flex-grow: 1;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 16px 0;
  animation: slide-up-fade-in 0.5s ease-out;
}

.result-preview-container {
  /* 尺寸和风格与 ImagePreview.vue 保持一致 */
  width: 90%;
  max-width: 900px;
  height: 80vh;
  max-height: 600px;
  border: 1px solid var(--n-border-color);
  border-radius: 16px;
  padding: 16px; /* 容器内边距 */
  background-color: var(--card-color-imgpv-bg);
  box-shadow: var(--component-shadow);
  transition: all 0.3s ease;

  /* 使用 flex 布局确保内部的 StatusDisplay 组件可以填满整个容器。
    这与 ImagePreview.vue 中居中图片的方式略有不同，但更适合内容展示。
  */
  display: flex;
  overflow: hidden;
}

/* --- 内容样式 --- */
/*
  因为 StatusDisplay 本身是一个 Naive UI 的 Card 组件，
  它有自己的背景和内边距。为了让它完美融入我们自定义的“图框”：
  1. 让它充满图框的可用空间 (width: 100%)。
  2. 将它的背景设为透明，避免出现卡片里套卡片的视觉效果。
  3. 通过 :deep() 选择器移除其自身的内边距，因为我们的容器已经有内边距了。
*/
.status-display-content {
  width: 100%;
  background: transparent;
  /* StatusDisplay.vue 根元素是 <n-card>，
    使用 :deep() 穿透组件的 scoped 样式，修改其内部 padding。
  */
}
.status-display-content:deep(.n-card__content) {
  padding: 0;
}
.status-display-content:deep(.n-card__header) {
  padding-bottom: 16px;
}


/* 动画效果与 ImagePreview.vue 保持一致 */
@keyframes slide-up-fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
