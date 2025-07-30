# Altan Frontend SDK

The altan SDK let's you add chat rooms with AI Agents directly into your product. 

## Installation

```bash
npm install @altanlabs/sdk
```

## Usage

### Agent Mode (1-on-1 Chat)

Chat with an AI agent. Automatically finds existing conversation or creates new one.

```jsx
import { Room } from '@altanlabs/sdk';

<Room
  mode="agent"
  accountId="account-id"
  agentId="agent-123"
  guestInfo={{ first_name: "John", external_id: "user-123" }}
/>
```

## SDK Parameters

| Prop        | Type                  | Required | Description                          |
| ----------- | --------------------- | -------- | ------------------------------------ |
| `mode`      | `"agent"` | ✅        | Chat with agent or join room         |
| `accountId` | string                | ✅        | Your Altan account ID                |
| `agentId`   | string                | ✅       | Agent ID (required for agent mode)   |
| `guestInfo` | object                | ❌        | User info (name, external_id, email) |


If any of these tables are missing you must prompt Altan Agent to orchestrate the creation of the required tables.

**`guestInfo`**:
* `external_id` (string): user’s ID in your Supabase `users` table (enables history).
* `first_name`, `last_name`, `email` (strings): user’s personal info.

> **MUST RULE:** All IDs and user data must be loaded dynamically from your database. Do **NOT** hard‑code any values.

### How to fetch each value

1. **accountId**

   * If not in memory: call Altan’s `get_project` method.
2. **agentId**

   * If missing: prompt the user (or upstream system) to supply the correct identifier.
3. **guestInfo.external\_id**

   * Retrieve from your Supabase `users` table’s primary key for the current user.
4. **guestInfo.first\_name, last\_name, email**

   * Collect from your own user store or prompt the user on first access.

> **Error handling:**
> If the `projects` or `users` tables don’t exist in your database schema, prompt the Altan Agent to orchestrate their creation before rendering the chat

## Requirements

- **Agents must be public** for agent mode to work
- **Allowlist your domains** in Altan dashboard for better security

## Guest Info

```jsx
guestInfo={{
  external_id: 'user-123',    // Your user ID (enables conversation history)
  first_name: 'John',         // User's first name
  last_name: 'Doe',          // User's last name  
  email: 'john@example.com'   // User's email
}}
```

## Complete Example

```jsx
import React from 'react';
import { Room } from '@altanlabs/sdk';

function App() {
  return (
    <div style={{ height: '600px' }}>
      <Room
        mode="agent"
        accountId="altan-account-id"
        agentId="agent-123"
        guestInfo={{
          first_name: 'Jane',
          last_name: 'Doe',
          email: 'jane@example.com',
          external_id: 'user-456'
        }}
        onConversationReady={(room) => console.log('Chat ready!')}
        onAuthSuccess={(guest) => console.log('User authenticated:', guest.id)}
      />
    </div>
  );
}
```