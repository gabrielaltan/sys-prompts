# Authentication
**ALWAYS use altan-auth library**

```typescript
// ALWAYS use altan-auth library
import { AuthProvider } from 'altan-auth'
import { supabase } from './supabaseClient'

// Wrap application
<AuthProvider supabase={supabase}>
  <AuthContainer />
</AuthProvider>

// Inside AuthContainer
<AuthWrapper 
  defaultTab="signin" 
  onSignInSuccess={handleSignInSuccess}
  onSignUpSuccess={handleSignUpSuccess}
  onError={handleError}
  showSocialAuth={true}  // default: true
/>
```

## Hooks
**`useAuth()`**
Returns the authentication context:
- `service`: Instance of AuthService with authentication methods
- `session`: Current session data (null if not authenticated) session returns this format:

```json
{
  "type": "object",
  "properties": {
    "access_token": { "type": "string" },
    "refresh_token": { "type": "string" },
    "expires_in": { "type": "integer" },
    "expires_at": { "type": "integer" },
    "token_type": { "type": "string" },
    "user": {
      "type": "object",
      "properties": {
        "id": { "type": "string", "format": "uuid" },
        "email": { "type": "string", "format": "email" },
        "role": { "type": "string" },
        "app_metadata": { "type": "object" },
        "user_metadata": {
          "type": "object",
          "properties": {
            "avatar": { "type": ["string", "null"] },
            "name": { "type": "string" },
            "surname": { "type": "string" }
          },
          "required": ["name", "surname"]
        }
      },
      "required": ["id", "email", "role", "app_metadata", "user_metadata"]
    }
  },
  "required": ["access_token", "refresh_token", "expires_in", "expires_at", "token_type", "user"]
}
```

- `loading`: Boolean indicating if auth state is being loaded

## AuthService Methods
- `signUp(email, password, name, surname)`: Register a new user
- `signIn(email, password)`: Sign in with email and password
- `signInWithOAuth(provider)`: Sign in with an OAuth provider
- `signOut()`: Sign out the current user
- `getSession()`: Get the current session
- `getUser()`: Get the current user
- `onAuthStateChange(callback)`: Listen for auth state changes
