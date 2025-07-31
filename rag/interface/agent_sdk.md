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

| Prop        | Type      | Required | Description                          |
| ----------- | --------- | -------- | ------------------------------------ |
| `mode`      | `"agent"` | ✅        | Chat with agent or join room         |
| `accountId` | string    | ✅        | Your Altan account ID                |
| `agentId`   | string    | ✅        | Agent ID (required for agent mode)   |
| `guestInfo` | object    | ❌        | User info (name, external_id, email) |


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

You control whether history is enabled by supplying `guestInfo`. You must follow these rules exactly when populating it:

### Rules You Must Follow

1. **`external_id` is the primary key for user history.**

   * You must supply `guestInfo.external_id` only if it matches an existing user ID in your `users` table.
   * If that ID does not exist or you cannot reliably resolve the current session to a user, set it to `null`.
   * This value is how you load and recover per-user conversation history; it must come from the database.

2. **Never hardcode or fabricate data.**

   * Do not hardcode `first_name`, `last_name`, `email`, or `external_id` (except `null`).
   * Do not generate `external_id` dynamically (e.g., `guest_${Date.now()}`) or make up any user fields.
   * Only pull values from your authenticated user record in the database. If unavailable, use `null`.

3. **Respect your logging/history mechanism.**

   * If your project has a logging or history system enabled, you must fetch all `guestInfo` values directly from the canonical user store (`users` table).
   * If there is no logging/history mechanism or you cannot securely identify the user, you must leave those fields as `null`.

4. **Enforce authentication when you rely on history.**

   * Any feature that uses conversation history must require that the user is authenticated so `guestInfo.external_id` is valid and consistent.

5. **Validate before use.**

   * Before passing `external_id` into the SDK, verify it exists in the `users` table. If the required `users` table is missing, trigger your orchestration logic to create it. Do not proceed assuming history will work without that validation.

### When to Populate `guestInfo`

* Populate it with real values only when:

  * You have a valid authenticated session tied to a user record, and
  * The required user data exists in the `users` table (logging/history is available).

* Otherwise, set each field to `null`. Do not guess or backfill with placeholder data.

### Correct Usage Example

```jsx
const user = await fetchCurrentUserFromDB(); // must come from your users table

<Room
  mode="agent"
  accountId={resolveAccountId()}    // loaded dynamically
  agentId={resolveAgentId()}        // loaded dynamically
  guestInfo={{
    first_name: user?.first_name || null,
    last_name: user?.last_name || null,
    email: user?.email || null,
    external_id: user?.id || null, // MUST be an existing user ID
  }}
/>
```

### Incorrect / Forbidden Examples

```jsx
guestInfo={{
  first_name: "Guest",                    // ❌ hardcoded
  external_id: `guest_${Date.now()}`,     // ❌ invented
  email: "someone@example.com",           // ❌ hardcoded
  last_name: "User"                       // ❌ hardcoded
}}
```

```jsx
guestInfo={{
  external_id: "nonexistent-id",          // ❌ not verified against users table
}}
```

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