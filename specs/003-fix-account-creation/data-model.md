# Data Model: Fix Account Creation and Login Issues

## User Entity

### Fields
- `id` (string): Unique user identifier from Better Auth
- `email` (string): User's email address, unique, required
- `name` (string): User's display name, optional
- `hashed_password` (string): Bcrypt hashed password, required, max_length=255
- `created_at` (datetime): Account creation timestamp
- `updated_at` (datetime): Last update timestamp

### Validation Rules
- Email must be valid email format
- Email must be unique across users
- Hashed password must be properly formatted bcrypt hash
- Name, if provided, must be 1-255 characters

### Relationships
- One-to-many: User has many Tasks
- User ID is referenced in Task entities for data isolation

## Authentication Token

### Fields
- `access_token` (string): JWT token for authentication
- `token_type` (string): Type of token (typically "bearer")
- `expires_at` (datetime): Token expiration timestamp

### Validation Rules
- Access token must be valid JWT format
- Token must not be expired at time of validation
- Token must be signed with correct secret

## Error Response

### Fields
- `detail` (string): Human-readable error message
- `error_code` (string): Machine-readable error code
- `timestamp` (datetime): Time when error occurred

### Validation Rules
- Detail must be user-friendly and not expose technical details
- Error code must follow standard format
- Timestamp must be in ISO 8601 format

## State Transitions

### User Account States
- `pending_registration`: After form submission, before account creation
- `active`: Account created and verified
- `disabled`: Account temporarily or permanently disabled

### Transition Rules
- `pending_registration` → `active`: After successful registration and validation
- `active` → `disabled`: When account is deactivated
- `disabled` → `active`: When account is reactivated (admin action)

## Constraints

### Security Constraints
- Passwords must be hashed using bcrypt before storage
- JWT tokens must be validated using shared secret
- User IDs must match between JWT token and database lookup

### Data Integrity Constraints
- Email uniqueness enforced at database level
- User ID must exist in users table when creating related data
- Timestamps must be in UTC timezone

### Performance Constraints
- Password hashing operations should complete within 1 second
- JWT validation should complete within 100ms
- User lookup queries should use indexed fields