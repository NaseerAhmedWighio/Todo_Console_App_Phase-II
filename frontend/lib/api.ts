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

    // Then try to get token from Better Auth client
    try {
      const { authClient } = await import('./auth');
      const authSession = await authClient.getSession();
      if (authSession?.data) {
        // Better Auth typically stores session tokens in cookies, not in the returned data
        // The session data contains user info but not necessarily a separate token
        // Return the user ID as a fallback or handle as needed
        return authSession.data.user?.id || null;
      }
    } catch (error) {
      console.error('Error getting auth token from Better Auth client:', error);
    }

    // Fallback: try to get from document cookies
    if (typeof document !== 'undefined') {
      const cookies = document.cookie.split(';');
      for (const cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'better-auth-session') {
          return value;
        }
      }
    }

    return null;
  }

  // Authentication methods - these should use the auth.ts functions instead
  // This API client is for task operations only

  // Task methods - these should match the backend API which has /api/v1 prefix
  async getTasks(userId: string): Promise<Task[]> {
    return this.request(`/api/v1/tasks/${userId}/tasks`);
  }

  async createTask(userId: string, taskData: { title: string; description?: string; completed?: boolean }) {
    return this.request(`/api/v1/tasks/${userId}/tasks`, {
      method: 'POST',
      body: taskData,
    });
  }

  async getTask(userId: string, taskId: number): Promise<Task> {
    return this.request(`/api/v1/tasks/${userId}/tasks/${taskId}`);
  }

  async updateTask(userId: string, taskId: number, taskData: { title: string; description?: string; completed: boolean }) {
    return this.request(`/api/v1/tasks/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: taskData,
    });
  }

  async deleteTask(userId: string, taskId: number) {
    return this.request(`/api/v1/tasks/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskCompletion(userId: string, taskId: number, completed: boolean) {
    return this.request(`/api/v1/tasks/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
      body: { completed },
    });
  }
}

// Export a singleton instance
export const apiClient = new ApiClient();