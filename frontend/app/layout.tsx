'use client';

import './globals.css';
import { Inter } from 'next/font/google';
import { AuthProvider } from '@/components/auth/AuthProvider';
import UserProfile from '../components/common/user-profile';
import Link from 'next/link';

const inter = Inter({ subsets: ['latin'] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-gray-100">
            {/* Header with homepage button and user profile */}
            <header className="sticky top-0 z-10 bg-gray-900/80 backdrop-blur-sm border-b border-gray-800">
              <div className="container mx-auto px-4 py-3 flex justify-between items-center">
                <Link
                  href="/dashboard"
                  className="text-xl font-bold bg-gradient-to-r from-yellow-400 to-yellow-600 bg-clip-text text-transparent hover:opacity-80 transition-opacity"
                >
                  Todo App
                </Link>
                <UserProfile />
              </div>
            </header>

            <main>{children}</main>
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}
