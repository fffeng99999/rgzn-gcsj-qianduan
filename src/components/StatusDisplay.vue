// src/components/StatusDisplay.vue

<template>
  <n-card title="实时监控" :bordered="false">
    <n-p depth="3">实时处理进度与模型 Loss 曲线。</n-p>
    <n-h6>处理进度</n-h6>
    <n-progress
        type="line"
        :percentage="progress"
        :indicator-placement="'inside'"
        processing
    />
    <n-h6 style="margin-top: 16px;">Loss 曲线预览</n-h6>
    <v-chart class="chart" :option="chartOption" autoresize />
  </n-card>
</template>

<script setup>
import { ref, computed } from 'vue';
import { NCard, NP, NH6, NProgress } from 'naive-ui';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { LineChart } from 'echarts/charts';
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent } from 'echarts/components';
import VChart from 'vue-echarts';

use([ CanvasRenderer, LineChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent ]);

const props = defineProps({
  progress: Number,
  lossData: Array // Expects an array of numbers
});

const chartOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  xAxis: { type: 'category' },
  yAxis: { type: 'value', name: 'Loss', min: 0 },
  series: [{
    data: props.lossData,
    type: 'line',
    smooth: true,
    showSymbol: false,
    lineStyle: { color: 'var(--n-primary-color)' }
  }]
}));
</script>

<style scoped>
.chart {
  height: 200px;
}
</style>