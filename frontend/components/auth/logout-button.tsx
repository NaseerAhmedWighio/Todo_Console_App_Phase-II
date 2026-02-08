'use client';

import { useRouter } from 'next/navigation';
import { logoutUser } from '../../lib/auth';
import { motion } from 'framer-motion';

interface LogoutButtonProps {
  className?: string;
}

export default function LogoutButton({ className }: LogoutButtonProps) {
  const router = useRouter();

  const handleLogout = async () => {
    try {
      const success = await logoutUser();
      if (success) {
        // Clear any local state if needed
        router.push('/login');
        router.refresh(); // Refresh to update session context
      }
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  return (
    <motion.button
      whileHover={{ scale: 1.03 }}
      whileTap={{ scale: 0.98 }}
      onClick={handleLogout}
      className={`flex items-center space-x-3 w-full px-4 py-3 rounded-lg text-sm font-medium text-gray-300 hover:bg-red-900/30 hover:text-white transition-all ${className}`}
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
        <polyline points="16 16 21 12 16 8"></polyline>
        <line x1="21" x2="9" y1="12" y2="12"></line>
      </svg>
      <span>Logout</span>
    </motion.button>
  );
}
