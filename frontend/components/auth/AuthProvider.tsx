// 'use client';

// import React, { createContext, useContext, useEffect, useState } from 'react';
// import { useRouter, usePathname } from 'next/navigation';

// interface User {
//   id: string;
//   email: string;
//   name?: string;
// }

// interface AuthContextType {
//   user: User | null;
//   isAuthenticated: boolean;
//   isLoading: boolean;
//   login: (userData: User, token: string, expiresAt: string) => void;
//   logout: () => void;
//   refreshAuth: () => void;
// }

// const AuthContext = createContext<AuthContextType | undefined>(undefined);

// // Public routes that don't require authentication
// const PUBLIC_ROUTES = ['/login', '/register', '/'];

// export function AuthProvider({ children }: { children: React.ReactNode }) {
//   const [user, setUser] = useState<User | null>(null);
//   const [isAuthenticated, setIsAuthenticated] = useState(false);
//   const [isLoading, setIsLoading] = useState(true);
//   const router = useRouter();
//   const pathname = usePathname();

//   // Check localStorage for existing session
//   const checkAuthFromStorage = () => {
//     if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
//       try {
//         const storedSession = localStorage.getItem('user_session');
//         if (storedSession) {
//           const parsedSession = JSON.parse(storedSession);
          
//           // Check if session has expired
//           const now = new Date();
//           const expiresAt = new Date(parsedSession.expiresAt);
          
//           if (now >= expiresAt) {
//             console.log('🕐 Session expired, clearing localStorage');
//             localStorage.removeItem('user_session');
//             return null;
//           }
          
//           console.log('✅ Valid session found in localStorage:', parsedSession.user);
//           return parsedSession;
//         }
//       } catch (error) {
//         console.error('❌ Error parsing stored session:', error);
//         localStorage.removeItem('user_session');
//       }
//     }
//     return null;
//   };

//   // Login function
//   const login = (userData: User, token: string, expiresAt: string) => {
//     const sessionData = {
//       user: userData,
//       token,
//       expiresAt,
//     };

//     setUser(userData);
//     setIsAuthenticated(true);

//     // Store in localStorage
//     if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
//       try {
//         localStorage.setItem('user_session', JSON.stringify(sessionData));
//         console.log('✅ Session stored in localStorage');
//       } catch (error) {
//         console.error('❌ Error storing session:', error);
//       }
//     }
//   };

//   // Logout function
// const logout = async () => {
//   console.log('🚪 Logging out user');

//   // 1. Clear frontend state first
//   setUser(null);
//   setIsAuthenticated(false);

//   // 2. Clear storage
//   if (typeof window !== 'undefined') {
//     localStorage.removeItem('user_session');
//     // Optional: clear any other keys you might use
//     // localStorage.removeItem('token');
//   }

//   // 3. Optional backend logout (best effort – don't block UI on it)
//   try {
//     const sessionStr = localStorage.getItem('user_session'); // already removed, but for reference
//     // If you want to call logout endpoint, do it before clearing or use a stored token copy
//     await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/v1/auth/logout`, {
//       method: 'POST',
//       credentials: 'include',
//       headers: { 'Content-Type': 'application/json' },
//     }).catch(() => {}); // silent fail is ok for logout
//   } catch {}

//   // 4. Force navigation
//   router.replace('/login');

//   // Optional: refresh page to break any lingering state
//   // router.refresh(); // Next.js 13+ can help in some cases
// };

//   // Refresh auth status
//   const refreshAuth = () => {
//     const session = checkAuthFromStorage();
//     if (session) {
//       setUser(session.user);
//       setIsAuthenticated(true);
//     } else {
//       setUser(null);
//       setIsAuthenticated(false);
//     }
//   };

//   // Check authentication on mount and route changes
//   useEffect(() => {
//     const initAuth = () => {
//       const session = checkAuthFromStorage();
      
//       if (session) {
//         setUser(session.user);
//         setIsAuthenticated(true);
//         console.log('✅ User authenticated:', session.user.email);
//       } else {
//         setUser(null);
//         setIsAuthenticated(false);
//         console.log('❌ No valid session found');
//       }
      
//       setIsLoading(false);
//     };

//     initAuth();
//   }, []);

//   // Handle route protection
// // AuthProvider.tsx (relevant part)

// // 1. First useEffect: load/check initial session from localStorage
// useEffect(() => {
//   const initAuth = () => {
//     const session = checkAuthFromStorage();
    
//     if (session) {
//       setUser(session.user);
//       setIsAuthenticated(true);
//       console.log('✅ User authenticated:', session.user.email);
//     } else {
//       setUser(null);
//       setIsAuthenticated(false);
//       console.log('❌ No valid session found');
//     }
    
//     setIsLoading(false);
//   };

//   initAuth();
// }, []);   // ← only on mount


// // 2. Second useEffect: route protection + auth page redirect
// useEffect(() => {
//   if (isLoading) return;

//   const isPublic = PUBLIC_ROUTES.includes(pathname);

