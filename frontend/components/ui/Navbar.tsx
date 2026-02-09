'use client';

import Link from 'next/link';
import AuthButton from './AuthButton';
import { motion } from 'framer-motion';
import { useAuth } from '@/components/auth/AuthProvider';

export default function Navbar() {
  const { isAuthenticated, isLoading } = useAuth();

  return (
    <motion.nav 
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-[#0B0B0E]/90 backdrop-blur-lg border-b border-[#2A2A2F] sticky top-0 z-40"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href={isAuthenticated ? "/dashboard" : "/"} className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-[#C9A24D] to-[#D4AF37] rounded-lg flex items-center justify-center">
              <span className="text-white font-bold">T</span>
            </div>
            <span className="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-[#C9A24D] to-[#E6C066]">
              Todo App
            </span>
          </Link>

          {/* Navigation Links - Only show when authenticated */}
          {!isLoading && isAuthenticated && (
            <div className="hidden md:flex items-center space-x-6">
              <Link 
                href="/dashboard" 
                className="text-[#A0A0A5] hover:text-[#F5F5F7] transition-colors font-medium"
              >
                Dashboard
              </Link>
              <Link 
                href="/dashboard" 
                className="text-[#A0A0A5] hover:text-[#F5F5F7] transition-colors font-medium"
              >
                Todos
              </Link>
            </div>
          )}

          {/* Auth Button */}
          <AuthButton />
        </div>
      </div>
    </motion.nav>
  );
}
