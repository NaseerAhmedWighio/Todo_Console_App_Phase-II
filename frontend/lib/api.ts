/** API client for Todo App frontend */
import { getSession } from './auth';

export interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface ApiOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  body?: any;
  headers?: Record<string, string>;
}

export class ApiClient {
  private baseUrl: string;

  constructor() {
    // Use the backend API URL for task operations
    this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
  }

  private async request<T>(endpoint: string, options: ApiOptions = {}): Promise<T> {
    const { method = 'GET', body, headers = {} } = options;

    // Get auth token if available
    const token = await this.getAuthToken();
    const authHeaders = token ? { 'Authorization': `Bearer ${token}` } : {};

    // Construct the full URL
    const url = `${this.baseUrl}${endpoint}`;

    // Prepare request options
    const requestOptions: RequestInit = {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...authHeaders,
        ...headers,
      },
      // Include credentials to send cookies along with the request
      credentials: 'include',
      ...(body && { body: JSON.stringify(body) }),
    };

    try {
      // Use a direct fetch that bypasses any interceptors
      const response = await fetch(url, requestOptions);

      // Handle different status codes
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Unknown error' }));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
      }

      // Don't try to parse body for 204 No Content responses
      if (response.status === 204) {
        return undefined as T;
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed: ${method} ${url}`, error);
      throw error;
    }
  }

  private async getAuthToken(): Promise<string | null> {
    // First, try to get token from localStorage
    if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
      try {
        const storedSession = localStorage.getItem('user_session');
        if (storedSession) {
          const parsedSession = JSON.parse(storedSession);
          if (parsedSession.token) {
            return parsedSession.token;
          }
          // If no token in stored session, try to get from user data
          if (parsedSession.user?.id) {
            // Return the user ID as a fallback token if needed
            return parsedSession.user.id;
          }
        }
      } catch (parseError) {
        console.error('Error parsing stored session for token:', parseError);
      }
    }

    return null;
  }

  // Authentication methods - these should use the auth.ts functions instead
  // This API client is for task operations only

  // Task methods - these should match the backend API structure based on documentation
  async getTasks(userId?: string): Promise<Task[]> {
    const actualUserId = userId || await this.getCurrentUserId();
    if (!actualUserId) {
      throw new Error('User not authenticated');
    }
    return this.request(`/api/v1/tasks/${actualUserId}/tasks`);
  }

  async createTask(taskData: { title: string; description?: string; completed?: boolean }, userId?: string) {
    const actualUserId = userId || await this.getCurrentUserId();
    if (!actualUserId) {
      throw new Error('User not authenticated');
    }
    return this.request(`/api/v1/tasks/${actualUserId}/tasks`, {
      method: 'POST',
      body: taskData,
    });
  }

  async getTask(taskId: number, userId?: string): Promise<Task> {
    const actualUserId = userId || await this.getCurrentUserId();
    if (!actualUserId) {
      throw new Error('User not authenticated');
    }
    return this.request(`/api/v1/tasks/${actualUserId}/tasks/${taskId}`);
  }

  async updateTask(taskId: number, taskData: { title: string; description?: string; completed: boolean }, userId?: string) {
    const actualUserId = userId || await this.getCurrentUserId();
    if (!actualUserId) {
      throw new Error('User not authenticated');
    }
    return this.request(`/api/v1/tasks/${actualUserId}/tasks/${taskId}`, {
      method: 'PUT',
      body: taskData,
    });
  }

  async deleteTask(taskId: number, userId?: string) {
    const actualUserId = userId || await this.getCurrentUserId();
    if (!actualUserId) {
      throw new Error('User not authenticated');
    }
    return this.request(`/api/v1/tasks/${actualUserId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskCompletion(taskId: number, completed: boolean, userId?: string) {
    const actualUserId = userId || await this.getCurrentUserId();
    if (!actualUserId) {
      throw new Error('User not authenticated');
    }
    return this.request(`/api/v1/tasks/${actualUserId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
      body: { completed },
    });
  }

  private async getCurrentUserId(): Promise<string | null> {
    try {
      const storedSession = typeof window !== 'undefined' ? localStorage.getItem('user_session') : null;
      if (storedSession) {
        const parsedSession = JSON.parse(storedSession);
        return parsedSession.user?.id || null;
      }
    } catch (error) {
      console.error('Error getting current user ID:', error);
    }
    return null;
  }
}

// Export a singleton instance
export const apiClient = new ApiClient();