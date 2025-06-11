import axios from 'axios';

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

const api = axios.create({
    baseURL: apiBaseUrl,
    headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
    withCredentials: true,  // This ensures cookies are sent with requests
    timeout: 10000,  // 10 second timeout
});

// Add request interceptor for debugging
api.interceptors.request.use(
    (config) => {
        // Ensure HTTPS is used and remove trailing slashes
        if (config.url) {
            if (config.url.startsWith('http://')) {
                config.url = config.url.replace('http://', 'https://');
            }
            // Remove trailing slash if present
            if (config.url.endsWith('/')) {
                config.url = config.url.slice(0, -1);
            }
        }
        console.log('Making request to:', config.url);
        return config;
    },
    (error) => {
        console.error('Request error:', error);
        return Promise.reject(error);
    }
);

// Add response interceptor for better error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.code === 'ERR_NETWORK') {
            console.error('Network error:', error);
            throw new Error('Unable to connect to the server. Please check if the backend is running on port 8080.');
        }
        if (error.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            console.error('Response error:', error.response.data);
            const errorMessage = error.response.data?.detail || 'An error occurred';
            throw new Error(errorMessage);
        } else if (error.request) {
            // The request was made but no response was received
            console.error('Request error:', error.request);
            throw new Error('No response from server. Please try again later.');
        } else {
            // Something happened in setting up the request that triggered an Error
            console.error('Error:', error.message);
            throw error;
        }
    }
);

export const postRequest = async <T>(url: string, data: T, config?: any) => {
    try {
        const response = await api.post(url, data, config);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getRequest = async (url: string) => {
    try {
        const response = await api.get(url);
        console.log(url);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getRequestWithParams = async (url: string, params: any) => {
    try {
        const response = await api.get(url, { params });
        return response.data;
    } catch (error) {
        throw error;
    }
}

export const deleteRequest = async (url: string) => {
    try {
        const response = await api.delete(url);
        return response.data;
    } catch (error) {
        throw error;
    }
};
export const putRequest = async <T>(url: string, data: T) => {
    try {
        const response = await api.put(url, data);
        return response.data;
    } catch (error) {
        throw error;
    }
}