// src/store/enhancementStore.ts

import { defineStore } from 'pinia';
import { imageProcessingApi } from '../services/api'; // 从新的入口文件导入API模块

export const useEnhancementStore = defineStore('enhancement', {
    state: () => ({
        uploadedImage: null as File | null,
        uploadedImageUrl: null as string | null,
        uploadedImageId: null as string | null,
        processingTaskId: null as string | null, // 添加回处理任务ID
        processedResultUrl: null as string | null, // 添加回处理结果URL
        isUploading: false,
        isProcessing: false, // 添加处理中状态
        isLoadingResult: false, // 添加获取结果中状态
        uploadError: null as string | null,
        processError: null as string | null, // 添加处理错误
        resultError: null as string | null, // 添加结果错误
        processingStatus: 'idle' as 'idle' | 'uploading' | 'processing' | 'completed' | 'failed', // 任务状态
    }),

    actions: {
        async uploadImageAction(file: File) {
            this.isUploading = true;
            this.uploadError = null;
            this.uploadedImage = file;
            this.uploadedImageUrl = URL.createObjectURL(file);
            this.processingStatus = 'uploading';

            try {
                const data = await imageProcessingApi.uploadImage(file); // 通过模块调用
                this.uploadedImageId = data.id;
                this.processingStatus = 'completed'; // 上传成功
                console.log('Image uploaded successfully, ID:', this.uploadedImageId);
                return true;
            } catch (error: any) {
                this.uploadedImageId = null;
                this.uploadError = error.message || '图片上传失败。';
                this.processingStatus = 'failed';
                console.error('Upload image action failed:', error);
                return false;
            } finally {
                this.isUploading = false;
            }
        },

        async processImageAction(parameters: any) {
            if (!this.uploadedImageId) {
                this.processError = '请先上传图片。';
                return false;
            }

            this.isProcessing = true;
            this.processError = null;
            this.processingTaskId = null;
            this.processedResultUrl = null;
            this.processingStatus = 'processing';

            try {
                const data = await imageProcessingApi.processImage(this.uploadedImageId, parameters); // 通过模块调用
                this.processingTaskId = data.id;
                console.log('Image processing started, Task ID:', this.processingTaskId);
                return true;
            } catch (error: any) {
                this.processingTaskId = null;
                this.processError = error.message || '图片处理请求失败。';
                this.processingStatus = 'failed';
                console.error('Process image action failed:', error);
                return false;
            } finally {
                this.isProcessing = false;
            }
        },

        async fetchImageResultAction() {
            if (!this.processingTaskId) {
                this.resultError = '没有进行中的处理任务。';
                return false;
            }

            this.isLoadingResult = true;
            this.resultError = null;

            try {
                const data = await imageProcessingApi.getImageResult(this.processingTaskId); // 通过模块调用
                if (data.status === 'completed') {
                    this.processedResultUrl = data.resultUrl;
                    this.processingStatus = 'completed';
                    console.log('Image processing completed, Result URL:', this.processedResultUrl);
                    return true;
                } else {
                    console.log('Image processing still in progress, status:', data.status);
                    this.processingStatus = 'processing';
                    return false;
                }
            } catch (error: any) {
                this.processedResultUrl = null;
                this.resultError = error.message || '获取处理结果失败。';
                this.processingStatus = 'failed';
                console.error('Fetch image result action failed:', error);
                return false;
            } finally {
                this.isLoadingResult = false;
            }
        },

        resetEnhancementState() {
            this.$reset();
        }
    },

    getters: {
        hasAnyError: (state) => !!state.uploadError || !!state.processError || !!state.resultError,
        canProcess: (state) => !!state.uploadedImageId && !state.isProcessing,
    },
});