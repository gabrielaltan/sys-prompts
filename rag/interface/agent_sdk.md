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

### Compact Mode (Floating Widget)

Shows a floating text field that expands to full chat on click.

```jsx
<Room
  mode="compact"
  ....
/>
```

**When to use it:** Use it for projects where the agent is a core element. Like FAQs agents or simple assistants. When in doubt, favor the use compact mode.


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

## Requirements

- **Agents must be public** for agent mode to work
- **Allowlist your domains** in Altan dashboard for better security

## Guest Info

Providing `guestInfo` enables chat history. 

```jsx
const user = useAuth();
...
guestInfo={{
  first_name: user?.first_name || null,    // Your user ID (enables conversation history)
  last_name: user?.last_name || null,    // User's first name
  email: user?.email || null,   // User's last name  
  external_id: user?.id || null   // User's email
}}
```

> **MUST RULE:** Any feature that relies on history **must** be protected by authentication. If you require chat history, enforce login so `guestInfo.external_id` reliably identifies the user.

> **MUST RULE:** `guestInfo` parameters must be fetch dynamically from the Database.

## Customization

### Agent Mode

| Property               | Type     | Default     | Description                              |
| ---------------------- | -------- | ----------- | ---------------------------------------- |
| `tabs`                 | boolean  | `true`      | Show/hide tab navigation                 |
| `conversation_history` | boolean  | `true`      | Show/hide conversation history           |
| `members`              | boolean  | `true`      | Show/hide members panel                  |
| `settings`             | boolean  | `true`      | Show/hide settings panel                 |
| `theme`                | string   | `undefined` | Theme mode: 'light', 'dark', or 'system' |
| `title`                | string   | `undefined` | Custom title                             |
| `description`          | string   | `undefined` | Custom description                       |
| `voice_enabled`        | boolean  | `true`      | Enable/disable voice functionality       |
| `suggestions`          | string[] | `[]`        | Predefined message suggestions           |


### Compact Mode (Widget Mode)

| Property           | Type    | Default         | Description                                              |
| ------------------ | ------- | --------------- | -------------------------------------------------------- |
| `primary_color`    | string  | `#007bff`       | Primary color (hex) for buttons and accents              |
| `background_color` | string  | `#ffffff`       | Background color (hex) for the widget                    |
| `background_blur`  | boolean | `true`          | Enable glassmorphism background blur effect              |
| `position`         | string  | `bottom-center` | Position: 'bottom-right', 'bottom-left', 'bottom-center' |
| `widget_width`     | number  | `350`           | Widget width in pixels                                   |
| `room_width`       | number  | `450`           | Room width in pixels when expanded                       |
| `room_height`      | number  | `600`           | Room height in pixels when expanded                      |
| `border_radius`    | number  | `16`            | Border radius in pixels for rounded corners              |


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