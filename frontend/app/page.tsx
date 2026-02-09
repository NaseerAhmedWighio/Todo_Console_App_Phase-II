'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../components/auth/AuthProvider';

export default function HomePage() {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    // The AuthProvider will handle the routing, so we just need to wait
    // for the auth state to be determined and let the AuthProvider handle it
  }, [isAuthenticated, isLoading]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-black">
      <div className="text-center">
        <div className="w-16 h-16 border-4 border-yellow-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
        <p className="text-gray-400">Redirecting...</p>
      </div>
    </div>
  );
}