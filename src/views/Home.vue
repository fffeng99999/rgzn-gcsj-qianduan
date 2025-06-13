// src/views/Home.vue

<template>
  <n-space vertical :size="24">
    <n-card>
      <n-h1 style="font-weight: 500;">
        <n-text type="primary">
          欢迎访问 人工智能 工程实践 演示
        </n-text>
      </n-h1>
      <n-p>
        【待修改】 这是一个基于 Vue 3 和 Naive UI 构建的现代化单页应用。你可以在这里体验到流畅的交互和丰富的功能。
      </n-p>
      <n-p>
        请通过顶部的导航栏探索 "演示" "增强" 和 "关于" 页面。
      </n-p>
    </n-card>

    <n-alert title="项目状态" type="success">
      所有系统均运行正常。今天是 {{ currentDate }}。
    </n-alert>
  </n-space>
</template>

<script setup>
import { NCard, NH1, NP, NText, NSpace, NAlert } from 'naive-ui';
import { computed } from 'vue';

const currentDate = computed(() => {
  return new Date().toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  });
});
</script>

<style scoped>
.n-h1 {
  margin-top: 0;
}
</style>