'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { apiClient, Task } from '../../../../lib/api';
import { getCurrentUserId } from '../../../../lib/auth';
import TaskCard from '../../../../components/tasks/task-card';

export default function TaskDetailPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    const loadTask = async () => {
      try {
        const userId = await getCurrentUserId();
        setUserId(userId);

        if (userId && id) {
          // Use the user ID to get the task by its ID
          const taskDetails = await apiClient.getTask(parseInt(id), userId);
          setTask(taskDetails);
        } else {
          // If we don't have the user ID, redirect to login
          router.push('/login');
        }
      } catch (error) {
        console.error('Error loading task:', error);
        router.push('/tasks'); // Redirect to tasks list if error
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      loadTask();
    }
  }, [id, router]);

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

  if (!task) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-black">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-200 mb-2">Task Not Found</h2>
          <p className="text-gray-500 mb-4">The requested task could not be found</p>
          <button
            onClick={() => router.push('/tasks')}
            className="px-4 py-2 bg-gradient-to-r from-yellow-600 to-yellow-700 hover:from-yellow-500 hover:to-yellow-600 text-white rounded-lg font-medium transition-all"
          >
            Back to Tasks
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-gray-100 p-6">
      <div className="max-w-2xl mx-auto">
        <div className="mb-8">
          <button
            onClick={() => router.back()}
            className="flex items-center text-yellow-500 hover:text-yellow-400 mb-4"
          >
            ← Back to Tasks
          </button>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <TaskCard task={task} />
          </motion.div>
        </div>

        <div className="flex gap-4 mt-6">
          <button
            onClick={() => router.push(`/tasks/${task.id}/edit`)}
            className="px-4 py-2 bg-gradient-to-r from-gray-700 to-gray-800 hover:from-gray-600 hover:to-gray-700 text-white rounded-lg font-medium transition-all"
          >
            Edit Task
          </button>

          <button
            onClick={async () => {
              if (window.confirm('Are you sure you want to delete this task?')) {
                try {
                  await apiClient.deleteTask(task.id, task.user_id);
                  router.push('/tasks');
                } catch (error) {
                  console.error('Error deleting task:', error);
                }
              }
            }}
            className="px-4 py-2 bg-gradient-to-r from-red-700 to-red-800 hover:from-red-600 hover:to-red-700 text-white rounded-lg font-medium transition-all"
          >
            Delete Task
          </button>
        </div>
      </div>
    </div>
  );
}