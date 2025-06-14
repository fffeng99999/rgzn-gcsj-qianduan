// src/composables/useImageUploader.js

import { ref, onUnmounted } from 'vue';
import { useMessage } from 'naive-ui';

/**
 * 一个用于处理图片上传、文件选择和拖拽的 Vue Composable。
 * 管理上传文件的引用、URL 和上传状态，并处理 URL 的生命周期。
 */
export function useImageUploader() {
    const message = useMessage(); // 使用 Naive UI 的消息提示
    const fileInputRef = ref(null); // 用于引用隐藏的文件输入框
    const uploadedFile = ref(null); // 存储上传的原始文件对象
    const isImageUploaded = ref(false); // 标记是否有图片已上传
    const imageUrl = ref(null); // 存储图片的 Blob URL，用于预览

    /**
     * 触发隐藏的文件输入框点击事件，打开文件选择对话框。
     */
    const handleUploadClick = () => {
        fileInputRef.value?.click();
    };

    /**
     * 处理文件输入框的 change 事件，获取用户选择的文件。
     * @param {Event} e Change 事件对象
     */
    const handleFileChange = (e) => {
        processAndSetFile(e.target.files);
        // 清空文件输入框的值，以便用户再次选择同一个文件也能触发 change 事件
        if (e.target) e.target.value = '';
    };

    /**
     * 核心文件处理逻辑，用于处理来自文件输入框或拖拽的文件。
     * 验证文件类型，创建预览URL，并更新相关状态。
     * @param {FileList | File[]} files 文件列表
     */
    const processAndSetFile = (files) => {
        if (!files || files.length === 0) return;
        const file = files[0];

        if (file && file.type.startsWith('image/')) {
            message.success(`图片 ${file.name} 已接收！`);
            // 如果之前有图片URL，先撤销旧的URL以释放内存
            if (imageUrl.value) URL.revokeObjectURL(imageUrl.value);

            // 更新上传相关的状态
            uploadedFile.value = file;
            imageUrl.value = URL.createObjectURL(file);
            isImageUploaded.value = true;
        } else {
            // 如果文件类型不正确，显示错误信息并重置上传状态
            message.error('请只上传图片文件！');
            uploadedFile.value = null;
            if (imageUrl.value) {
                URL.revokeObjectURL(imageUrl.value);
                imageUrl.value = null;
            }
            isImageUploaded.value = false;
        }
    };

    /**
     * 清理函数：在组件卸载时撤销 Blob URL，防止内存泄漏。
     * 必须在调用此 Composable 的组件的 onUnmounted 钩子中调用。
     */
    const cleanup = () => {
        if (imageUrl.value) {
            URL.revokeObjectURL(imageUrl.value);
            imageUrl.value = null;
        }
    };

    // 注册 onUnmounted 钩子以自动执行清理 (如果Composable只在组件生命周期内使用)
    // 或者选择在组件中手动调用 cleanup() 以便更灵活地控制
    onUnmounted(() => {
        cleanup();
    });

    return {
        fileInputRef,
        uploadedFile,
        isImageUploaded,
        imageUrl,
        handleUploadClick,
        handleFileChange,
        processAndSetFile, // 暴露给 useDragAndDrop 或其他需要直接处理文件列表的地方
        cleanup, // 也暴露出去，以便外部手动调用，例如在特定事件时重置状态
    };
}