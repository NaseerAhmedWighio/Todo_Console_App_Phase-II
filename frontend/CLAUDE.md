# Frontend Development Guidelines

## Technology Stack
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth (JWT enabled)
- Framer Motion (for animations)

## Project Structure
```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   └── forgot-password/page.tsx
│   ├── (main)/
│   │   ├── dashboard/page.tsx
│   │   ├── tasks/
│   │   │   ├── page.tsx
│   │   │   ├── [id]/page.tsx
│   │   │   └── new/page.tsx
│   │   └── profile/page.tsx
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ui/
│   ├── auth/
│   ├── tasks/
│   └── layout/
├── lib/
│   ├── auth.ts
│   ├── api.ts
│   └── utils.ts
├── public/
└── types/
```

## Development Guidelines

### Styling
- Use Tailwind CSS exclusively for styling
- Follow the luxury design system:
  - Primary: Deep Charcoal (#0B0B0E)
  - Secondary: Soft Graphite (#1A1A1F)
  - Accent: Royal Gold (#C9A24D)
  - Success: Emerald Green
  - Danger: Soft Crimson
  - Text: Off-white (#F5F5F7)

### Animations
- Implement all micro-interactions with Framer Motion
- Use consistent animation durations (300ms standard)
- Apply hover effects: smooth scale (scale-105), soft glow
- Add task completion animations and loading skeletons

### Authentication
- Integrate Better Auth with JWT plugin enabled
- Store tokens securely using httpOnly cookies or secure localStorage
- Attach JWT to all API requests automatically
- Handle token expiration gracefully

### API Integration
- Create centralized API client in lib/api.ts
- Handle authentication headers automatically
- Implement proper error handling and user feedback
- Use TypeScript interfaces for API responses

### Component Architecture
- Build reusable, testable components
- Follow Atomic Design principles
- Use proper TypeScript interfaces and props validation
- Implement proper error boundaries

### Testing
- Write comprehensive unit tests for components
- Implement integration tests for API interactions
- Use Jest and React Testing Library
- Maintain 80%+ test coverage

### Performance
- Optimize bundle size with code splitting
- Implement proper image optimization
- Use lazy loading for non-critical components
- Minimize re-renders with React.memo and useMemo