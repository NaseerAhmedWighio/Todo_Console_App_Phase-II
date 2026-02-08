'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { FiHome, FiCheckSquare, FiPlusSquare, FiUser, FiLogOut } from 'react-icons/fi';
import LogoutButton from '../auth/logout-button';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  const pathname = usePathname();

  const navItems = [
    { href: '/dashboard', icon: <FiHome size={20} />, label: 'Dashboard' },
    { href: '/tasks', icon: <FiCheckSquare size={20} />, label: 'My Tasks' },
    { href: '/tasks/new', icon: <FiPlusSquare size={20} />, label: 'Create Task' },
    { href: '/profile', icon: <FiUser size={20} />, label: 'Profile' },
  ];

  return (
    <>
      {/* Backdrop for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={onClose}
        />
      )}

      <motion.aside
        initial={{ x: -280 }}
        animate={{ x: isOpen ? 0 : -280 }}
        transition={{ type: 'spring', damping: 25, stiffness: 200 }}
        className="fixed left-0 top-0 h-full w-64 bg-gradient-to-b from-gray-900 to-black z-50 shadow-xl border-r border-gray-800 md:relative md:translate-x-0"
      >
        <div className="p-6">
          <div className="flex items-center space-x-3 mb-10">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-yellow-500 to-yellow-600 flex items-center justify-center">
              <span className="text-white font-bold">T</span>
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-yellow-400 to-yellow-600 bg-clip-text text-transparent">
              TodoApp
            </span>
          </div>

          <nav>
            <ul className="space-y-1">
              {navItems.map((item) => (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className={`flex items-center space-x-3 px-4 py-3 rounded-lg text-sm font-medium transition-all ${
                      pathname.startsWith(item.href)
                        ? 'bg-yellow-500/10 text-yellow-500'
                        : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                    }`}
                    onClick={() => {
                      if (window.innerWidth < 768) onClose();
                    }}
                  >
                    <span>{item.icon}</span>
                    <span>{item.label}</span>
                  </Link>
                </li>
              ))}
            </ul>

            <div className="pt-8 mt-8 border-t border-gray-800">
              <LogoutButton className="flex items-center space-x-3 w-full px-4 py-3 rounded-lg text-sm font-medium text-gray-300 hover:bg-red-900/30 hover:text-white transition-all" />
            </div>
          </nav>
        </div>
      </motion.aside>
    </>
  );
}