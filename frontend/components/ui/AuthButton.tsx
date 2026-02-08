'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '@/components/auth/AuthProvider';

export default function AuthButton() {
  const { user, isAuthenticated, isLoading, logout } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);
  const [loggingOut, setLoggingOut] = useState(false);
  const router = useRouter();

 const handleSignOut = async () => {
  setLoggingOut(true);
  setShowDropdown(false);

  try {
    await logout();           // from context — already does redirect
  } catch (err) {
    console.error('Logout failed', err);
    router.push('/login');    // fallback
  } finally {
    setLoggingOut(false);
  }
};

  const handleSignIn = () => {
    router.push('/login');
  };

  if (isLoading) {
    return (
      <div className="flex items-center">
        <div className="w-8 h-8 border-2 border-yellow-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  // Show Sign In button when not authenticated
  if (!isAuthenticated || !user) {
    return (
      <motion.button
        onClick={handleSignIn}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="px-6 py-2 bg-gradient-to-r from-[#C9A24D] to-[#D4AF37] text-white rounded-lg font-medium shadow-lg hover:shadow-xl transition-all duration-200"
      >
        Sign In
      </motion.button>
    );
  }

  // Show user profile dropdown when authenticated
  return (
    <div className="relative">
      <motion.button
        onClick={() => setShowDropdown(!showDropdown)}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        disabled={loggingOut}
        className={`flex items-center space-x-3 px-4 py-2 bg-[#1A1A1F] border border-[#2A2A2F] rounded-lg text-[#F5F5F7] hover:bg-[#2A2A2F] transition-all duration-200 ${
          loggingOut ? 'opacity-50 cursor-not-allowed' : ''
        }`}
      >
        {/* User Avatar */}
        <div className="w-8 h-8 bg-gradient-to-r from-[#C9A24D] to-[#D4AF37] rounded-full flex items-center justify-center text-white font-semibold text-sm">
          {user.name?.charAt(0).toUpperCase() || user.email?.charAt(0).toUpperCase() || 'U'}
        </div>
        
        {/* User Info - Hidden on mobile */}
        <div className="hidden sm:block">
          <div className="text-sm font-medium text-left">
            {user.name || 'User'}
          </div>
          <div className="text-xs text-[#A0A0A5] text-left">
            {user.email}
          </div>
        </div>
        
        {/* Dropdown Arrow */}
        <svg 
          className={`w-4 h-4 transition-transform ${showDropdown ? 'rotate-180' : ''}`}
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </motion.button>

      {/* Dropdown Menu */}
      <AnimatePresence>
        {showDropdown && (
          <motion.div
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            transition={{ duration: 0.2 }}
            className="absolute right-0 mt-2 w-64 bg-[#1A1A1F] border border-[#2A2A2F] rounded-lg shadow-xl z-50 overflow-hidden"
          >
            {/* User Info Header */}
            <div className="px-4 py-3 border-b border-[#2A2A2F] bg-[#0F0F14]">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-[#C9A24D] to-[#D4AF37] rounded-full flex items-center justify-center text-white font-semibold">
                  {user.name?.charAt(0).toUpperCase() || user.email?.charAt(0).toUpperCase() || 'U'}
                </div>
                <div>
                  <div className="text-sm font-medium text-[#F5F5F7]">
                    {user.name || 'User'}
                  </div>
                  <div className="text-xs text-[#A0A0A5]">
                    {user.email}
                  </div>
                </div>
              </div>
            </div>
            
            {/* Navigation Links */}
            <div className="py-2">
              <button
                onClick={() => {
                  setShowDropdown(false);
                  router.push('/dashboard');
                }}
                className="w-full text-left px-4 py-2 text-sm text-[#F5F5F7] hover:bg-[#2A2A2F] transition-colors flex items-center space-x-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 5a2 2 0 012-2h4a2 2 0 012 2v6H8V5z" />
                </svg>
                <span>Dashboard</span>
              </button>
              
              <button
                onClick={() => {
                  setShowDropdown(false);
                  router.push('/todos');
                }}
                className="w-full text-left px-4 py-2 text-sm text-[#F5F5F7] hover:bg-[#2A2A2F] transition-colors flex items-center space-x-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
                <span>My Todos</span>
              </button>
              
              <button
                onClick={() => {
                  setShowDropdown(false);
                  router.push('/profile');
                }}
                className="w-full text-left px-4 py-2 text-sm text-[#F5F5F7] hover:bg-[#2A2A2F] transition-colors flex items-center space-x-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <span>Profile</span>
              </button>
            </div>
            
            {/* Logout Button */}
            <div className="border-t border-[#2A2A2F] py-2">
              <button
                onClick={handleSignOut}
                disabled={loggingOut}
                className="w-full text-left px-4 py-2 text-sm text-red-400 hover:bg-red-900/20 transition-colors disabled:opacity-50 flex items-center space-x-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                <span>{loggingOut ? 'Signing Out...' : 'Sign Out'}</span>
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
