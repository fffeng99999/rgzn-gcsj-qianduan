<template>
  <n-space vertical size="large">
    <n-space>
      <n-button>Default</n-button>
      <n-button type="tertiary">Tertiary</n-button>
      <n-button type="primary">Primary</n-button>
      <n-button type="info">Info</n-button>
      <n-button type="success">Success</n-button>
      <n-button type="warning">Warning</n-button>
      <n-button type="error">Error</n-button>
    </n-space>

    <n-card title="关于我们">
      <n-p>
        我们是一个致力于提供高质量图片超分应用的团队，热衷于探索前沿技术。
      </n-p>

      <n-h3>技术栈</n-h3>

      <n-list>
        <n-list-item>
          <n-thing title="Vue 3">
            核心框架，采用了组合式 API (Composition API)。
          </n-thing>
        </n-list-item>

        <n-list-item>
          <n-thing title="Naive UI">
            一个功能强大、主题可调的 Vue 3 组件库。
          </n-thing>
        </n-list-item>

        <n-list-item>
          <n-thing title="Vite">
            下一代前端构建工具，提供极速的开发体验。
          </n-thing>
        </n-list-item>
      </n-list>
    </n-card>
  </n-space>
</template>

<script setup>
import {
  NButton,
  NSpace,
  NCard,
  NP,
  NH3,
  NList,
  NListItem,
  NThing
} from 'naive-ui';
</script>
