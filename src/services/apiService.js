import axios from 'axios';

// Create an Axios instance with your backend's URL.
const apiClient = axios.create({
    baseURL: 'http://localhost:5000', // This URL comes from your app.py configuration.
});

/**
 * Sends the image and all associated metadata to the backend.
 * @param {File} file The image file.
 * @param {Object} metadata The JSON object with all settings.
 * @returns {Promise<Object>} The response from the server.
 */
export const processImageWithMetadata = async (file, metadata) => {
    const formData = new FormData();

    // The backend expects the file under the key 'file'.
    formData.append('file', file);

    // The backend will expect the JSON data under the key 'metadata'.
    formData.append('metadata', JSON.stringify(metadata));

    console.log("Sending data to backend...");

    try {
        const response = await apiClient.post('/process-image', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        console.error('API Service Error:', error.response || error.message);
        // Throw a more structured error for the component to catch.
        throw error.response?.data || { error: 'A network or server error occurred.' };
    }
};