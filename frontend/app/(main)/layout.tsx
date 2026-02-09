// 'use client';

// import { useEffect, useState } from 'react';
// import { useRouter } from 'next/navigation';
// import { isAuthenticated } from '@/lib/auth';
// import { motion } from 'framer-motion';

// export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
//   const [isLoading, setIsLoading] = useState(true);
//   const [isAuthorized, setIsAuthorized] = useState(false);
//   const router = useRouter();

//   useEffect(() => {
//     let isMounted = true; // Prevent state updates after unmount

//     const checkAuth = async () => {
//       try {
//         // Add a small delay to ensure session is properly established
//         await new Promise(resolve => setTimeout(resolve, 200));
        
//         const ok = await isAuthenticated();

//         if (isMounted) {
//           if (!ok) {
//             // Clear any stale session data
//             if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
//               localStorage.removeItem('user_session');
//             }
//             router.replace('/login');
//           } else {
//             setIsAuthorized(true);
//           }
//           setIsLoading(false);
//         }
//       } catch (error) {
//         console.error('❌ Auth check failed:', error);
//         if (isMounted) {
//           router.replace('/login');
//           setIsLoading(false);
//         }
//       }
//     };

//     checkAuth();

//     // Cleanup function
//     return () => {
//       isMounted = false;
//     };
//   }, [router]);

//   if (isLoading) {
//     return (
//       <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-black">
//         <motion.div
//           animate={{ rotate: 360 }}
//           transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
//           className="w-12 h-12 border-4 border-yellow-500 border-t-transparent rounded-full"
//         />
//       </div>
//     );
//   }

//   if (!isAuthorized) return null;

//   return (
//     <motion.div
//       initial={{ opacity: 0, y: 20 }}
//       animate={{ opacity: 1, y: 0 }}
//       transition={{ duration: 0.5 }}
//       className="min-h-screen"
//     >
//       {children}
//     </motion.div>
//   );
// }






// layout.tsx   (ProtectedLayout)

// 'use client';

// import { useEffect } from 'react'; // ← no need for useState anymore in many cases
// import { useRouter } from 'next/navigation';
// import { authClient } from '@/lib/auth'; // ← import the client, not a function
// import { motion } from 'framer-motion';

// export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
//   const router = useRouter();
//   const { data: session, isPending, error } = authClient.useSession();

//   useEffect(() => {
//     if (!isPending) {
//       if (!session?.user) {
//         // Optional: clear any stale localStorage if you're mixing approaches
//         localStorage.removeItem('user_session');
//         router.replace('/login');
//       }
//       // else → user is authenticated → render children
//     }
//   }, [isPending, session, router]);

//   if (isPending || error) {
//     return (
//       <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-black">
//         <motion.div
//           animate={{ rotate: 360 }}
//           transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
//           className="w-12 h-12 border-4 border-yellow-500 border-t-transparent rounded-full"
//         />
//       </div>
//     );
//   }

//   if (!session?.user) {
//     return null; // or a redirect component, but useEffect already handles it
//   }

//   return (
//     <motion.div
//       initial={{ opacity: 0, y: 20 }}
//       animate={{ opacity: 1, y: 0 }}
//       transition={{ duration: 0.5 }}
//       className="min-h-screen"
//     >
//       {children}
//     </motion.div>
//   );
// }



'use client';

import { useAuth } from "@/components/auth/AuthProvider";
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  // Since AuthProvider already handles routing, we just need to render children
  // or a loading state. No additional redirects needed here.
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-black">
        <div className="w-12 h-12 border-4 border-yellow-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  // If user is not authenticated, the AuthProvider will handle redirect
  // So we just return the children here
  return <div className="min-h-screen">{children}</div>;
}