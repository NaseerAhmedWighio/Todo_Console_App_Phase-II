'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import TaskCheckbox from './task-checkbox';

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface TaskCardProps {
  task: Task;
}

export default function TaskCard({ task }: TaskCardProps) {
  return (
    <motion.div
      whileHover={{ y: -5 }}
      className={`bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-5 border ${
        task.completed ? 'border-green-500/30' : 'border-gray-700'
      } shadow-lg transition-all duration-300`}
    >
      <div className="flex items-start gap-3">
        <TaskCheckbox
          taskId={task.id}
          completed={task.completed}
          onToggle={() => {}}
        />

        <div className="flex-1">
          <h3
            className={`text-lg font-semibold ${
              task.completed ? 'line-through text-gray-500' : 'text-white'
            }`}
          >
            {task.title}
          </h3>

          {task.description && (
            <p className={`mt-2 text-gray-400 ${task.completed ? 'line-through' : ''}`}>
              {task.description}
            </p>
          )}

          <div className="mt-4 flex justify-between items-center">
            <span className="text-xs text-gray-500">
              {new Date(task.created_at).toLocaleDateString()}
            </span>

            <Link
              href={`/tasks/${task.id}`}
              className="text-yellow-500 hover:text-yellow-400 text-sm font-medium"
            >
              View Details
            </Link>
          </div>
        </div>
      </div>
    </motion.div>
  );
}