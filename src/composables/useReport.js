// src/composables/useReport.js

import { ref, computed } from 'vue';
import { useMessage } from 'naive-ui';

export function useReport(displayState, imageUrl, resultImageUrl) {
    const message = useMessage();
    const showReportModal = ref(false);

    // 将 Mock 数据也移入
    const mockComparisonImages = computed(() => {
        const images = [{ label: '原始图像', src: imageUrl.value }];

        // 关键修改：在这里提供所有可能被显示的结果项
        // 让下游的 ResultsDisplay.vue 组件自己去根据 selectedSteps 筛选
        // 这里我们假设所有步骤都暂时使用同一个结果图 resultImageUrl.value
        images.push({ label: 'Step 1 结果', src: resultImageUrl.value });
        images.push({ label: 'Step 2 结果', src: resultImageUrl.value });
        images.push({ label: 'Step 3 结果', src: resultImageUrl.value });

        return images;
    });

    const mockGifUrl = ref("https://em-content.zobj.net/source/telegram/386/zany-face_1f92a.webp");
    const mockMetrics = ref({
        psnr: 32.8,
        ssim: 0.95,
        clipScore: 0.88,
    });

    // 将打开逻辑也移入
    const openReport = () => {
        if (displayState.value !== 'result') {
            message.error('请先等待处理完成再查看报告！');
            return;
        }
        showReportModal.value = true;
    };

    return {
        showReportModal,
        openReport,
        // 将数据组合成一个对象传出
        reportData: computed(() => ({
            comparisonImages: mockComparisonImages.value,
            gifUrl: mockGifUrl.value,
            metrics: mockMetrics.value,
        })),
    };
}