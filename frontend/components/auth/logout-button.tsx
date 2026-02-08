// 'use client';

// import { useRouter } from 'next/navigation';
// import { logoutUser } from '../../lib/auth';
// import { motion } from 'framer-motion';

// interface LogoutButtonProps {
//   className?: string;
// }

// export default function LogoutButton({ className }: LogoutButtonProps) {
//   const router = useRouter();

//   const handleLogout = async () => {
//     try {
//       const success = await logoutUser();
//       if (success) {
//         // Clear any local state if needed
//         router.push('/login');
//         router.refresh(); // Refresh to update session context
//       }
//     } catch (error) {
//       console.error('Logout error:', error);
//     }
//   };

//   return (
//     <motion.button
//       whileHover={{ scale: 1.03 }}
//       whileTap={{ scale: 0.98 }}
//       onClick={handleLogout}
//       className={`px-4 py-2 rounded-lg bg-gradient-to-r from-gray-700 to-gray-800 hover:from-gray-600 hover:to-gray-700 text-gray-200 font-medium border border-gray-600 transition-all ${className}`}
//     >
//       Logout
//     </motion.button>
//   );
// }










'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { logoutUser } from '@/lib/auth';
import { motion } from 'framer-motion';

export default function LogoutPage() {
  const router = useRouter();

  useEffect(() => {
    const performLogout = async () => {
      try {
        await logoutUser();
        // Small delay to show the logout message
        setTimeout(() => {
          router.replace('/login');
        }, 2000);
      } catch (error) {
        console.error('❌ Logout failed:', error);
        router.replace('/login');
      }
    };

    performLogout();
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#0B0B0E] to-black">
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="bg-[#1A1A1F] p-8 rounded-2xl shadow-xl border border-[#2A2A2F] text-center max-w-md w-full"
      >
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          className="w-12 h-12 border-4 border-yellow-500 border-t-transparent rounded-full mx-auto mb-6"
        />
        
        <h1 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-[#C9A24D] to-[#E6C066] mb-4">
          Signing Out
        </h1>
        
        <p className="text-[#A0A0A5] mb-6">
          Please wait while we securely sign you out...
        </p>
        
        <div className="text-sm text-[#6B6B75]">
          You will be redirected to the login page shortly.
        </div>
      </motion.div>
    </div>
  );
}
