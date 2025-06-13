// src/layout/Layout.vue

<template>
  <n-layout position="absolute">
    <TopNavigationBar />

    <n-layout-content
        :native-scrollbar="false"
        :content-style="contentStyle"
    >
      <router-view :key="route.fullPath" />
    </n-layout-content>

    <n-layout-footer bordered position="absolute" style="height: 48px; display: flex; align-items: center; justify-content: center;">
      © {{ currentYear }} 人工智能 工程实践 演示
    </n-layout-footer>
  </n-layout>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { NLayout, NLayoutContent, NLayoutFooter } from 'naive-ui';
import TopNavigationBar from '../components/TopNavigationBar.vue';

const route = useRoute();
const currentYear = new Date().getFullYear();

// 将样式定义为一个变量，传递给 content-style
const contentStyle = "padding: 64px 24px 32px 24px; display: flex; flex-direction: column;"

</script>

<style scoped>

</style>