// src/composables/useDragAndDrop.js

import { ref, onMounted, onUnmounted } from 'vue';

export function useDragAndDrop(onDropCallback) {
    // 响应式变量，用于控制遮罩层的显示和隐藏
    const isDragging = ref(false);
    let dragCounter = 0;

    const handleDragEnter = (e) => {
        e.preventDefault();
        if (e.dataTransfer.types.includes('Files')) {
            dragCounter++;
            isDragging.value = true;
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        dragCounter--;
        if (dragCounter === 0) {
            isDragging.value = false;
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        isDragging.value = false;
        dragCounter = 0;
        // 调用传入的回调函数来处理文件
        if (onDropCallback) {
            onDropCallback(e.dataTransfer.files);
        }
    };

    onMounted(() => {
        window.addEventListener('dragenter', handleDragEnter);
        window.addEventListener('dragover', handleDragOver);
        window.addEventListener('dragleave', handleDragLeave);
        window.addEventListener('drop', handleDrop);
    });

    onUnmounted(() => {
        window.removeEventListener('dragenter', handleDragEnter);
        window.removeEventListener('dragover', handleDragOver);
        window.removeEventListener('dragleave', handleDragLeave);
        window.removeEventListener('drop', handleDrop);
    });

    // 将 isDragging 状态返回给使用它的组件
    return {
        isDragging,
    };
}