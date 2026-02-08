'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { getSession } from '../../../lib/auth';

interface UserData {
  id: string;
  email: string;
  name?: string;
}

export default function ProfilePage() {
  const [userData, setUserData] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const session = await getSession();
        if (session) {
          setUserData({
            id: session.user.id,
            email: session.user.email,
            name: session.user.name || undefined
          });
        }
      } catch (error) {
        console.error('Error loading profile:', error);
      } finally {
        setLoading(false);
      }
    };

    loadProfile();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-black">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          className="w-12 h-12 border-4 border-yellow-500 border-t-transparent rounded-full"
        />
      </div>
    );
  }

  if (!userData) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-black">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-200 mb-2">Access Denied</h2>
          <p className="text-gray-500">Please sign in to access your profile</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-gray-100 p-6">
      <div className="max-w-2xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="text-3xl font-bold bg-gradient-to-r from-yellow-400 to-yellow-600 bg-clip-text text-transparent mb-8">
            My Profile
          </h1>

          <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-700">
            <div className="flex items-center gap-6 mb-8">
              <div className="w-16 h-16 rounded-full bg-gradient-to-br from-yellow-500 to-yellow-600 flex items-center justify-center text-white text-xl font-bold">
                {userData.name ? userData.name.charAt(0).toUpperCase() : userData.email.charAt(0).toUpperCase()}
              </div>
              <div>
                <h2 className="text-xl font-semibold text-white">
                  {userData.name || userData.email.split('@')[0]}
                </h2>
                <p className="text-gray-400">{userData.email}</p>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Email</label>
                <div className="bg-gray-700/50 border border-gray-600 rounded-lg px-4 py-3 text-white">
                  {userData.email}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">User ID</label>
                <div className="bg-gray-700/50 border border-gray-600 rounded-lg px-4 py-3 text-gray-300 text-sm font-mono">
                  {userData.id}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Account Status</label>
                <div className="bg-gray-700/50 border border-gray-600 rounded-lg px-4 py-3 text-green-400">
                  Active
                </div>
              </div>
            </div>
          </div>

          <div className="mt-8">
            <h3 className="text-lg font-semibold text-white mb-4">Account Settings</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <button className="px-4 py-3 bg-gradient-to-r from-gray-700 to-gray-800 hover:from-gray-600 hover:to-gray-700 text-white rounded-lg font-medium transition-all">
                Change Password
              </button>
              <button className="px-4 py-3 bg-gradient-to-r from-gray-700 to-gray-800 hover:from-gray-600 hover:to-gray-700 text-white rounded-lg font-medium transition-all">
                Update Profile
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}