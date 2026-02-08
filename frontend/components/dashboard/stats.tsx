'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { apiClient } from '../../lib/api';
import { getCurrentUserId } from '../../lib/auth';

interface StatsData {
  total: number;
  completed: number;
  pending: number;
}

export default function DashboardStats() {
  const [stats, setStats] = useState<StatsData>({ total: 0, completed: 0, pending: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadStats = async () => {
      try {
        const userId = await getCurrentUserId();
        if (!userId) return;

        const tasks = await apiClient.getTasks(userId);

        // Calculate stats
        const completed = tasks.filter(t => t.completed).length;
        const total = tasks.length;

        setStats({
          total,
          completed,
          pending: total - completed
        });
      } catch (error) {
        console.error('Error loading stats:', error);
      } finally {
        setLoading(false);
      }
    };

    loadStats();
  }, []);

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[1, 2, 3].map((item) => (
          <div
            key={item}
            className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-700"
          >
            <div className="animate-pulse">
              <div className="h-4 bg-gray-700 rounded w-1/3 mb-2"></div>
              <div className="h-8 bg-gray-700 rounded w-1/2"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="grid grid-cols-1 md:grid-cols-3 gap-6"
    >
      <motion.div
        whileHover={{ scale: 1.02 }}
        className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-700"
      >
        <h3 className="text-gray-400 text-sm font-medium mb-2">Total Tasks</h3>
        <p className="text-3xl font-bold text-white">{stats.total}</p>
      </motion.div>

      <motion.div
        whileHover={{ scale: 1.02 }}
        className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-700"
      >
        <h3 className="text-gray-400 text-sm font-medium mb-2">Completed</h3>
        <p className="text-3xl font-bold text-green-400">{stats.completed}</p>
      </motion.div>

      <motion.div
        whileHover={{ scale: 1.02 }}
        className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-700"
      >
        <h3 className="text-gray-400 text-sm font-medium mb-2">Pending</h3>
        <p className="text-3xl font-bold text-yellow-400">{stats.pending}</p>
      </motion.div>
    </motion.div>
  );
}