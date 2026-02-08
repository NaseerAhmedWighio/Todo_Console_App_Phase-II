/** Better Auth integration for Todo App frontend */
import { createAuthClient } from 'better-auth/react';
import { useAuthQuery } from 'better-auth/react';

// Initialize Better Auth client to communicate with our backend API
// The backend now has Better Auth compatible endpoints at /api/auth/*
const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  fetchOptions: {
    credentials: 'include' as const,
  },
  // Ensure session is handled properly
  plugins: [],
});

// Type for session data
interface SessionData {
  user: {
    id: string;
    email: string;
    name?: string;
  };
  token: string;
  expiresAt: Date;
}

/**
 * Get the current user session
 */
export async function getSession(): Promise<SessionData | null> {
  // First, try to get from localStorage
  if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
    try {
      const storedSession = localStorage.getItem('user_session');
      if (storedSession) {
        const parsedSession = JSON.parse(storedSession);
        console.log('Retrieved stored session:', parsedSession); // Debug log
        
        // Check if session has expired
        const now = new Date();
        const expiresAt = new Date(parsedSession.expires || Date.now() + 30 * 60 * 1000);
        
        if (now >= expiresAt) {
          // Session has expired, remove from localStorage
          localStorage.removeItem('user_session');
          console.log('Session expired, removed from localStorage'); // Debug log
          return null;
        }
        
        return {
          user: {
            id: parsedSession.user.id || 'unknown',
            email: parsedSession.user.email || 'unknown',
            name: parsedSession.user.name || 'User',
          },
          token: parsedSession.token || parsedSession.user.id || '',
          expiresAt: expiresAt,
        };
      }
    } catch (parseError) {
      console.error('Error parsing stored session:', parseError);
      // Clear invalid session data
      if (typeof localStorage !== 'undefined') {
        localStorage.removeItem('user_session');
      }
    }
  }

  // If not in localStorage, try to get from Better Auth
  try {
    const session = await authClient.getSession();
    if (session?.data) {
      // Check if Better Auth session is valid
      const now = new Date();
      const expiresAt = new Date(session.data.expires || Date.now() + 30 * 60 * 1000);
      
      if (now >= expiresAt) {
        // Session has expired
        console.log('Better Auth session expired'); // Debug log
        return null;
      }
      
      // Update localStorage with fresh session data
      const sessionData = {
        user: {
          id: session.data.data.user.id || 'unknown',
          email: session.data.data.user.email || 'unknown',
          name: session.data.data.user.name || 'User',
        },
        token: session.data.data.token || '',
        expires: session.data.data.expires || new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
      };
      
      if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
        try {
          localStorage.setItem('user_session', JSON.stringify(sessionData));
          console.log('Session updated in localStorage:', sessionData); // Debug log
        } catch (storageError) {
          console.error('Error updating session in localStorage:', storageError);
        }
      }
      
      return {
        user: {
          id: session.data.data.user.id || 'unknown',
          email: session.data.data.user.email || 'unknown',
          name: session.data.data.user.name || 'User',
        },
        token: session.data.data.token || session.data.data.user.id || '', // Use user ID as fallback token
        expiresAt: expiresAt,
      };
    }
  } catch (error) {
    console.error('Error getting session from Better Auth:', error);
  }

  return null;
}

/**
 * Sign in a user
 */
