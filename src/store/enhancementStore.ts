// src/store/enhancementStore.ts

import { reactive } from 'vue';

// 创建一个响应式的 store 对象
export const enhancementStore = reactive({
    file: null,
    prompt: '',
    selectedSteps: [],
});

// 提供一个方法来设置数据
export function setEnhancementData(data) {
    enhancementStore.file = data.file;
    enhancementStore.prompt = data.prompt;
    enhancementStore.selectedSteps = data.selectedSteps;
}