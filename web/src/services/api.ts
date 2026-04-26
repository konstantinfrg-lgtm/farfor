import axios from 'axios';
import { Item, User, LoginData, RegisterData, AuthResponse } from '../types';

const API_BASE = '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  login: async (data: LoginData): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/auth/login', data);
    return response.data;
  },

  register: async (data: RegisterData): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/auth/register', data);
    return response.data;
  },

  getMe: async (): Promise<User> => {
    const response = await api.get<User>('/auth/me');
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
};

export const itemService = {
  getAll: async (search?: string, isPublicOnly?: boolean): Promise<Item[]> => {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (isPublicOnly) params.append('public_only', 'true');
    
    const response = await api.get<Item[]>(`/items?${params.toString()}`);
    return response.data;
  },

  getById: async (id: number): Promise<Item> => {
    const response = await api.get<Item>(`/items/${id}`);
    return response.data;
  },

  create: async (formData: FormData): Promise<Item> => {
    const response = await api.post<Item>('/items', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  update: async (id: number, formData: FormData): Promise<Item> => {
    const response = await api.put<Item>(`/items/${id}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/items/${id}`);
  },

  togglePublic: async (id: number): Promise<Item> => {
    const response = await api.patch<Item>(`/items/${id}/toggle-public`);
    return response.data;
  },

  getMyItems: async (): Promise<Item[]> => {
    const response = await api.get<Item[]>('/items/my');
    return response.data;
  },

  getUserPublicItems: async (userId: number): Promise<Item[]> => {
    const response = await api.get<Item[]>(`/items/user/${userId}/public`);
    return response.data;
  },
};

export const publicService = {
  getPublicItems: async (search?: string): Promise<Item[]> => {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    params.append('public_only', 'true');
    
    const response = await api.get<Item[]>(`/items?${params.toString()}`);
    return response.data;
  },

  getPublicCollections: async (): Promise<User[]> => {
    const response = await api.get<User[]>('/users/public-collections');
    return response.data;
  },
};

export default api;
