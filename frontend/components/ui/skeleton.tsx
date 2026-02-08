import { motion } from 'framer-motion';

interface SkeletonProps {
  className?: string;
  width?: string | number;
  height?: string | number;
  borderRadius?: string;
}

export default function Skeleton({
  className = '',
  width = '100%',
  height = '1rem',
  borderRadius = '0.5rem'
}: SkeletonProps) {
  return (
    <motion.div
      className={`bg-gradient-to-r from-gray-800/50 to-gray-900/50 ${className}`}
      style={{ width, height, borderRadius }}
      animate={{
        backgroundPosition: ['0%', '100%', '0%'],
      }}
      transition={{
        duration: 1.5,
        repeat: Infinity,
        ease: 'easeInOut',
      }}
    />
  );
}

interface SkeletonCardProps {
  count?: number;
}

export function SkeletonCard({ count = 1 }: SkeletonCardProps) {
  return (
    <>
      {Array.from({ length: count }).map((_, index) => (
        <div key={index} className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-700">
          <Skeleton height="1.5rem" width="60%" className="mb-4" />
          <Skeleton height="1rem" width="100%" className="mb-2" />
          <Skeleton height="1rem" width="80%" className="mb-4" />
          <div className="flex justify-between">
            <Skeleton height="0.8rem" width="30%" />
            <Skeleton height="2rem" width="6rem" borderRadius="0.5rem" />
          </div>
        </div>
      ))}
    </>
  );
}