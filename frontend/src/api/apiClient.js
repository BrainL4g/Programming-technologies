const TOKEN_KEY = 'jwt_token';

const API_BASE_URL = 'http://127.0.0.1:8000';

const handleResponse = async (response) => {
    if (response.ok) {
        const contentType = response.headers.get("content-type");
        if (response.status === 204 || !contentType || !contentType.includes("application/json")) {
            return {};
        }
        return response.json();
    }

    let error;
    try {
        error = await response.json();
    } catch {
        throw new Error(`Server responded with status ${response.status}`);
    }

    throw new Error(error.detail || error.message || 'An unknown error occurred');
};

const getAuthHeaders = (isFormUrlEncoded = false) => {
    const token = localStorage.getItem(TOKEN_KEY);
    const headers = {};

    if (isFormUrlEncoded) {
        headers['Content-Type'] = 'application/x-www-form-urlencoded';
    } else {
        headers['Content-Type'] = 'application/json';
    }

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
};


const apiClient = {
    async login(email, password) {
        const url = new URLSearchParams();
        url.append('username', email);
        url.append('password', password);

        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: getAuthHeaders(true),
            body: url.toString(),
        });

        return handleResponse(response);
    },

    async get(endpoint) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'GET',
            headers: getAuthHeaders(),
        });
        return handleResponse(response);
    },

    async post(endpoint, data) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(data),
        });
        return handleResponse(response);
    },

    async patch(endpoint, data) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'PATCH',
            headers: getAuthHeaders(),
            body: JSON.stringify(data),
        });
        return handleResponse(response);
    },

    async delete(endpoint) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'DELETE',
            headers: getAuthHeaders(),
        });
        return handleResponse(response);
    },
};

export default apiClient;