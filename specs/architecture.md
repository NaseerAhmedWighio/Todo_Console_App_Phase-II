# Todo App Phase II Architecture

## System Architecture
The application follows a modern full-stack architecture with clear separation between frontend and backend components:

```
┌─────────────────┐    HTTP/HTTPS     ┌──────────────────┐
│   Frontend      │ ────────────────► │    Backend       │
│   (Next.js)     │                   │   (FastAPI)      │
│                 │ ◄───────────────  │                  │
│  - React UI     │   REST API        │  - Business Logic│
│  - Auth Client  │                   │  - Auth Service  │
│  - Animations   │                   │  - DB Access     │
└─────────────────┘                   └──────────────────┘
                                             │
                                      ┌──────────────────┐
                                      │   Database       │
                                      │  (Neon PG)       │
                                      └──────────────────┘
```

## Technology Stack
### Frontend
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth (JWT enabled)
- Framer Motion (animations)

### Backend
- FastAPI (Python)
- SQLModel ORM
- Neon Serverless PostgreSQL

## Data Flow
1. User authenticates via Better Auth
2. JWT token issued and stored securely
3. Frontend attaches token to API requests
4. Backend validates JWT and extracts user_id
5. Backend filters data by authenticated user
6. Database operations performed with proper isolation

## Security Architecture
- JWT-based authentication
- Token validation middleware
- User data isolation at API level
- Secure token storage and transmission
- Proper error handling without information leakage

## Deployment Architecture
- Separate deployments for frontend and backend
- Environment-specific configurations
- Database connection pooling
- CDN for static assets (future consideration)