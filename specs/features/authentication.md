# Authentication Specification

## Feature Overview
Secure JWT-based authentication system using Better Auth for frontend and custom JWT middleware for backend, ensuring proper user isolation and authorization.

## Functional Requirements

### User Registration
- **Page**: `/auth/signup`
- **Functionality**: Allow new users to create accounts
- **Validation**: Email format, password strength
- **Integration**: With Better Auth registration flow
- **Post-registration**: Redirect to dashboard/home

### User Login
- **Page**: `/auth/signin`
- **Functionality**: Allow existing users to authenticate
- **Validation**: Credentials verification
- **Integration**: With Better Auth login flow
- **Post-login**: Redirect to dashboard/home with JWT token

### User Logout
- **Functionality**: Securely end user session
- **Token Management**: Remove JWT from storage
- **Redirect**: To login page after logout
- **Security**: Clear all authentication state

### JWT Token Management
- **Storage**: Secure storage of JWT in browser (httpOnly cookies or secure localStorage)
- **Expiry**: Handle token expiration gracefully
- **Refresh**: Implement refresh mechanism if needed
- **Security**: Tokens must not be exposed to XSS attacks

### Protected Routes
- **Middleware**: Verify JWT before rendering protected pages
- **Redirect**: Unauthenticated users to login page
- **Error Handling**: Display appropriate messages for auth failures

## API Authentication Requirements

### JWT Middleware (Backend)
- **Location**: Applied to all `/api/*` routes
- **Functionality**: Extract and validate JWT from Authorization header
- **Header Format**: `Authorization: Bearer <jwt_token>`
- **Validation**: Verify signature using BETTER_AUTH_SECRET
- **User Extraction**: Extract user_id from token payload
- **Error Response**: 401 for invalid/missing tokens

### User Context Injection
- **Dependency**: Inject authenticated user context into request handlers
- **Available Data**: user_id, email, name (as available from Better Auth)
- **Access Control**: Pass user context to data access layer

### Authorization Enforcement
- **Route Parameters**: Verify {user_id} in URL matches authenticated user
- **Data Filtering**: Only return data belonging to authenticated user
- **Operation Validation**: Prevent cross-user data manipulation
- **Error Response**: 403 for authorization failures

## Security Requirements

### Token Security
- **Secret**: Shared BETTER_AUTH_SECRET between frontend and backend
- **Algorithm**: Use strong algorithm (HS256/RS256)
- **Expiration**: Reasonable token lifetime (1-7 days)
- **Storage**: Secure storage to prevent XSS/CSRF attacks

### Session Management
- **Concurrent Sessions**: Support multiple device sessions
- **Session Invalidation**: Ability to invalidate sessions
- **Logout Propagation**: Clear all related session state

### Attack Prevention
- **Rate Limiting**: Prevent brute force attempts
- **CSRF Protection**: Additional protection where needed
- **XSS Prevention**: Secure token storage and handling
- **Replay Attack Prevention**: Proper token invalidation

## Integration Points

### Frontend-Better Auth Integration
- **Configuration**: JWT plugin enabled in Better Auth
- **Client Setup**: Initialize Better Auth client with JWT support
- **API Calls**: Automatically attach JWT to API requests
- **State Management**: Sync auth state with application state

### Frontend-Backend API Integration
- **Header Injection**: Add Authorization header to all API calls
- **Error Handling**: Handle 401/403 responses appropriately
- **Token Refresh**: Implement token refresh logic
- **UI Updates**: Reflect auth status in UI components

## Error Scenarios

### Authentication Errors
- **Invalid Credentials**: Display appropriate error message
- **Network Issues**: Handle API connectivity problems
- **Token Expiry**: Redirect to login or refresh token
- **Account Disabled**: Show account-specific messages

### Authorization Errors
- **Insufficient Permissions**: Deny access to protected resources
- **Expired Session**: Redirect to login page
- **Token Tampering**: Treat as unauthorized access
- **Missing Token**: Redirect to authentication flow

## Configuration

### Environment Variables
- **BETTER_AUTH_SECRET**: Shared secret for JWT signing/verification
- **AUTH_API_BASE_URL**: Base URL for auth API calls
- **TOKEN_EXPIRY_BUFFER**: Buffer time before token expiry handling

### Better Auth Configuration
- **Providers**: Configure social login providers if needed
- **Database**: Configure user storage
- **JWT Settings**: Configure token generation parameters
- **Callbacks**: Configure post-authentication redirects