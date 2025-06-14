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

    return {
        transformState,
        updateTransform,
        resetTransform,
    };
}