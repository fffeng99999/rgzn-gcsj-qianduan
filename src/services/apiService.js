// src/services/apiService.js

import axios from 'axios';

<<<<<<< HEAD
const API_BASE_URL = import.meta.env.VITE_APP_API_BASE_URL || 'http://127.0.0.1:5000';

=======
// Using import.meta.env.VITE_APP_API_BASE_URL for better environment handling,
// but falling back to localhost for development if not defined.
const API_BASE_URL = import.meta.env.VITE_APP_API_BASE_URL || 'http://127.0.0.1:5000'; // Corrected default to 127.0.0.1 if that's your Flask default

// Create an Axios instance with your backend's URL.
>>>>>>> 7a887e08bad3f67f5ba7643fee66ec61202038b4
const apiClient = axios.create({
    baseURL: API_BASE_URL,
});

/**
<<<<<<< HEAD
 * Fetches pre-configured parameters for a specific model from the backend.
 * @param {string} modelName The base name of the model (e.g., 'unet_best').
 * @returns {Promise<Object>} The model parameters object.
=======
 * Sends the image and all associated metadata to the backend.
 * This metadata object will now include the model-specific parameters.
 * @param {File} file The image file.
 * @param {Object} metadata The JSON object with all settings, including parameters.
 * @returns {Promise<Object>} The response from the server.
>>>>>>> 7a887e08bad3f67f5ba7643fee66ec61202038b4
 */
export const fetchModelParameters = async (modelName) => {
    try {
        console.log(`Fetching parameters for model: ${modelName}`);
        const response = await apiClient.get(`/model-parameters/${modelName}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching parameters for model ${modelName}:`, error.response || error.message);
        throw error.response?.data || { error: 'Failed to fetch model parameters.' };
    }
};

/**
 * Lists all available model names from the backend.
 * @returns {Promise<string[]>} An array of model names (e.g., ['unet_best', 'model_v2']).
 */
export const listAvailableModels = async () => {
    try {
        console.log('Listing available models...');
        const response = await apiClient.get('/models');
        return response.data.models; // Backend returns { "models": ["name1", "name2"] }
    } catch (error) {
        console.error('Error listing available models:', error.response || error.message);
        throw error.response?.data || { error: 'Failed to list models.' };
    }
};

// The existing processImageWithMetadata function remains the same
export const processImageWithMetadata = async (file, metadata) => {
    // ... implementation remains the same
    const formData = new FormData();
    formData.append('file', file);
<<<<<<< HEAD
    formData.append('metadata', JSON.stringify(metadata));
    console.log("Sending data to backend with metadata:", metadata);
=======

    // The backend will expect the JSON data under the key 'metadata'.
    // Ensure the `metadata` object already contains the `parameters` field
    // (which includes steps, advancedParams, model, prompt, etc.).
    formData.append('metadata', JSON.stringify(metadata));

    console.log("Sending data to backend with metadata:", metadata); // Log the full metadata being sent

>>>>>>> 7a887e08bad3f67f5ba7643fee66ec61202038b4
    try {
        const response = await apiClient.post('/process-image', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
        return response.data;
    } catch (error) {
        console.error('API Service Error:', error.response || error.message);
        throw error.response?.data || { error: 'A network or server error occurred.' };
    }
};

<<<<<<< HEAD
=======
/**
 * Fetches pre-configured parameters for a specific model from the backend.
 * @param {string} modelName The base name of the model (e.g., 'unet_best').
 * @returns {Promise<Object>} The model parameters object.
 */
export const fetchModelParameters = async (modelName) => {
    try {
        console.log(`Fetching parameters for model: ${modelName}`);
        const response = await apiClient.get(`/model-parameters/${modelName}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching parameters for model ${modelName}:`, error.response || error.message);
        throw error.response?.data || { error: 'Failed to fetch model parameters.' };
    }
};

/**
 * Lists all available model names from the backend.
 * @returns {Promise<string[]>} An array of model names (e.g., ['unet_best', 'model_v2']).
 */
export const listAvailableModels = async () => {
    try {
        console.log('Listing available models...');
        const response = await apiClient.get('/models');
        return response.data.models; // Assuming the backend returns { "models": ["name1", "name2"] }
    } catch (error) {
        console.error('Error listing available models:', error.response || error.message);
        throw error.response?.data || { error: 'Failed to list models.' };
    }
};

>>>>>>> 7a887e08bad3f67f5ba7643fee66ec61202038b4

// import axios from 'axios';
//
// // Create an Axios instance with your backend's URL.
// const apiClient = axios.create({
//     baseURL: 'http://localhost:5000', // This URL comes from your app.py configuration.
// });
//
// /**
//  * Sends the image and all associated metadata to the backend.
//  * @param {File} file The image file.
//  * @param {Object} metadata The JSON object with all settings.
//  * @returns {Promise<Object>} The response from the server.
//  */
// export const processImageWithMetadata = async (file, metadata) => {
//     const formData = new FormData();
//
//     // The backend expects the file under the key 'file'.
//     formData.append('file', file);
//
//     // The backend will expect the JSON data under the key 'metadata'.
//     formData.append('metadata', JSON.stringify(metadata));
//
//     console.log("Sending data to backend...");
//
//     try {
//         const response = await apiClient.post('/process-image', formData, {
//             headers: {
//                 'Content-Type': 'multipart/form-data',
//             },
//         });
//         return response.data;
//     } catch (error) {
//         console.error('API Service Error:', error.response || error.message);
//         // Throw a more structured error for the component to catch.
//         throw error.response?.data || { error: 'A network or server error occurred.' };
//     }
// };