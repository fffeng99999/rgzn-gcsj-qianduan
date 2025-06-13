// src/App.vue

<template>
  <n-config-provider :theme="theme" :locale="zhCN" :date-locale="dateZhCN">
    <n-message-provider>
      <n-notification-provider>
        <n-dialog-provider>
          <n-loading-bar-provider>
            <Layout />
          </n-loading-bar-provider>
        </n-dialog-provider>
      </n-notification-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup>
import { ref, provide, computed } from 'vue' // 引入 computed
import {
  darkTheme,
  lightTheme,
  zhCN,
  dateZhCN,
  NConfigProvider,
  NMessageProvider,
  NNotificationProvider,
  NDialogProvider,
  NLoadingBarProvider
} from 'naive-ui'
import Layout from './layout/Layout.vue'
import { watchEffect } from 'vue'

// 自动判断系统主题色
const theme = ref(lightTheme)
const darkQuery = window.matchMedia('(prefers-color-scheme: dark)')
theme.value = darkQuery.matches ? darkTheme : lightTheme
darkQuery.addEventListener('change', (e) => {
  theme.value = e.matches ? darkTheme : lightTheme
})

// 切换主题的方法
const toggleTheme = () => {
  theme.value = theme.value.name === 'light' ? darkTheme : lightTheme
}

// 计算当前主题是否为“深色”主题，返回一个响应式布尔值
const isDark = computed(() => theme.value.name === 'dark')
// 提供切换主题的函数给所有子组件使用
provide('toggleTheme', toggleTheme)
// 提供当前主题状态（深色或浅色）给子组件，子组件可响应主题变化
provide('isDark', isDark)


watchEffect(() => {
  document.body.classList.remove('light-theme', 'dark-theme')
  document.body.classList.add(isDark.value ? 'dark-theme' : 'light-theme')
})

</script>