'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';

interface FilterControlsProps {
  onFilterChange: (filter: 'all' | 'completed' | 'pending') => void;
}

export default function FilterControls({ onFilterChange }: FilterControlsProps) {
  const [selectedFilter, setSelectedFilter] = useState<'all' | 'completed' | 'pending'>('all');

  const handleFilterClick = (filter: 'all' | 'completed' | 'pending') => {
    setSelectedFilter(filter);
    onFilterChange(filter);
  };

  return (
    <div className="flex space-x-2 bg-gray-800/50 border border-gray-700 rounded-lg p-1">
      <FilterButton
        isActive={selectedFilter === 'all'}
        onClick={() => handleFilterClick('all')}
      >
        All
      </FilterButton>
      <FilterButton
        isActive={selectedFilter === 'completed'}
        onClick={() => handleFilterClick('completed')}
      >
        Completed
      </FilterButton>
      <FilterButton
        isActive={selectedFilter === 'pending'}
        onClick={() => handleFilterClick('pending')}
      >
        Pending
      </FilterButton>
    </div>
  );
}

interface FilterButtonProps {
  isActive: boolean;
  onClick: () => void;
  children: React.ReactNode;
}

function FilterButton({ isActive, onClick, children }: FilterButtonProps) {
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
        isActive
          ? 'bg-gradient-to-r from-yellow-600 to-yellow-700 text-white shadow-md'
          : 'text-gray-400 hover:text-white'
      }`}
    >
      {children}
    </motion.button>
  );
}