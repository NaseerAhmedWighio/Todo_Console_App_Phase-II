// import { NextRequest } from 'next/server';
// import { jwtDecode } from 'jwt-decode';

// // Forward Better Auth requests to the backend
// export async function POST(request: NextRequest) {
//   const { pathname } = new URL(request.url);
//   const path = pathname.replace('/api/auth', '');

//   // Get the backend API URL from environment variables
//   const BACKEND_URL = process.env.BACKEND_API_URL || 'http://localhost:8000';

//   // Extract the actual endpoint from the path
//   let backendEndpoint = '';
//   let requestBody = {};

//   // Map Better Auth paths to backend paths
//   if (path.includes('sign-in') || path.includes('login')) {
//     backendEndpoint = '/api/v1/auth/login';
//   } else if (path.includes('sign-up') || path.includes('register')) {
//     backendEndpoint = '/api/v1/auth/register';
//   } else if (path.includes('sign-out') || path.includes('logout')) {
//     backendEndpoint = '/api/v1/auth/logout';
//   } else if (path.includes('email')) {
//     // Handle email verification or other email endpoints
//     backendEndpoint = `/api/v1/auth${path}`;
//   } else {
//     // Handle other auth endpoints if needed
//     backendEndpoint = `/api/v1/auth${path}`;
//   }

//   try {
//     // Get the request body
//     const originalBody = await request.json();

//     // Map Better Auth request format to backend format
//     if (backendEndpoint === '/api/v1/auth/login') {
//       requestBody = {
//         email: originalBody.email,
//         password: originalBody.password
//       };
//     } else if (backendEndpoint === '/api/v1/auth/register') {
//       requestBody = {
//         email: originalBody.email,
//         password: originalBody.password,
//         name: originalBody.name || originalBody.username || ''
//       };
//     } else {
//       requestBody = originalBody;
//     }

//     // Forward the request to the backend
//     const response = await fetch(`${BACKEND_URL}${backendEndpoint}`, {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify(requestBody),
//     });

//     const responseData = await response.json();

//     // Create the response based on backend response
//     const status = response.status;

//     // For login/register, we need to format the response to match Better Auth expectations
//     if ((backendEndpoint === '/api/v1/auth/login' || backendEndpoint === '/api/v1/auth/register') && status === 200) {
//       // Decode the JWT to get user info
//       if (responseData.access_token) {
//         let userId = '';
//         let userEmail = originalBody.email;
//         let userName = originalBody.name || '';

//         // Decode the token to get user information
//         try {
//           const decodedToken: any = jwtDecode(responseData.access_token);
//           userId = decodedToken.sub || decodedToken.user_id || '';
//           userEmail = decodedToken.email || originalBody.email || '';
//           userName = decodedToken.name || originalBody.name || '';
//         } catch (decodeError) {
//           console.error('Token decode error:', decodeError);
//         }

//         // Format response to match Better Auth client expectations
//         return new Response(JSON.stringify({
//           user: {
//             id: userId,
//             email: userEmail,
//             name: userName,
//             image: null, // Backend doesn't provide image in token, set to null for now
//           },
//           token: responseData.access_token,
//           expires: responseData.expires_at || new Date(Date.now() + 30 * 60 * 1000).toISOString(), // 30 min default
//         }), {
//           status: status,
//           headers: {
//             'Content-Type': 'application/json',
//           },
//         });
//       } else {
//         // If no token in response, return the original response
//         return new Response(JSON.stringify(responseData), {
//           status: status,
//           headers: {
//             'Content-Type': 'application/json',
//           },
//         });
//       }
//     }

//     // For other responses, just forward the backend response
//     return new Response(JSON.stringify(responseData), {
//       status: status,
//       headers: {
//         'Content-Type': 'application/json',
//       },
//     });
//   } catch (error) {
//     console.error('Proxy error:', error);
//     return new Response(JSON.stringify({ error: 'Internal server error' }), {
//       status: 500,
//       headers: {
//         'Content-Type': 'application/json',
//       },
//     });
//   }
// }

// // Handle GET requests for session info
// export async function GET(request: NextRequest) {
//   const { pathname } = new URL(request.url);
//   const path = pathname.replace('/api/auth', '');

//   if (path.includes('session') || path.includes('me')) {
//     // Get the backend API URL from environment variables
//     const BACKEND_URL = process.env.BACKEND_API_URL || 'http://localhost:8000';

//     // Extract token from Authorization header
//     const authHeader = request.headers.get('authorization');
//     if (!authHeader || !authHeader.startsWith('Bearer ')) {
//       return new Response(JSON.stringify({ error: 'Unauthorized' }), {
//         status: 401,
//         headers: {
//           'Content-Type': 'application/json',
//         },
//       });
//     }

//     const token = authHeader.substring(7);

//     try {
//       // Forward the request to the backend
//       const response = await fetch(`${BACKEND_URL}/api/v1/auth/me`, {
//         method: 'GET',
//         headers: {
//           'Authorization': `Bearer ${token}`,
//           'Content-Type': 'application/json',
//         },
//       });

//       if (response.ok) {
//         const responseData = await response.json();

//         // Decode the token to get user information
//         let userId = '';
//         let userEmail = '';
//         let userName = '';

//         try {
//           const decodedToken: any = jwtDecode(token);
//           userId = decodedToken.sub || decodedToken.user_id || '';
//           userEmail = decodedToken.email || '';
//           userName = decodedToken.name || '';
//         } catch (decodeError) {
//           console.error('Token decode error:', decodeError);
//         }

//         // Use response data if available, otherwise use token data
//         const user = responseData || {
//           id: userId,
//           email: userEmail,
//           name: userName,
//           image: null
//         };

//         return new Response(JSON.stringify({
//           user: {
//             id: user.id || userId,
//             email: user.email || userEmail,
//             name: user.name || userName,
//             image: user.image || null,
//           },
//           token: token,
//           expires: new Date(Date.now() + 30 * 60 * 1000).toISOString(), // 30 min default
//         }), {
//           status: 200,
//           headers: {
//             'Content-Type': 'application/json',
//           },
//         });
//       } else {
//         return new Response(JSON.stringify({ error: 'Unauthorized' }), {
//           status: response.status,
//           headers: {
//             'Content-Type': 'application/json',
//           },
//         });
//       }
//     } catch (error) {
//       console.error('Session proxy error:', error);
//       return new Response(JSON.stringify({ error: 'Internal server error' }), {
//         status: 500,
//         headers: {
//           'Content-Type': 'application/json',
//         },
//       });
//     }
//   }

//   return new Response(JSON.stringify({ error: 'Not found' }), {
//     status: 404,
//     headers: {
//       'Content-Type': 'application/json',
//     },
//   });
// }





















import { NextRequest } from 'next/server';

// Simplified auth route handler - mainly for future Better Auth integration
export async function POST(request: NextRequest) {
  const { pathname } = new URL(request.url);
  
  console.log('🔄 Auth route called:', pathname);
  
  // For now, just return a 404 since we're using direct API calls
  return new Response(JSON.stringify({ 
    error: 'This endpoint is not implemented. Use direct API calls to /api/v1/auth/*' 
  }), {
    status: 404,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}

export async function GET(request: NextRequest) {
  const { pathname } = new URL(request.url);
  
  console.log('🔄 Auth GET route called:', pathname);
  
  return new Response(JSON.stringify({ 
    error: 'This endpoint is not implemented. Use direct API calls to /api/v1/auth/*' 
  }), {
    status: 404,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}
