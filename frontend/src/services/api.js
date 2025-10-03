import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE_URL = 'http://192.168.0.165:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = await AsyncStorage.getItem('refresh_token');
        if (refreshToken) {
        const response = await axios.post(`${API_BASE_URL}/users/token/refresh/`, {
          refresh: refreshToken,
        });
        
        const { access } = response.data;
        if (access) {
          await AsyncStorage.setItem('access_token', access);
        }
          
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        await AsyncStorage.removeItem('access_token');
        await AsyncStorage.removeItem('refresh_token');
      }
    }
    
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (email, password) => 
    api.post('/users/token/', { email, password }),
  
  register: (userData) => 
    api.post('/users/register/', userData),
  
  getProfile: () => 
    api.get('/users/me/'),
  
  updateProfile: (userData) => 
    api.put('/users/me/', userData),
};

// Core API
export const coreAPI = {
  // Employers
  getEmployers: () => api.get('/employers/'),
  createEmployer: (data) => api.post('/employers/', data),
  updateEmployer: (id, data) => api.put(`/employers/${id}/`, data),
  
  // Candidates
  getCandidates: () => api.get('/candidates/'),
  createCandidate: (data) => api.post('/candidates/', data),
  updateCandidate: (id, data) => api.put(`/candidates/${id}/`, data),
  
  // Vacancies
  getVacancies: () => api.get('/vacancies/'),
  getVacancy: (id) => api.get(`/vacancies/${id}/`),
  createVacancy: (data) => api.post('/vacancies/', data),
  updateVacancy: (id, data) => api.put(`/vacancies/${id}/`, data),
  getEmployerVacancies: () => api.get('/employers/vacancies/'),
  
  // Applications
  getApplications: () => api.get('/applications/'),
  getApplication: (id) => api.get(`/applications/${id}/`),
  createApplication: (data) => api.post('/applications/', data),
  updateApplication: (id, data) => api.put(`/applications/${id}/`, data),
  getCandidateApplications: () => api.get('/candidates/applications/'),
  getVacancyApplications: (vacancyId) => api.get(`/vacancies/${vacancyId}/applications/`),
  
  // Documents
  getDocuments: () => api.get('/documents/'),
  getDocument: (id) => api.get(`/documents/${id}/`),
  uploadDocument: (formData) => api.post('/documents/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getUserDocuments: () => api.get('/users/documents/'),
  getApplicationDocuments: (applicationId) => api.get(`/applications/${applicationId}/documents/`),
  
  // Visa Cases
  getVisaCases: () => api.get('/visa-cases/'),
  getVisaCase: (id) => api.get(`/visa-cases/${id}/`),
  createVisaCase: (data) => api.post('/visa-cases/', data),
  updateVisaCase: (id, data) => api.put(`/visa-cases/${id}/`, data),
  getOfficerVisaCases: () => api.get('/officers/visa-cases/'),
  
  // Housing
  getHousingListings: () => api.get('/housing/'),
  getHousingListing: (id) => api.get(`/housing/${id}/`),
  createHousingListing: (data) => api.post('/housing/', data),
  updateHousingListing: (id, data) => api.put(`/housing/${id}/`, data),
  
  // Relocation Suggestions
  getRelocationSuggestions: () => api.get('/relocation-suggestions/'),
  getRelocationSuggestion: (id) => api.get(`/relocation-suggestions/${id}/`),
  createRelocationSuggestion: (data) => api.post('/relocation-suggestions/', data),
  getApplicationRelocationSuggestions: (applicationId) => 
    api.get(`/applications/${applicationId}/relocation-suggestions/`),
  
  // Expense Estimates
  getExpenseEstimates: () => api.get('/expense-estimates/'),
  getExpenseEstimate: (id) => api.get(`/expense-estimates/${id}/`),
  createExpenseEstimate: (data) => api.post('/expense-estimates/', data),
  updateExpenseEstimate: (id, data) => api.put(`/expense-estimates/${id}/`, data),
  getApplicationExpenseEstimates: (applicationId) => 
    api.get(`/applications/${applicationId}/expense-estimates/`),
  
  // AI Interactions
  getAIInteractions: () => api.get('/ai-interactions/'),
  getAIInteraction: (id) => api.get(`/ai-interactions/${id}/`),
  createAIInteraction: (data) => api.post('/ai-interactions/', data),
  getUserAIInteractions: () => api.get('/users/ai-interactions/'),
  getApplicationAIInteractions: (applicationId) => 
    api.get(`/applications/${applicationId}/ai-interactions/`),
  
  // Dashboard
  getDashboardStats: () => api.get('/dashboard/stats/'),
};

export default api;
