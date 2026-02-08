'use client';

import { motion } from 'framer-motion';
import { apiClient } from '../../lib/api';
import { getCurrentUserId } from '../../lib/auth';
import { useState } from 'react';

interface TaskCheckboxProps {
  taskId: number;
  completed: boolean;
  onToggle?: (completed: boolean) => void;
}

export default function TaskCheckbox({ taskId, completed, onToggle }: TaskCheckboxProps) {
  const [isChecked, setIsChecked] = useState(completed);

  const handleToggle = async () => {
    try {
      const userId = await getCurrentUserId();
      if (!userId) return;

      // Optimistically update UI
      const newCompletedState = !isChecked;
      setIsChecked(newCompletedState);

      // Update on server
      await apiClient.toggleTaskCompletion(userId, taskId, newCompletedState);

      // Call callback if provided
      if (onToggle) {
        onToggle(newCompletedState);
      }
    } catch (error) {
      console.error('Error toggling task completion:', error);
      // Revert optimistic update on error
      setIsChecked(!isChecked);
    }
  };

  return (
    <motion.div
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={handleToggle}
      className={`relative h-6 w-6 rounded-full flex items-center justify-center cursor-pointer ${
        isChecked ? 'bg-gradient-to-br from-green-500 to-green-600' : 'bg-gray-700 border-2 border-gray-600'
      }`}
    >
      {isChecked && (
        <motion.svg
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="3"
          className="h-4 w-4 text-white"
        >
          <motion.path
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ duration: 0.2 }}
            d="M5 13l4 4L19 7"
          />
        </motion.svg>
      )}
    </motion.div>
  );
}