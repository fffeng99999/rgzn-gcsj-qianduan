// src/composables/useImageTransform.js

import { reactive } from 'vue';

// 创建一个响应式对象来存储变换状态
const transformState = reactive({
    scale: 1,
    translateX: 0,
    translateY: 0,
});

/**
 * 一个用于共享和同步图像预览变换状态的 Composable。
 */
export function useImageTransform() {

    const updateTransform = (newState) => {
        if (newState) {
            transformState.scale = newState.scale;
            transformState.translateX = newState.translateX;
            transformState.translateY = newState.translateY;
        }
    };

    const resetTransform = (initialState = { scale: 1, translateX: 0, translateY: 0 }) => {
        updateTransform(initialState);
    };

    const initializeFit = (options = { fit: 'js' }) => {
        if (!imageEl.value || !containerEl.value) return;

        // 如果模式是 'css'，说明 CSS 的 object-fit 已经完成了缩放
        // JS 只需要重置 transform 状态即可
        if (options.fit === 'css') {
            resetTransform({ scale: 1, translateX: 0, translateY: 0 });
            return;
        }

        // 默认行为或 options.fit === 'js'，执行原来的计算逻辑
        const imgWidth = imageEl.value.naturalWidth;
        const imgHeight = imageEl.value.naturalHeight;
        const containerWidth = containerEl.value.clientWidth;
        const containerHeight = containerEl.value.clientHeight;

        if (imgWidth > 0 && imgHeight > 0) {
            const scaleX = containerWidth / imgWidth;
            const scaleY = containerHeight / imgHeight;
            const newScale = Math.min(scaleX, scaleY);
            resetTransform({ scale: newScale, translateX: 0, translateY: 0 });
        }
    };

    return {
        transformState,
        updateTransform,
        resetTransform,
        initializeFit,
    };
}