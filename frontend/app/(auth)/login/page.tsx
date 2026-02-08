'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { loginUser } from '../../../lib/auth';

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (loading) return;

    setLoading(true);
    setError(null);

    const result = await loginUser({ email, password });

    if (!result.success) {
      setError(result.error || 'Invalid email or password');
      setLoading(false);
      return;
    }

    // Wait a bit to ensure session is properly established before redirecting
    await new Promise(resolve => setTimeout(resolve, 500));
    // ✅ Session is already stored by loginUser
    router.replace('/dashboard');
    // Refresh to ensure the UI updates with the new session
    router.refresh();
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#0B0B0E] to-black">
      <div className="bg-[#1A1A1F] p-8 rounded-2xl shadow-xl w-full max-w-md border border-[#2A2A2F]">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-[#C9A24D] to-[#E6C066]">
            Todo App
          </h1>
          <p className="text-[#A0A0A5] mt-2">Sign in to your account</p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-[#2A1E20]/50 border border-[#EF4444]/50 rounded-lg text-[#FCA5A5] text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-[#D0D0D5] mb-1">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
              className="w-full px-4 py-3 bg-[#0F0F14] border border-[#2A2A2F] rounded-lg text-[#F5F5F7] placeholder-[#6B6B75] focus:outline-none focus:ring-2 focus:ring-[#C9A24D]"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-[#D0D0D5] mb-1">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="current-password"
              className="w-full px-4 py-3 bg-[#0F0F14] border border-[#2A2A2F] rounded-lg text-[#F5F5F7] placeholder-[#6B6B75] focus:outline-none focus:ring-2 focus:ring-[#C9A24D]"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full py-3 rounded-lg font-medium text-white transition-all ${
              loading
                ? 'bg-[#2A2A2F] cursor-not-allowed'
                : 'bg-gradient-to-r from-[#C9A24D] to-[#D4AF37] hover:scale-105 shadow-lg shadow-[#C9A24D]/20'
            }`}
          >
            {loading ? 'Signing in...' : 'Sign in'}
          </button>
        </form>

        <div className="mt-6 text-center text-sm text-[#A0A0A5]">
          Don&apos;t have an account?{' '}
          <Link
            href="/register"
            className="font-medium text-[#C9A24D] hover:text-[#E6C066] transition-colors"
          >
            Sign up
          </Link>
        </div>
      </div>
    </div>
  );
}