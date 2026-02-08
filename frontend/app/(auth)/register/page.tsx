'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { registerUser } from '../lib/auth';

export default function RegisterPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Basic validation
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      setLoading(false);
      return;
    }

    try {
      const result = await registerUser({ email, password, name });
      if (result.success) {
        router.push('/dashboard');
        router.refresh(); // Refresh to update session context
      } else {
        setError(result.error || 'Registration failed. Please try again.');
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred during registration');
      console.error('Registration error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#0B0B0E] to-black">
      <div className="bg-[#1A1A1F] p-8 rounded-2xl shadow-xl w-full max-w-md border border-[#2A2A2F]">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-[#C9A24D] to-[#E6C066]">
            Todo App
          </h1>
          <p className="text-[#A0A0A5] mt-2">Create your account</p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-[#2A1E20]/50 border border-[#EF4444]/50 rounded-lg text-[#FCA5A5] text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="space-y-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-[#D0D0D5] mb-1">
                Full Name
              </label>
              <input
                id="name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                className="w-full px-4 py-3 bg-[#0F0F14] border border-[#2A2A2F] rounded-lg text-[#F5F5F7] placeholder-[#6B6B75] focus:outline-none focus:ring-2 focus:ring-[#C9A24D] focus:border-transparent transition-all hover:shadow-lg hover:shadow-[#C9A24D]/10"
                placeholder="John Doe"
              />
            </div>

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
                className="w-full px-4 py-3 bg-[#0F0F14] border border-[#2A2A2F] rounded-lg text-[#F5F5F7] placeholder-[#6B6B75] focus:outline-none focus:ring-2 focus:ring-[#C9A24D] focus:border-transparent transition-all hover:shadow-lg hover:shadow-[#C9A24D]/10"
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
                className="w-full px-4 py-3 bg-[#0F0F14] border border-[#2A2A2F] rounded-lg text-[#F5F5F7] placeholder-[#6B6B75] focus:outline-none focus:ring-2 focus:ring-[#C9A24D] focus:border-transparent transition-all hover:shadow-lg hover:shadow-[#C9A24D]/10"
                placeholder="••••••••"
              />
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-[#D0D0D5] mb-1">
                Confirm Password
              </label>
              <input
                id="confirmPassword"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                className="w-full px-4 py-3 bg-[#0F0F14] border border-[#2A2A2F] rounded-lg text-[#F5F5F7] placeholder-[#6B6B75] focus:outline-none focus:ring-2 focus:ring-[#C9A24D] focus:border-transparent transition-all hover:shadow-lg hover:shadow-[#C9A24D]/10"
                placeholder="••••••••"
              />
            </div>

            <div className="flex items-center">
              <input
                id="terms"
                name="terms"
                type="checkbox"
                required
                className="h-4 w-4 text-[#C9A24D] focus:ring-[#C9A24D] border-[#2A2A2F] rounded bg-[#0F0F14]"
              />
              <label htmlFor="terms" className="ml-2 block text-sm text-[#A0A0A5]">
                I agree to the <a href="#" className="text-[#C9A24D] hover:text-[#E6C066] transition-colors">Terms and Conditions</a>
              </label>
            </div>

            <button
              type="submit"
              disabled={loading}
              className={`w-full py-3 px-4 rounded-lg font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#C9A24D] transition-all duration-300 hover:scale-105 ${
                loading
                  ? 'bg-[#2A2A2F] cursor-not-allowed'
                  : 'bg-gradient-to-r from-[#C9A24D] to-[#D4AF37] hover:from-[#E6C066] hover:to-[#F0D170] shadow-lg shadow-[#C9A24D]/20'
              }`}
            >
              {loading ? 'Creating account...' : 'Create account'}
            </button>
          </div>
        </form>

        <div className="mt-6 text-center text-sm text-[#A0A0A5]">
          Already have an account?{' '}
          <Link href="/login" className="font-medium text-[#C9A24D] hover:text-[#E6C066] transition-colors">
            Sign in
          </Link>
        </div>
      </div>
    </div>
  );
}