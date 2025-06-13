// src/components/FileDropOverlay.vue

<template>
  <div class="drop-overlay-container">
    <div class="drop-zone">
      <n-icon size="80" :component="CloudUploadOutline" />
      <n-h2 style="margin-top: 20px; color: #fff;">上传图片</n-h2>
      <n-p depth="3" style="color: #eee;">将图片文件拖放网页内，即可添加到对话中</n-p>
    </div>
  </div>
</template>

<script setup>
import { NIcon, NH2, NP } from 'naive-ui';
import { CloudUploadOutline } from '@vicons/ionicons5';
</script>

<style scoped>
.drop-overlay-container {
  position: fixed; /* 固定定位，覆盖整个屏幕 */
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.65); /* 半透明黑色背景 */
  z-index: 9999; /* 确保在最顶层 */

  /* 使用 Flexbox 将内容居中 */
  display: flex;
  justify-content: center;
  align-items: center;

  /* 添加一个微妙的渐入动画 */
  animation: fadeIn 0.3s ease;
}

.drop-zone {
  text-align: center;
  padding: 60px;
  border: 2px dashed var(--n-border-color);
  border-radius: 20px;
  max-width: 500px;
  width: 90%;
  background-color: rgba(255, 255, 255, 0.05); /* 轻微的背景色，增加质感 */
  color: #fff; /* 文字颜色 */
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>