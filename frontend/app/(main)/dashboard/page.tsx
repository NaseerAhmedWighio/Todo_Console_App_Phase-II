'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { apiClient, Task } from '../../../lib/api';
import { useAuth } from '../../../components/auth/AuthProvider';
import { useRouter } from 'next/navigation';

interface Stats {
  total: number;
  completed: number;
  pending: number;
}

export default function DashboardPage() {
  const [stats, setStats] = useState<Stats>({ total: 0, completed: 0, pending: 0 });
  const [recentTasks, setRecentTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // If user is not authenticated, redirect to login
    if (!authLoading && !isAuthenticated) {
      router.replace('/login');
    }
  }, [authLoading, isAuthenticated, router]);

  useEffect(() => {
    const loadDashboardData = async () => {
      if (!user?.id) return; // Wait for user to be available
      
      try {
        const tasks = await apiClient.getTasks(user.id);

        // Calculate stats
        const completed = tasks.filter(t => t.completed).length;
        const total = tasks.length;

        setStats({
          total,
          completed,
          pending: total - completed
        });

        // Get recent tasks (last 5)
        const sortedTasks = [...tasks].sort((a, b) =>
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        ).slice(0, 5);

        setRecentTasks(sortedTasks);
      } catch (error) {
        console.error('Error loading dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    if (user?.id) {
      loadDashboardData();
    }
  }, [user?.id]);

  if (authLoading || loading) {
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-gray-100 p-6">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold bg-gradient-to-r from-yellow-400 to-yellow-600 bg-clip-text text-transparent">
            Welcome Back
          </h1>
          <p className="text-gray-400 mt-2">Here&#39;s what&#39;s happening with your tasks today.</p>
        </motion.div>

        {/* Stats Grid */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8"
        >
          <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-700">
            <h3 className="text-gray-400 text-sm font-medium mb-2">Total Tasks</h3>
            <p className="text-3xl font-bold text-white">{stats.total}</p>
          </div>

          <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-700">
            <h3 className="text-gray-400 text-sm font-medium mb-2">Completed</h3>
            <p className="text-3xl font-bold text-green-400">{stats.completed}</p>
          </div>

          <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-700">
            <h3 className="text-gray-400 text-sm font-medium mb-2">Pending</h3>
            <p className="text-3xl font-bold text-yellow-400">{stats.pending}</p>
          </div>
        </motion.div>

        {/* Recent Tasks */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mb-8"
        >
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold text-white">Recent Tasks</h2>
            <Link
              href="/tasks"
              className="text-yellow-500 hover:text-yellow-400 font-medium"
            >
              View All →
            </Link>
          </div>

          {recentTasks.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {recentTasks.map((task, index) => (
                <motion.div
                  key={task.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                >
                  <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-4 border border-gray-700">
                    <h3 className={`font-semibold ${
                      task.completed ? 'line-through text-gray-500' : 'text-white'
                    }`}>
                      {task.title}
                    </h3>
                    <p className="text-gray-400 text-sm mt-1 truncate">
                      {task.description || 'No description'}
                    </p>
                    <div className="mt-2 text-xs text-gray-500">
                      {new Date(task.created_at).toLocaleDateString()}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl border border-gray-700">
              <p className="text-gray-400">No recent tasks. Create your first task to get started!</p>
              <Link
                href="/tasks/new"
                className="mt-4 inline-block px-4 py-2 bg-gradient-to-r from-yellow-600 to-yellow-700 hover:from-yellow-500 hover:to-yellow-600 text-white rounded-lg font-medium transition-all"
              >
                Create Task
              </Link>
            </div>
          )}
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <h2 className="text-2xl font-bold text-white mb-4">Quick Actions</h2>
          <div className="flex flex-wrap gap-4">
            <Link
              href="/tasks/new"
              className="px-6 py-3 bg-gradient-to-r from-yellow-600 to-yellow-700 hover:from-yellow-500 hover:to-yellow-600 text-white rounded-lg font-medium transition-all"
            >
              + Create Task
            </Link>
            <Link
              href="/tasks"
              className="px-6 py-3 bg-gradient-to-r from-gray-700 to-gray-800 hover:from-gray-600 hover:to-gray-700 text-white rounded-lg font-medium transition-all"
            >
              View All Tasks
            </Link>
          </div>
        </motion.div>
      </div>
    </div>
  );
}