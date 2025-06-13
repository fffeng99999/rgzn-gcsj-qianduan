// src/services/api/index.ts

// 导入所有具体的 API 模块
import * as imageProcessingApi from './imageProcessingApi';
// import * as authApi from './authApi'; // 如果未来有认证相关的API，可以在这里导入

// 导出所有导入的 API 模块
export {
    imageProcessingApi,
    // authApi, // 未来如果有了可以放开注释
};

// 或者，如果你希望直接导出每个函数而不是模块，可以这样：
// export { uploadImage, processImage, getImageResult } from './imageProcessingApi';
// 这种方式更扁平化，但如果API很多，可能会导致 index.ts 文件过长