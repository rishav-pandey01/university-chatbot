import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

// Attach JWT token to every request if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 responses globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      // Only redirect if not already on auth page
      if (!window.location.pathname.startsWith('/login') && !window.location.pathname.startsWith('/register')) {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// ── Auth ──
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
};

// ── Chat ──
export const chatAPI = {
  sendMessage: (data) => api.post('/chat/message', data),
  getSuggested: () => api.get('/chat/suggested'),
  getConversations: () => api.get('/chat/conversations'),
  getConversation: (id) => api.get(`/chat/conversations/${id}`),
  deleteConversation: (id) => api.delete(`/chat/conversations/${id}`),
  clearAllConversations: () => api.delete('/chat/conversations'),
};

// ── FAQs ──
export const faqAPI = {
  getAll: (params) => api.get('/faqs', { params }),
  getCategories: () => api.get('/faqs/categories'),
  getById: (id) => api.get(`/faqs/${id}`),
  create: (data) => api.post('/faqs', data),
  update: (id, data) => api.put(`/faqs/${id}`, data),
  delete: (id) => api.delete(`/faqs/${id}`),
};

// ── Announcements ──
export const announcementAPI = {
  getActive: () => api.get('/announcements'),
  getAll: () => api.get('/announcements/all'),
  create: (data) => api.post('/announcements', data),
  update: (id, data) => api.put(`/announcements/${id}`, data),
  delete: (id) => api.delete(`/announcements/${id}`),
};

// ── Documents ──
export const documentAPI = {
  getAll: () => api.get('/documents'),
  upload: (formData) =>
    api.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  delete: (id) => api.delete(`/documents/${id}`),
};

// ── Feedback ──
export const feedbackAPI = {
  submit: (data) => api.post('/feedback', data),
  getAll: () => api.get('/feedback'),
};

// ── Analytics ──
export const analyticsAPI = {
  getDashboard: () => api.get('/analytics/dashboard'),
  getUnanswered: () => api.get('/analytics/unanswered'),
  resolveQuery: (id, data) => api.put(`/analytics/unanswered/${id}/resolve`, data),
};

export default api;
