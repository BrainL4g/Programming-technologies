import apiClient from './apiClient';

const TOKEN_KEY = 'jwt_token';
const USER_KEY = 'user';

export const authService = {
    getToken() {
        return localStorage.getItem(TOKEN_KEY);
    },

    setAuthData(token, user) {
        localStorage.setItem(TOKEN_KEY, token);
        localStorage.setItem(USER_KEY, JSON.stringify(user));
    },

    clearAuthData() {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
    },

    isAuthenticated() {
        return !!this.getToken();
    },

    getCurrentUser() {
        const userJson = localStorage.getItem(USER_KEY);
        if (userJson) {
            try {
                return JSON.parse(userJson);
            } catch (e) {
                return null;
            }
        }
        return null;
    },

    async login(email, password) {
      try {
          const tokenResponse = await apiClient.login(email, password);
          const token = tokenResponse.access_token;
          this.setAuthData(token, {});
          const user = await apiClient.get('/users/me');
          this.setAuthData(token, user);
          return user;
        } catch (error) {
            console.error("Login failed:", error.message);
            this.clearAuthData();
            throw new Error(error.message || 'Invalid credentials');
        }
    },

    async register(email, password, confirm_password, username) {
        try {
            const registerData = { email, password, confirm_password, username };
            await apiClient.post('/register', registerData);
            const user = await this.login(email, password);

            return user;
        } catch (error) {
            console.error("Registration failed:", error.message);
            throw new Error(error.message || 'Registration failed');
        }
    },

    logout() {
        this.clearAuthData();
    }
};