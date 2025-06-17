// src/services/reportService.js

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_APP_API_BASE_URL || 'http://127.0.0.1:5000';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
});

/**
 * Fetches the detailed report data from the backend.
 * @param {Object} reportInfo - Object containing report_id, filenames, and parameters.
 * @returns {Promise<Object>} The detailed report data.
 */
export const fetchReportData = async (reportInfo) => {
    try {
        console.log("Fetching report data with info:", reportInfo);
        const response = await apiClient.post('/get-report', reportInfo);
        return response.data;
    } catch (error) {
        console.error('Report Service Error:', error.response || error.message);
        throw error.response?.data || { error: 'Failed to fetch report data.' };
    }
};