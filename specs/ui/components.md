# UI Components Specification

## Design System
### Color Palette
- **Primary**: Deep Charcoal / Jet Black (#0B0B0E)
- **Secondary**: Soft Graphite / Dark Gray (#1A1A1F)
- **Accent**: Royal Gold / Champagne (#C9A24D)
- **Success**: Emerald Green (#10B981)
- **Danger**: Soft Crimson (#EF4444)
- **Text**: Off-white (#F5F5F7)

### Typography
- **Headings**: Large, bold, modern sans-serif
- **Body**: Clean, readable font with appropriate hierarchy
- **Scale**: Consistent spacing and sizing ratios

## Core Components

### Layout Components

#### AppLayout
- **Purpose**: Main application wrapper with consistent structure
- **Features**: Responsive navigation, proper spacing, consistent padding
- **Props**: children, title, showNav (boolean)
- **Variants**: Authenticated vs unauthenticated layouts

#### Header
- **Purpose**: Top navigation bar with branding and user controls
- **Elements**: Logo, navigation links, user profile dropdown
- **Responsive**: Collapsible menu on mobile
- **Styling**: Fixed position with backdrop blur effect

#### Sidebar
- **Purpose**: Navigation sidebar for authenticated users
- **Elements**: Dashboard link, tasks link, settings, logout
- **Behavior**: Collapsible on smaller screens
- **Styling**: Matches secondary color (#1A1A1F)

#### Footer
- **Purpose**: Informational footer with legal links
- **Elements**: Copyright, privacy policy, terms of service
- **Position**: Sticky at bottom when content is short

### Authentication Components

#### AuthForm
- **Purpose**: Base form component for auth flows
- **Features**: Form validation, error display, loading states
- **Props**: onSubmit, children, title, subtitle
- **Variants**: Login, signup, forgot password

#### LoginForm
- **Purpose**: User login form with credentials
- **Fields**: Email, password
- **Features**: Social login options, "Remember me"
- **Validation**: Real-time field validation

#### SignupForm
- **Purpose**: User registration form
- **Fields**: Name, email, password, confirm password
- **Features**: Password strength indicator
- **Validation**: Email format, password requirements

#### UserProfile
- **Purpose**: User profile display and management
- **Elements**: Avatar, name, email, settings links
- **Actions**: Edit profile, change password, logout

### Task Management Components

#### TaskCard
- **Purpose**: Individual task display with action controls
- **Elements**: Title, description, completion checkbox, actions
- **Animation**: Hover effects, completion transition
- **States**: Completed (strikethrough), pending
- **Actions**: Edit, delete, toggle completion

#### TaskList
- **Purpose**: Container for multiple task cards
- **Features**: Loading skeleton, empty state, infinite scroll
- **Filtering**: Show all/completed/pending tasks
- **Sorting**: By creation date, alphabetical

#### TaskForm
- **Purpose**: Form for creating/editing tasks
- **Fields**: Title (required), description (optional), completion status
- **Features**: Character counters, validation feedback
- **Actions**: Submit, cancel, reset

#### TaskActionBar
- **Purpose**: Action bar for bulk task operations
- **Elements**: Select all, bulk delete, bulk complete
- **Visibility**: Appears when tasks are selected

### Interactive Components

#### Button
- **Variants**: Primary, secondary, accent, danger, ghost
- **Sizes**: Small, medium, large
- **States**: Enabled, disabled, loading
- **Animations**: Scale-105 on hover, soft glow, color transition (300ms)

#### InputField
- **Types**: Text, textarea, email, password
- **Features**: Label, placeholder, error state, helper text
- **Validation**: Real-time validation feedback

#### Checkbox
- **Purpose**: Task completion toggle
- **Animation**: Smooth transition, ripple effect
- **States**: Checked, unchecked, indeterminate

#### ToggleSwitch
- **Purpose**: Binary state toggles
- **Animation**: Smooth slide transition
- **Accessibility**: Proper ARIA labels

#### Modal
- **Purpose**: Overlay dialogs for important actions
- **Features**: Click-outside to close, ESC key, focus trap
- **Animations**: Fade-in/slide-up entrance

#### Toast
- **Purpose**: Temporary notifications
- **Types**: Success, error, warning, info
- **Behavior**: Auto-dismiss, stackable

### Navigation Components

#### LinkButton
- **Purpose**: Link styled as a button
- **Styling**: Inherits button styles but navigates
- **Accessibility**: Proper semantic markup

#### Breadcrumb
- **Purpose**: Navigation trail showing current location
- **Elements**: Hierarchical links with separators
- **Behavior**: Updates with page navigation

#### Pagination
- **Purpose**: Navigate through paginated content
- **Elements**: Previous/next buttons, page numbers
- **Features**: Current page highlighting

### Loading Components

#### SkeletonLoader
- **Purpose**: Placeholder content during loading
- **Variants**: Text, card, avatar shapes
- **Animation**: Subtle shimmer effect

#### Spinner
- **Purpose**: Indicate ongoing operations
- **Variants**: Small (inline), large (centered)
- **Animation**: Smooth rotation

## Animation Specifications

### Micro-interactions
- **Checkbox**: Smooth scale (scale-105) with color transition
- **Task completion**: Strike-through animation with opacity change
- **Button hover**: Soft glow or shadow, color transition (300ms)
- **Card hover**: Lift effect with border highlight

### Page Transitions
- **Navigation**: Fade/slide transitions between pages
- **Modal**: Open/close animation with backdrop fade
- **Loading**: Skeleton loader with shimmer effect

### Scroll Animations
- **Task cards**: Fade-in on scroll with stagger
- **Sections**: Reveal animations using Framer Motion
- **Sticky header**: Blur background effect on scroll

## Responsive Design

### Breakpoints
- **Mobile**: Up to 640px
- **Tablet**: 641px to 1024px
- **Desktop**: 1025px and above

### Responsive Behaviors
- **Navigation**: Collapses to hamburger menu on mobile
- **Forms**: Stacked layout on mobile, side-by-side on desktop
- **Grids**: Single column on mobile, multiple columns on desktop
- **Touch targets**: Minimum 44px touch targets on mobile

## Accessibility
- **Keyboard navigation**: Full keyboard operability
- **Screen readers**: Proper ARIA labels and roles
- **Focus indicators**: Visible focus states
- **Color contrast**: WCAG AA compliance
- **Alternative text**: Descriptive alt text for images

## Component States
- **Default**: Normal appearance
- **Hover**: Enhanced appearance for interactive elements
- **Active**: Pressed/down state
- **Focus**: Keyboard navigation state
- **Disabled**: Non-interactive state
- **Loading**: Operation in progress state
- **Error**: Invalid state with error indication
- **Success**: Valid state with success indication

## Styling Approach
- **Framework**: Tailwind CSS utility classes
- **Customization**: Custom properties for theme values
- **Consistency**: Shared utility classes for common patterns
- **Performance**: Purge unused styles in production