//   if (!isAuthenticated && !isPublic) {
//     console.log(`Protecting ${pathname} → redirect to /login`);
//     router.replace('/login');
//   } 
//   else if (isAuthenticated && (pathname === '/login' || pathname === '/register')) {
//     console.log(`Authenticated user on auth page → redirect to /dashboard`);
//     router.replace('/dashboard');
//   }
// }, [isAuthenticated, isLoading, pathname, router]);

//   return (
//     <AuthContext.Provider 
//       value={{
//         user,
//         isAuthenticated,
//         isLoading,
//         login,
//         logout,
//         refreshAuth,
//       }}
//     >
//       {children}
//     </AuthContext.Provider>
//   );
// }

// export function useAuth() {
//   const context = useContext(AuthContext);
//   if (context === undefined) {
//     throw new Error('useAuth must be used within an AuthProvider');
//   }
//   return context;
// }










'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { loginUser, getSession, isAuthenticated as checkIsAuthenticated, logoutUser } from '@/lib/auth';

interface User {
  id: string;
  email: string;
  name?: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: { email: string; password: string }) => Promise<{ success: boolean; error?: string }>;
  logout: () => Promise<void>;
  refreshAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const PUBLIC_ROUTES = ['/login', '/register', '/'];

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticatedState, setIsAuthenticatedState] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  // Initialize auth state from localStorage
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        // Add a small delay to ensure all initialization is complete
        await new Promise(resolve => setTimeout(resolve, 100));
        
        const authenticated = await checkIsAuthenticated();
        console.log('AuthProvider: Initial auth check result:', authenticated); // Debug log
        
        setIsAuthenticatedState(authenticated);
        
        if (authenticated) {
          const session = await getSession();
          console.log('AuthProvider: Session data:', session); // Debug log
          
          if (session?.user) {
            setUser({
              id: session.user.id,
              email: session.user.email,
              name: session.user.name,
            });
          }
        } else {
          console.log('AuthProvider: No valid session found'); // Debug log
        }
      } catch (error) {
        console.error('Error initializing auth:', error);
        setIsAuthenticatedState(false);
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, []);

  // Login function
  const login = async (credentials: { email: string; password: string }) => {
    try {
      const result = await loginUser(credentials);
      
      if (result.success) {
        // Add a small delay to ensure session is properly stored
        await new Promise(resolve => setTimeout(resolve, 300));
        
        // Refresh auth state after successful login
        const authenticated = await checkIsAuthenticated();
        console.log('AuthProvider: Login - auth check result:', authenticated); // Debug log
        
        setIsAuthenticatedState(authenticated);
        
        if (authenticated) {
          const session = await getSession();
          console.log('AuthProvider: Login - session data:', session); // Debug log
          
          if (session?.user) {
            setUser({
              id: session.user.id,
              email: session.user.email,
              name: session.user.name,
            });
          }
        }
      }
      
      return result;
    } catch (err: any) {
      console.error('Login error:', err);
      return { success: false, error: err.message || 'Login failed' };
    }
  };

  const logout = async () => {
    try {
      await logoutUser();
      
      // Clear local state
      setUser(null);
      setIsAuthenticatedState(false);
      
      // Add a small delay to ensure session is cleared
      await new Promise(resolve => setTimeout(resolve, 200));
      
      router.replace('/login');
    } catch (error) {
      console.error('Logout error:', error);
      // Still clear local state even if logout fails
      setUser(null);
      setIsAuthenticatedState(false);
      
      // Add a small delay to ensure session is cleared
      await new Promise(resolve => setTimeout(resolve, 200));
      
      router.replace('/login');
    }
  };

  const refreshAuth = async () => {
    try {
      // Add a small delay to ensure session is properly established
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const authenticated = await checkIsAuthenticated();
      console.log('AuthProvider: Refresh auth - auth check result:', authenticated); // Debug log
      
      setIsAuthenticatedState(authenticated);
      
      if (authenticated) {
        const session = await getSession();
        console.log('AuthProvider: Refresh auth - session data:', session); // Debug log
        
        if (session?.user) {
          setUser({
            id: session.user.id,
            email: session.user.email,
            name: session.user.name,
          });
        }
      } else {
        console.log('AuthProvider: Refresh auth - no valid session'); // Debug log
        setUser(null);
      }
    } catch (error) {
      console.error('Refresh auth error:', error);
      setIsAuthenticatedState(false);
      setUser(null);
    }
  };

  // Route protection
  useEffect(() => {
    if (isLoading) return;

    const isPublic = PUBLIC_ROUTES.includes(pathname);

    if (!isAuthenticatedState && !isPublic) {
      console.log(`❌ No session - Protecting ${pathname} → /login`);
      router.replace('/login');
    } else if (isAuthenticatedState && (pathname === '/login' || pathname === '/register')) {
      console.log(`✅ Auth user on auth page → /dashboard`);
      router.replace('/dashboard');
    }
  }, [isAuthenticatedState, isLoading, pathname, router]);

  return (
    <AuthContext.Provider value={{ 
      user, 
      isAuthenticated: isAuthenticatedState, 
      isLoading, 
      login, 
      logout, 
      refreshAuth 
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}