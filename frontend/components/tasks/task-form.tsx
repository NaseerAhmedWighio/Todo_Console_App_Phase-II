'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { apiClient } from '../../lib/api';
import { getCurrentUserId } from '../../lib/auth';

interface TaskFormProps {
  task?: {
    id: number;
    title: string;
    description: string | null;
    completed: boolean;
  };
  onSuccess?: () => void;
  onCancel?: () => void;
}

export default function TaskForm({ task, onSuccess, onCancel }: TaskFormProps) {
  const router = useRouter();
  const [title, setTitle] = useState(task?.title || '');
  const [description, setDescription] = useState(task?.description || '');
  const [completed, setCompleted] = useState(task?.completed || false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const userId = await getCurrentUserId();
      if (!userId) {
        setError('User not authenticated');
        setLoading(false);
        return;
      }

      if (task) {
        // Update existing task
        await apiClient.updateTask(task.id, {
          title,
          description: description || undefined,
          completed,
        }, userId);
      } else {
        // Create new task
        await apiClient.createTask({
          title,
          description: description || undefined,
          completed,
        }, userId);
      }

      if (onSuccess) {
        onSuccess();
      } else {
        router.push('/tasks');
        router.refresh();
      }
    } catch (err) {
      setError(task ? 'Failed to update task. Please try again.' : 'Failed to create task. Please try again.');
      console.error(task ? 'Update task error:' : 'Create task error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.form
      onSubmit={handleSubmit}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-6"
    >
      {error && (
        <div className="p-3 bg-red-900/30 border border-red-700 rounded-lg text-red-300 text-sm">
          {error}
        </div>
      )}

      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-300 mb-1">
          Title *
        </label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent transition-all"
          placeholder="What needs to be done?"
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-300 mb-1">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={4}
          className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent transition-all resize-none"
          placeholder="Add more details..."
        />
      </div>

      <div className="flex items-center">
        <input
          id="completed"
          type="checkbox"
          checked={completed}
          onChange={(e) => setCompleted(e.target.checked)}
          className="h-4 w-4 text-yellow-500 focus:ring-yellow-500 border-gray-700 rounded bg-gray-800"
        />
        <label htmlFor="completed" className="ml-2 block text-sm text-gray-300">
          Mark as completed
        </label>
      </div>

      <div className="flex gap-4 pt-4">
        <button
          type="submit"
          disabled={loading}
          className={`px-6 py-3 rounded-lg font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 transition-all ${
            loading
              ? 'bg-gray-700 cursor-not-allowed'
              : 'bg-gradient-to-r from-yellow-600 to-yellow-700 hover:from-yellow-500 hover:to-yellow-600'
          }`}
        >
          {loading ? (task ? 'Updating...' : 'Creating...') : task ? 'Update Task' : 'Create Task'}
        </button>

        {onCancel ? (
          <button
            type="button"
            onClick={onCancel}
            className="px-6 py-3 bg-gradient-to-r from-gray-700 to-gray-800 hover:from-gray-600 hover:to-gray-700 text-white rounded-lg font-medium transition-all"
          >
            Cancel
          </button>
        ) : (
          <button
            type="button"
            onClick={() => router.back()}
            className="px-6 py-3 bg-gradient-to-r from-gray-700 to-gray-800 hover:from-gray-600 hover:to-gray-700 text-white rounded-lg font-medium transition-all"
          >
            Cancel
          </button>
        )}
      </div>
    </motion.form>
  );
}