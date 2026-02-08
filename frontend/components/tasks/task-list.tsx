'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { apiClient } from '../../../lib/api';
import { getCurrentUserId } from '../../../lib/auth';
import TaskCard from './task-card';
import SearchBar from './search-bar';
import FilterControls from './filter-controls';

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface TaskListProps {
  initialFilter?: 'all' | 'completed' | 'pending';
}

export default function TaskList({ initialFilter = 'all' }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [currentFilter, setCurrentFilter] = useState<'all' | 'completed' | 'pending'>(initialFilter);

  useEffect(() => {
    const loadTasks = async () => {
      try {
        // Add a small delay to ensure session is established
        await new Promise(resolve => setTimeout(resolve, 100));
        
        const userId = await getCurrentUserId();
        if (!userId) {
          setError('User not authenticated');
          return;
        }

        // Fetch tasks with filter and search parameters
        const allTasks = await apiClient.getTasks(userId);
        setTasks(allTasks);
        applyFiltersAndSearch(allTasks, currentFilter, searchQuery);
      } catch (err) {
        setError('Failed to load tasks. Please try again.');
        console.error('Load tasks error:', err);
      } finally {
        setLoading(false);
      }
    };

    loadTasks();
  }, []);

  const applyFiltersAndSearch = (tasksToFilter: Task[], filter: 'all' | 'completed' | 'pending', search: string) => {
    let result = [...tasksToFilter];

    // Apply filter
    if (filter === 'completed') {
      result = result.filter(task => task.completed);
    } else if (filter === 'pending') {
      result = result.filter(task => !task.completed);
    }

    // Apply search
    if (search) {
      const lowerSearch = search.toLowerCase();
      result = result.filter(task =>
        task.title.toLowerCase().includes(lowerSearch) ||
        (task.description && task.description.toLowerCase().includes(lowerSearch))
      );
    }

    setFilteredTasks(result);
  };

  const handleFilterChange = (filter: 'all' | 'completed' | 'pending') => {
    setCurrentFilter(filter);
    applyFiltersAndSearch(tasks, filter, searchQuery);
  };

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    applyFiltersAndSearch(tasks, currentFilter, query);
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row gap-4">
          <SearchBar onSearch={handleSearch} />
          <FilterControls onFilterChange={handleFilterChange} />
        </div>

        <div className="flex justify-center items-center py-12">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
            className="w-8 h-8 border-4 border-yellow-500 border-t-transparent rounded-full"
          />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row gap-4">
          <SearchBar onSearch={handleSearch} />
          <FilterControls onFilterChange={handleFilterChange} />
        </div>

        <div className="text-center py-12">
          <p className="text-red-500">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row gap-4">
        <SearchBar onSearch={handleSearch} />
        <FilterControls onFilterChange={handleFilterChange} />
      </div>

      {filteredTasks.length === 0 ? (
        <div className="text-center py-12">
          <h3 className="text-xl text-gray-400 mb-2">
            {searchQuery
              ? 'No tasks match your search'
              : currentFilter === 'completed' ? 'No completed tasks' :
                currentFilter === 'pending' ? 'No pending tasks' : 'No tasks yet'}
          </h3>
          <p className="text-gray-500">
            {searchQuery
              ? 'Try adjusting your search query'
              : currentFilter === 'completed' ? 'Complete some tasks to see them here' :
                currentFilter === 'pending' ? 'All tasks are completed!' : 'Create your first task to get started'}
          </p>
        </div>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
        >
          {filteredTasks.map((task, index) => (
            <motion.div
              key={task.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
            >
              <TaskCard task={task} />
            </motion.div>
          ))}
        </motion.div>
      )}
    </div>
  );
}