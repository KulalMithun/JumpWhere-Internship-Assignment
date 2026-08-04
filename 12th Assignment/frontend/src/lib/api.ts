import axios from 'axios';
import { getAuthToken } from './auth';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '';

export const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = getAuthToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface DocumentItem {
  id: string;
  filename: string;
  file_type: string;
  file_size: number;
  chunk_count: number;
  created_at: string;
  owner_id: string;
}

export interface SourceChunk {
  chunk_id: string;
  page?: number;
  content: string;
  score: number;
  document_id: string;
  document_name: string;
}

export interface ChatMessageItem {
  id: string;
  sender: 'user' | 'assistant';
  content: string;
  confidence_score?: number;
  sources?: SourceChunk[];
  prompt_tokens?: number;
  completion_tokens?: number;
  total_cost?: number;
  created_at?: string;
}

export interface ChatSessionItem {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  messages: ChatMessageItem[];
}

export interface ChatResponse {
  session_id: string;
  message_id: string;
  answer: string;
  confidence_score: number;
  retrieved_chunk_count: number;
  source_pages: number[];
  sources: SourceChunk[];
  prompt_tokens: number;
  completion_tokens: number;
  total_cost: number;
}
