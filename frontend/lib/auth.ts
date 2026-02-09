/** Custom Auth integration for Todo App frontend */

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

  return null;
}

/**
 * Sign in a user
 */
export async function loginUser(credentials: { email: string; password: string }): Promise<{ success: boolean; error?: string }> {
  try {
    // Use the correct API endpoint for login
    const baseURL = (process.env.NEXT_PUBLIC_API_BASE_URL || '').replace(/\/$/, '');
    const fullUrl = baseURL ? `${baseURL}/api/v1/auth/login` : '/api/v1/auth/login';
    const response = await fetch(fullUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: credentials.email,
        password: credentials.password
      }),
      credentials: 'include' // Include cookies in cross-origin requests
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Login failed' }));
      return { success: false, error: errorData.detail || `Login failed with status: ${response.status}` };
    }

    const result = await response.json();
    
    // Create session data to store in localStorage
    const sessionData = {
      user: {
        id: result.user_id || result.id || 'unknown',
        email: result.email || credentials.email,
        name: result.name || credentials.email.split('@')[0] || 'User'
      },
      token: result.access_token || result.token || '',
      expires: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // 24 hours
    };

    // Store the session data in localStorage
    if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
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
    return { success: false, error: errorMessage };
  }
}

/**
 * Sign up a new user
 */
export async function registerUser(userData: { email: string; password: string; name?: string }): Promise<{ success: boolean; error?: string }> {
  try {
    // Use the correct API endpoint for registration
    const baseURL = (process.env.NEXT_PUBLIC_API_BASE_URL || '').replace(/\/$/, '');
    const fullUrl = baseURL ? `${baseURL}/api/v1/auth/register` : '/api/v1/auth/register';
    const response = await fetch(fullUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: userData.email,
        password: userData.password,
        name: userData.name || userData.email.split('@')[0]
      }),
      credentials: 'include' // Include cookies in cross-origin requests
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Registration failed' }));
      return { success: false, error: errorData.detail || `Registration failed with status: ${response.status}` };
    }

    const result = await response.json();
    
    // Create session data to store in localStorage
    const sessionData = {
      user: {
        id: result.user_id || result.id || 'unknown',
        email: result.email || userData.email,
        name: result.name || userData.name || userData.email.split('@')[0] || 'User'
      },
      token: result.access_token || result.token || '',
      expires: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // 24 hours
    };

    // Store the session data in localStorage
    if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
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
    console.error('Registration error:', error);
    // Provide user-friendly error messages
    let errorMessage = error.message || 'Registration failed';
    return { success: false, error: errorMessage };
  }
}

/**
 * Sign out the current user
 */
export async function logoutUser(): Promise<boolean> {
  try {
    // Call the logout API endpoint
    const baseURL = (process.env.NEXT_PUBLIC_API_BASE_URL || '').replace(/\/$/, '');
    const fullUrl = baseURL ? `${baseURL}/api/v1/auth/logout` : '/api/v1/auth/logout';
    const response = await fetch(fullUrl, {
      method: 'POST',
      credentials: 'include' // Include cookies in cross-origin requests
    });

    // Even if the API call fails, clear local storage
    if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
      try {
        localStorage.removeItem('user_session');
        console.log('Session cleared from localStorage'); // Debug log
      } catch (storageError) {
        console.error('Error clearing session from localStorage:', storageError);
      }
    }

    return response.ok;
  } catch (error) {
    console.error('Logout error:', error);
    // Still clear local storage even if API call fails
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
    // Check if we have session data in localStorage
    if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
      try {
        const storedSession = localStorage.getItem('user_session');
        console.log('Checking localStorage for session:', storedSession); // Debug log
        if (storedSession) {
          const parsedSession = JSON.parse(storedSession);
          
          // Check if session has expired
          const now = new Date();
          const expiresAt = new Date(parsedSession.expires || Date.now() + 30 * 60 * 1000);
          
          if (now < expiresAt) {
            return true;
          } else {
            // Session has expired, remove from localStorage
            localStorage.removeItem('user_session');
            return false;
          }
        }
        return false;
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