'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { usePathname } from 'next/navigation';
import { getSession } from '../../lib/auth';
import LogoutButton from '../auth/logout-button';

interface User {
  id: string;
  email: string;
  name?: string;
}

export default function Header() {
  const pathname = usePathname();
  const [user, setUser] = useState<User | null>(null);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  useEffect(() => {
    const loadUser = async () => {
      try {
        const session = await getSession();
        if (session) {
          setUser({
            id: session.user.id,
            email: session.user.email,
            name: session.user.name
          });
        }
      } catch (error) {
        console.error('Error loading user:', error);
      }
    };

    loadUser();
  }, []);

  // Close menu when navigating
  useEffect(() => {
    setIsMenuOpen(false);
  }, [pathname]);

  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="sticky top-0 z-50 bg-gray-900/80 backdrop-blur-md border-b border-gray-800"
    >
      <div className="max-w-6xl mx-auto px-6 py-4">
        <div className="flex justify-between items-center">
          <Link href="/dashboard" className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-yellow-500 to-yellow-600 flex items-center justify-center">
              <span className="text-white font-bold text-sm">T</span>
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-yellow-400 to-yellow-600 bg-clip-text text-transparent">
              TodoApp
            </span>
          </Link>

          <nav className="hidden md:flex items-center space-x-8">
            <Link
              href="/dashboard"
              className={`text-sm font-medium transition-colors ${
                pathname.startsWith('/dashboard')
                  ? 'text-yellow-500'
                  : 'text-gray-300 hover:text-white'
              }`}
            >
              Dashboard
            </Link>
            <Link
              href="/tasks"
              className={`text-sm font-medium transition-colors ${
                pathname.startsWith('/tasks') && !pathname.includes('/new')
                  ? 'text-yellow-500'
                  : 'text-gray-300 hover:text-white'
              }`}
            >
              Tasks
            </Link>
            <Link
              href="/tasks/new"
              className={`text-sm font-medium transition-colors ${
                pathname.includes('/tasks/new')
                  ? 'text-yellow-500'
                  : 'text-gray-300 hover:text-white'
              }`}
            >
              New Task
            </Link>
            <Link
              href="/profile"
              className={`text-sm font-medium transition-colors ${
                pathname.startsWith('/profile')
                  ? 'text-yellow-500'
                  : 'text-gray-300 hover:text-white'
              }`}
            >
              Profile
            </Link>
          </nav>

          {user && (
            <div className="flex items-center space-x-4">
              <div className="relative">
                <button
                  onClick={() => setIsMenuOpen(!isMenuOpen)}
                  className="flex items-center space-x-2 focus:outline-none"
                >
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-yellow-500 to-yellow-600 flex items-center justify-center text-white font-bold">
                    {user.name ? user.name.charAt(0).toUpperCase() : user.email.charAt(0).toUpperCase()}
                  </div>
                  <span className="hidden sm:block text-sm text-gray-300 max-w-[100px] truncate">
                    {user.name || user.email.split('@')[0]}
                  </span>
                </button>

                {isMenuOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="absolute right-0 mt-2 w-48 bg-gray-800 rounded-lg shadow-lg py-2 border border-gray-700 z-50"
                  >
                    <Link
                      href="/profile"
                      className="block px-4 py-2 text-sm text-gray-300 hover:bg-gray-700 hover:text-white"
                      onClick={() => setIsMenuOpen(false)}
                    >
                      Profile
                    </Link>
                    <div className="border-t border-gray-700 my-1"></div>
                    <div className="px-4 py-2 text-xs text-gray-500">
                      {user.email}
                    </div>
                    <div className="border-t border-gray-700 my-1"></div>
                    <LogoutButton  />
                  </motion.div>
                )}
              </div>
            </div>
          )}

          {/* Mobile menu button */}
          <button
            className="md:hidden text-gray-300 focus:outline-none"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
        </div>

        {/* Mobile menu */}
        {isMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden mt-4 pb-4"
          >
            <nav className="flex flex-col space-y-2">
              <Link
                href="/dashboard"
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  pathname.startsWith('/dashboard')
                    ? 'bg-yellow-500/10 text-yellow-500'
                    : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                }`}
              >
                Dashboard
              </Link>
              <Link
                href="/tasks"
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  pathname.startsWith('/tasks') && !pathname.includes('/new')
                    ? 'bg-yellow-500/10 text-yellow-500'
                    : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                }`}
              >
                Tasks
              </Link>
              <Link
                href="/tasks/new"
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  pathname.includes('/tasks/new')
                    ? 'bg-yellow-500/10 text-yellow-500'
                    : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                }`}
              >
                New Task
              </Link>
              <Link
                href="/profile"
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  pathname.startsWith('/profile')
                    ? 'bg-yellow-500/10 text-yellow-500'
                    : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                }`}
              >
                Profile
              </Link>
            </nav>
          </motion.div>
        )}
      </div>
    </motion.header>
  );
}