import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://rasan-ai-labs-production.up.railway.app/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadFile = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const preprocessData = async (filename: string) => {
  const response = await api.post(`/preprocess/${filename}`);
  return response.data;
};

export const analyzeData = async (filename: string, targetColumn?: string) => {
  const response = await api.post('/analyze', { 
    filename, 
    target_column: targetColumn || undefined 
  });
  return response.data;
};

export const trainModel = async (data: {
  filename: string;
  target: string;
  problem_type: string;
  model_name?: string;
  features?: string[];
}) => {
  const response = await api.post('/train', data);
  return response.data;
};

export const getModel = async (modelId: string) => {
  const response = await api.get(`/models/${modelId}`);
  return response.data;
};

export const predict = async (modelId: string, data: Record<string, any>) => {
  const response = await api.post('/predict', { model_id: modelId, data });
  return response.data;
};
