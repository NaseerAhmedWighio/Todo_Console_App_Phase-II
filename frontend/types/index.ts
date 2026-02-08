// Task-related types
export interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface TaskCreateData {
  title: string;
  description?: string;
  completed?: boolean;
}

export interface TaskUpdateData {
  title?: string;
  description?: string;
  completed?: boolean;
}

// User-related types
export interface User {
  id: string;
  email: string;
  name?: string;
}

export interface SessionData {
  user: User;
  token: string;
  expiresAt: Date;
}

// API response types
export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

// UI component types
export interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'accent' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

export interface CardProps {
  children: React.ReactNode;
  className?: string;
  hoverEffect?: boolean;
  border?: boolean;
}

// Filter and search types
export type TaskFilter = 'all' | 'completed' | 'pending';

// Error types
export interface ApiError {
  message: string;
  code?: string;
  status?: number;
}