'use client';

import { useRouter } from 'next/navigation';
import { useAuth } from '../auth/AuthProvider';

export default function UserProfile() {
  const { user, isAuthenticated, isLoading, logout } = useAuth();
  const router = useRouter();

  if (isLoading) {
    return (
      <div className="flex items-center space-x-2">
        <div className="w-8 h-8 rounded-full bg-gray-700 animate-pulse"></div>
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return (
      <button
        onClick={() => router.push('/login')}
        className="px-4 py-2 bg-gradient-to-r from-yellow-500 to-yellow-600 text-white rounded-lg font-medium hover:opacity-90 transition-opacity"
      >
        Sign In
      </button>
    );
  }

  return (
    <div className="flex items-center space-x-3">
      <div className="flex items-center space-x-2">
        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-yellow-500 to-yellow-600 flex items-center justify-center">
          <span className="text-white text-xs font-medium">
            {user.name ? user.name.charAt(0).toUpperCase() : user.email.charAt(0).toUpperCase()}
          </span>
        </div>
        <span className="hidden md:inline text-gray-300 text-sm max-w-[120px] truncate" title={user.email}>
          {user.name || user.email.split('@')[0]}
        </span>
      </div>
      
      <button
        onClick={logout}
        className="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-300 text-xs rounded-lg transition-colors"
      >
        Logout
      </button>
    </div>
  );
}