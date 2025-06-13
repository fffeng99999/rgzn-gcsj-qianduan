// src/components/ResultsDisplay.vue

<template>
  <n-card title="3. 结果展示与输出" :bordered="false">
    <n-tabs type="line" animated>
      <n-tab-pane name="compare" tab="单步结果对比">
        <n-p depth="3">并排展示原始图像与各阶段处理结果，可缩放查看细节。</n-p>
        <n-space justify="space-around">
          <div class="image-container" v-for="image in filteredComparisonImages" :key="image.label">
            <n-h6>{{ image.label }}</n-h6>
            <n-image width="200" :src="image.src" />
          </div>
        </n-space>
      </n-tab-pane>
      <n-tab-pane name="gif" tab="GIF 动画">
        <n-p depth="3">自动生成的处理全过程 GIF 动画。</n-p>
        <n-space justify="center">
          <n-image :src="gifUrl" />
        </n-space>
      </n-tab-pane>
      <n-tab-pane name="metrics" tab="质量指标">
        <n-p depth="3">图像增强质量的量化评估指标。</n-p>
        <n-descriptions label-placement="left" bordered :column="1">
          <n-descriptions-item label="PSNR (峰值信噪比)">
            {{ metrics.psnr }} dB
          </n-descriptions-item>
          <n-descriptions-item label="SSIM (结构相似性指数)">
            {{ metrics.ssim }}
          </n-descriptions-item>
          <n-descriptions-item label="CLIP-SCORE (语义相似度得分)">
            {{ metrics.clipScore }}
          </n-descriptions-item>
        </n-descriptions>
      </n-tab-pane>
    </n-tabs>
    <n-divider />
    <n-h6>下载选项</n-h6>
    <n-space>
      <n-button v-if="selectedSteps.includes('step1')">下载 Step1 结果</n-button>
      <n-button v-if="selectedSteps.includes('step2')">下载 Step2 结果</n-button>
      <n-button v-if="selectedSteps.includes('step3')">下载 Step3 结果</n-button>
      <n-button>下载 GIF 动画</n-button>
      <n-button>下载指标报告</n-button>
    </n-space>
  </n-card>
</template>

<script setup>
import { computed } from 'vue'; // ✨ 1. 引入 computed
import { NCard, NP, NH6, NTabs, NTabPane, NSpace, NImage, NDivider, NButton, NDescriptions, NDescriptionsItem } from 'naive-ui';

// ✨ 1. 修改 props，增加 selectedSteps 用于接收父组件传递的选择状态
const props = defineProps({
  comparisonImages: Array,
  gifUrl: String,
  metrics: Object,
  selectedSteps: {
    type: Array,
    default: () => []
  }
});

// ✨ 1. 创建计算属性，用于过滤要显示的对比图像
const filteredComparisonImages = computed(() => {
  if (!props.comparisonImages) return [];

  return props.comparisonImages.filter(image => {
    // 始终显示原始图像
    if (image.label.includes('原始')) {
      return true;
    }
    // 根据 selectedSteps 动态显示对应的步骤结果
    if (image.label.includes('Step 1') && props.selectedSteps.includes('step1')) {
      return true;
    }
    if (image.label.includes('Step 2') && props.selectedSteps.includes('step2')) {
      return true;
    }
    if (image.label.includes('Step 3') && props.selectedSteps.includes('step3')) {
      return true;
    }
    return false;
  });
});

</script>

<style scoped>
.image-container {
  text-align: center;
}
</style>