export async function loginUser(credentials: { email: string; password: string }): Promise<{ success: boolean; error?: string }> {
  try {
    const result = await authClient.signIn.credentials({
      email: credentials.email,
      password: credentials.password,
      redirect: false,
    });

    if (result.error) {
      // Provide user-friendly error messages
      let errorMessage = result.error.message || 'Login failed';
      if (errorMessage.toLowerCase().includes('password') || errorMessage.toLowerCase().includes('72 bytes')) {
        errorMessage = 'Password validation failed. Please try a different password.';
      }
      return { success: false, error: errorMessage };
    }

    // Wait to ensure session is properly established
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Get the session from Better Auth to ensure it's ready
    let sessionResult = null;
    try {
      sessionResult = await authClient.getSession();
      console.log('Better Auth session result:', sessionResult); // Debug log
    } catch (sessionError) {
      console.error('Error getting Better Auth session:', sessionError);
    }
    
    // Create session data to store in localStorage
    let sessionData = null;
    
    if (sessionResult?.data?.data) {
      // Use data from Better Auth if available
      sessionData = {
        user: {
          id: sessionResult.data.data.user.id || 'unknown',
          email: sessionResult.data.data.user.email || credentials.email,
          name: sessionResult.data.data.user.name || credentials.email.split('@')[0]
        },
        token: sessionResult.data.data.token || '',
        expires: sessionResult.data.data.expires || new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
      };
    } else {
      // If Better Auth session isn't ready, make a direct API call to get user data
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/v1/auth/me`, {
          method: 'GET',
          credentials: 'include', // Include cookies
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        console.log('API response status:', response.status); // Debug log
        
        if (response.ok) {
          const userData = await response.json();
          console.log('User data received:', userData); // Debug log
          
          sessionData = {
            user: {
              id: userData.id || userData.user_id || userData.sub || 'unknown',
              email: userData.email || userData.username || credentials.email,
              name: userData.name || userData.full_name || userData.email?.split('@')[0] || credentials.email.split('@')[0] || 'User'
            },
            token: '', // Token will come from Better Auth cookies
            expires: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // 24 hours
          };
        } else {
          // If API call fails, create a minimal session based on login credentials
          sessionData = {
            user: {
              id: 'unknown', // Will be updated later when API works
              email: credentials.email,
              name: credentials.email.split('@')[0] || 'User'
            },
            token: '',
            expires: new Date(Date.now() + 1 * 60 * 60 * 1000).toISOString() // 1 hour
          };
        }
      } catch (apiError) {
        console.error('Error fetching user data after login:', apiError);
        // Create a minimal session based on login credentials
        sessionData = {
          user: {
            id: 'unknown', // Will be updated later when API works
            email: credentials.email,
            name: credentials.email.split('@')[0] || 'User'
          },
          token: '',
          expires: new Date(Date.now() + 1 * 60 * 60 * 1000).toISOString() // 1 hour
        };
      }
    }
    
    // Store the session data in localStorage
    if (sessionData && typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
      try {
        localStorage.setItem('user_session', JSON.stringify(sessionData));
        console.log('Session stored in localStorage:', sessionData); // Debug log
        return { success: true };
      } catch (storageError) {
        console.error('Error storing session in localStorage:', storageError);
        return { success: false, error: 'Failed to store session' };
      }
    } else {
      console.error('No session data to store');
      return { success: false, error: 'No session data to store' };
    }
  } catch (error: any) {
    console.error('Login error:', error);
    // Provide user-friendly error messages
    let errorMessage = error.message || 'Login failed';
    if (errorMessage.toLowerCase().includes('password') || errorMessage.toLowerCase().includes('72 bytes')) {
      errorMessage = 'Password validation failed. Please try a different password.';
    }
    return { success: false, error: errorMessage };
  }
}

/**
 * Sign up a new user
 */
export async function registerUser(userData: { email: string; password: string; name?: string }): Promise<{ success: boolean; error?: string }> {
  try {
    const result = await authClient.signUp.email({
      email: userData.email,
      password: userData.password,
      name: userData.name || userData.email.split('@')[0],
      redirect: false,
    });

    if (result.error) {
      // Provide user-friendly error messages
      let errorMessage = result.error.message || 'Registration failed';
      if (errorMessage.toLowerCase().includes('password') || errorMessage.toLowerCase().includes('72 bytes')) {
        errorMessage = 'Password validation failed. Please try a different password.';
      }
      return { success: false, error: errorMessage };
    }

    return { success: true };
  } catch (error: any) {
    console.error('Registration error:', error);
    // Provide user-friendly error messages
    let errorMessage = error.message || 'Registration failed';
    if (errorMessage.toLowerCase().includes('password') || errorMessage.toLowerCase().includes('72 bytes')) {
      errorMessage = 'Password validation failed. Please try a different password.';
    }
    return { success: false, error: errorMessage };
  }
}

/**
 * Sign out the current user
 */
export async function logoutUser(): Promise<boolean> {
  try {
    const result = await authClient.signOut({
      redirect: false,
    });

    // Clear local storage
    if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
      try {
        localStorage.removeItem('user_session');
        console.log('Session cleared from localStorage'); // Debug log
      } catch (storageError) {
        console.error('Error clearing session from localStorage:', storageError);
      }
    }

    return !result.error;
  } catch (error) {
    console.error('Logout error:', error);
    // Still clear local storage even if Better Auth sign out fails
    if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
      try {
        localStorage.removeItem('user_session');
        console.log('Session cleared from localStorage after error'); // Debug log
      } catch (storageError) {
        console.error('Error clearing session from localStorage:', storageError);
      }
    }
    return false;
  }
}

/**
 * Check if the user is authenticated
 */
export async function isAuthenticated(): Promise<boolean> {
  try {
    // First try to get session through Better Auth
    const session = await getSession();
    if (session) {
      return true;
    }
    
    // If that fails, try to directly check with Better Auth client
    try {
      const authStatus = await authClient.getSession();
      if (authStatus?.data?.data) {
        // Update localStorage with fresh session data if available
        const sessionData = {
          user: authStatus.data.data.user,
          token: authStatus.data.data.token,
          expires: authStatus.data.data.expires
        };
        if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
          try {
            localStorage.setItem('user_session', JSON.stringify(sessionData));
          } catch (storageError) {
            console.error('Error storing session in localStorage:', storageError);
          }
        }
        return true;
      }
    } catch (innerError) {
      console.error('Direct auth check error:', innerError);
    }
    
    // Final fallback: check if we have session data in localStorage
    if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
      try {
        const storedSession = localStorage.getItem('user_session');
        console.log('Checking localStorage for session:', storedSession); // Debug log
        return !!storedSession;
      } catch (storageError) {
        console.error('Error checking localStorage:', storageError);
        return false;
      }
    }
    
    return false;
  } catch (error) {
    console.error('Auth check error:', error);
    return false;
  }
}

/**
 * Get the current user ID
 */
export async function getCurrentUserId(): Promise<string | null> {
  // First try to get from localStorage
  if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
    try {
      const storedSession = localStorage.getItem('user_session');
      if (storedSession) {
        const parsedSession = JSON.parse(storedSession);
        return parsedSession.user?.id || null;
      }
    } catch (parseError) {
      console.error('Error parsing stored session for user ID:', parseError);
    }
  }

  try {
    const session = await getSession();
    return session?.user?.id || null;
  } catch (error) {
    console.error('Get user ID error:', error);
    return null;
  }
}

// Export the auth client for use in components
export { authClient };