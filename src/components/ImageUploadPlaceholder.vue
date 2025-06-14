// src/components/ImageUploadPlaceholder.vue

<template>
  <div class="placeholder-box">
    <div class="placeholder-content">
      <n-icon :component="ImageOutline" size="60" />
      <n-text depth="3" style="font-size: 32px;">请上传图片</n-text>
    </div>
  </div>
</template>

<script setup>
import { NIcon, NText } from 'naive-ui';
import { ImageOutline } from '@vicons/ionicons5';
</script>

<style scoped>
.placeholder-box {
  padding-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50%;
  height: 100%;
  border-radius: 12px;
  background-color: rgba(255, 255, 255, 0); /* 示例背景色 */
}

.placeholder-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #ccc;
}
</style>