/** Backend API authentication utilities for Todo App frontend */

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterData {
  email: string;
  password: string;
  name?: string;
}

interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

interface SessionData {
  user: {
    id: string;
    email: string;
    name?: string;
  };
  access_token: string;
  token_type: string;
}

// Get API base URL from environment or use default
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

/**
 * Login a user using backend API
 */
export async function loginWithBackend(credentials: LoginCredentials): Promise<ApiResponse<SessionData>> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: credentials.email,
        password: credentials.password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return {
        success: false,
        error: data.detail || 'Login failed',
      };
    }

    // Store the token in localStorage for API requests
    if (data.access_token) {
      localStorage.setItem('access_token', data.access_token);
    }

    return {
      success: true,
      data: {
        user: {
          id: data.access_token ? extractUserIdFromToken(data.access_token) : '',
          email: credentials.email,
          name: data.user?.name || '',
        },
        access_token: data.access_token,
        token_type: data.token_type,
      },
    };
  } catch (error: any) {
    console.error('Login error:', error);
    return {
      success: false,
      error: error.message || 'Login failed',
    };
  }
}

/**
 * Register a user using backend API
 */
export async function registerWithBackend(userData: RegisterData): Promise<ApiResponse<SessionData>> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: userData.email,
        password: userData.password,
        name: userData.name || userData.email.split('@')[0],
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return {
        success: false,
        error: data.detail || 'Registration failed',
      };
    }

    // Store the token in localStorage for API requests
    if (data.access_token) {
      localStorage.setItem('access_token', data.access_token);
    }

    return {
      success: true,
      data: {
        user: {
          id: data.id || '',
          email: data.email,
          name: data.name || '',
        },
        access_token: data.access_token || '',
        token_type: 'bearer',
      },
    };
  } catch (error: any) {
    console.error('Registration error:', error);
    return {
      success: false,
      error: error.message || 'Registration failed',
    };
  }
}

/**
 * Get current user session
 */
export async function getSessionFromBackend(): Promise<SessionData | null> {
  const token = localStorage.getItem('access_token');
  if (!token) {
    return null;
  }

  try {
    // For now, just return a session based on the stored token
    // In a real implementation, you'd validate the token with the backend
    return {
      user: {
        id: extractUserIdFromToken(token),
        email: localStorage.getItem('user_email') || '',
        name: localStorage.getItem('user_name') || '',
      },
      access_token: token,
      token_type: 'bearer',
    };
  } catch (error) {
    console.error('Get session error:', error);
    return null;
  }
}

/**
 * Logout user
 */
export async function logoutFromBackend(): Promise<boolean> {
  try {
    // Clear stored tokens
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_email');
    localStorage.removeItem('user_name');

    return true;
  } catch (error) {
    console.error('Logout error:', error);
    return false;
  }
}

/**
 * Helper function to extract user ID from JWT token
 * This is a simplified implementation - in production, use a proper JWT library
 */
function extractUserIdFromToken(token: string): string {
  try {
    // Split the token to get the payload part
    const parts = token.split('.');
    if (parts.length !== 3) return '';

    // Decode the payload (second part)
    const payload = parts[1];
    // Add padding if needed
    const paddedPayload = payload + '='.repeat((4 - payload.length % 4) % 4);
    const decodedPayload = atob(paddedPayload);
    const parsed = JSON.parse(decodedPayload);

    // Return the subject (sub) which should be the user ID
    return parsed.sub || parsed.userId || parsed.id || '';
  } catch (error) {
    console.error('Error decoding token:', error);
    return '';
  }
}

/**
 * Get auth token for API requests
 */
export function getAuthToken(): string | null {
  return localStorage.getItem('access_token');
}

/**
 * Check if user is authenticated
 */
export async function isAuthenticated(): Promise<boolean> {
  const session = await getSessionFromBackend();
  return !!session;
}

/**
 * Get current user ID
 */
export async function getCurrentUserId(): Promise<string | null> {
  const session = await getSessionFromBackend();
  return session?.user?.id || null;
}