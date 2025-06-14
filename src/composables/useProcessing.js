import { ref } from 'vue';
import { useMessage } from 'naive-ui';

export function useProcessing() {
    const message = useMessage();
    const displayState = ref('single'); // 'single', 'processing', 'result'
    const processingProgress = ref(0);
    const lossData = ref([]);
    let processingInterval = null;

    const startProcessing = (onSuccess) => {
        displayState.value = 'processing';
        processingProgress.value = 0;
        lossData.value = [];

        if (processingInterval) clearInterval(processingInterval);

        // 模拟后端处理
        processingInterval = setInterval(() => {
            if (processingProgress.value < 100) {
                processingProgress.value += 20;
                const newLoss = Math.random() * (0.8 - lossData.value.length * 0.1) + 0.1;
                lossData.value.push(parseFloat(newLoss.toFixed(2)));
            } else {
                clearInterval(processingInterval);
            }
        }, 900);

        message.loading('请求已提交，正在处理中...', { duration: 5000 });

        // 模拟处理完成
        setTimeout(() => {
            clearInterval(processingInterval);
            processingProgress.value = 100;
            displayState.value = 'result';
            if (onSuccess) onSuccess();
        }, 5000);
    };

    const resetProcessingState = () => {
        displayState.value = 'single';
        if (processingInterval) clearInterval(processingInterval);
        processingProgress.value = 0;
        lossData.value = [];
    };

    const cleanup = () => {
        if (processingInterval) clearInterval(processingInterval);
    };

    return {
        displayState,
        processingProgress,
        lossData,
        startProcessing,
        resetProcessingState,
        cleanup,
    };
}