# Altan AI SDK

Ultra-simple AI chat integration for any website.

## 🚀 One-Line Integration (No Coding Required!)

Perfect for **Wix, Shopify, WordPress, or any website**. Just add this single line:

```html
<script
  src="https://cdn.altan.ai/sdk/altan-widget.js"
  data-account-id="your-account-id"
  data-agent-id="your-agent-id"
></script>
```

**That's it!** A beautiful floating chat appears at the bottom of your page with:
- ⚡ **Instant loading** - Pre-loads in background
- 📱 **Mobile responsive** - Adapts to all screen sizes  
- 🎨 **Smooth animations** - GPU-accelerated transforms
- 🔒 **Secure** - Generates unique visitor IDs

### Widget Configuration

Customize the widget with data attributes:

```html
<script 
  src="https://cdn.altan.ai/sdk/altan-widget.js"
  data-account-id="your-account-id"
  data-agent-id="your-agent-id"
  data-placeholder="Ask me anything..."
  data-guest-name="Website Visitor"
  data-guest-email="user@example.com"
  data-theme="dark"
  data-tabs="false"
  data-voice-enabled="true"
  data-suggestions='["Hello","How can I help?","Support"]'
></script>
```

#### Core Widget Data Attributes

| Attribute          | Required | Description                                     |
| ------------------ | -------- | ----------------------------------------------- |
| `data-account-id`  | ✅        | Your Altan account ID                           |
| `data-agent-id`    | ✅*       | Agent ID for 1-on-1 chat                        |
| `data-room-id`     | ✅*       | Room ID for group chat                          |
| `data-mode`        | ❌        | Widget mode: 'compact' (default)                |
| `data-placeholder` | ❌        | Text field placeholder                          |
| `data-guest-name`  | ❌        | Visitor's display name                          |
| `data-guest-email` | ❌        | Visitor's email                                 |
| `data-external-id` | ❌        | Custom user ID (auto-generated if not provided) |

*Either `data-agent-id` or `data-room-id` is required

#### Room Personalization Data Attributes

| Attribute                   | Type       | Default | Description                         |
| --------------------------- | ---------- | ------- | ----------------------------------- |
| `data-tabs`                 | boolean    | `true`  | Show/hide tab navigation            |
| `data-conversation-history` | boolean    | `true`  | Show/hide conversation history      |
| `data-members`              | boolean    | `true`  | Show/hide members panel             |
| `data-settings`             | boolean    | `true`  | Show/hide settings panel            |
| `data-theme`                | string     | -       | Theme: 'light', 'dark', or 'system' |
| `data-title`                | string     | -       | Custom room title                   |
| `data-description`          | string     | -       | Custom room description             |
| `data-voice-enabled`        | boolean    | `true`  | Enable/disable voice functionality  |
| `data-suggestions`          | JSON array | `[]`    | Predefined message suggestions      |

#### Widget Styling Data Attributes

| Attribute               | Type    | Default         | Description                                              |
| ----------------------- | ------- | --------------- | -------------------------------------------------------- |
| `data-primary-color`    | string  | `#007bff`       | Primary color (hex) for buttons and accents              |
| `data-background-color` | string  | `#ffffff`       | Background color (hex) for the widget                    |
| `data-background-blur`  | boolean | `true`          | Enable glassmorphism background blur effect              |
| `data-position`         | string  | `bottom-center` | Position: 'bottom-right', 'bottom-left', 'bottom-center' |
| `data-width`            | number  | `350`           | Widget width in pixels                                   |
| `data-room-width`       | number  | `450`           | Room width in pixels when expanded                       |
| `data-room-height`      | number  | `600`           | Room height in pixels when expanded                      |
| `data-border-radius`    | number  | `16`            | Border radius in pixels for rounded corners              |

#### Advanced Configuration

```html
<script 
  src="https://cdn.altan.ai/sdk/altan-widget.js"
  data-account-id="your-account-id"
  data-agent-id="your-agent-id"
  data-api-base-url="https://api.altan.ai/platform/guest"
  data-auth-base-url="https://api.altan.ai/auth/login/guest"
  data-room-base-url="https://altan.ai/r"
></script>
```

#### Complete Example

```html
<script 
  src="https://cdn.altan.ai/sdk/altan-widget.js"
  data-account-id="afd0ea2c-b44a-475b-b433-096eece24085"
  data-agent-id="support-agent-123"
  data-placeholder="Need help? Ask me anything!"
  data-guest-name="John Doe"
  data-guest-email="john@example.com"
  data-external-id="user-123"
  data-theme="dark"
  data-tabs="false"
  data-members="false"
  data-voice-enabled="true"
  data-title="Customer Support"
  data-description="We're here to help!"
  data-suggestions='["I need help with my order","Technical support","Billing question"]'
  data-primary-color="#6366f1"
  data-background-color="#ffffff"
  data-background-blur="true"
  data-position="bottom-right"
  data-width="400"
  data-room-width="550"
  data-room-height="700"
  data-border-radius="20"
></script>
```

---

## 🔧 JavaScript API

The widget exposes a JavaScript API for advanced integration and control.

### Global Instance

After loading the script, the widget is available as `window.AltanWidget`:

```javascript
// Check if widget is loaded
if (window.AltanWidget) {
  console.log('Altan Widget is ready!');
}
```

### Manual Initialization

Initialize the widget programmatically instead of using data attributes:

```javascript
window.AltanWidget.init({
  accountId: 'your-account-id',
  agentId: 'your-agent-id',
  mode: 'compact',
  placeholder: 'How can I help you?',
  guestName: 'John Doe',
  guestEmail: 'john@example.com',
  theme: 'dark',
  voice_enabled: true,
  primary_color: '#6366f1'
});
```

### Widget Control Methods

```javascript
// Initialize widget manually
window.AltanWidget.init(config);

// Destroy the widget and clean up
window.AltanWidget.destroy();

// Generate a unique external ID
const externalId = window.AltanWidget.generateExternalId();
```

### Event Listeners

Listen to widget events for integration with your application:

```javascript
// Authentication successful
document.addEventListener('altan-auth-success', (event) => {
  const { guest, tokens } = event.detail;
  console.log('User authenticated:', guest);
  // Store user info, track analytics, etc.
});

// Conversation ready (agent mode)
document.addEventListener('altan-conversation-ready', (event) => {
  const { room } = event.detail;
  console.log('Chat conversation ready:', room);
});

// Room joined (room mode)
document.addEventListener('altan-room-joined', (event) => {
  const { guest, tokens } = event.detail;
  console.log('User joined room:', guest);
});

// Error occurred
document.addEventListener('altan-error', (event) => {
  const { error } = event.detail;
  console.error('Widget error:', error);
  // Handle error, show fallback, etc.
});
```

### User Identity Management

The widget automatically manages user identity:

```javascript
// Widget automatically generates and stores external IDs in localStorage
// Key: 'altan-external-id'
// Format: 'web_timestamp_randomstring'

// Override with your own user ID
window.AltanWidget.init({
  accountId: 'your-account-id',
  agentId: 'your-agent-id',
  externalId: 'your-user-id' // Your custom user identifier
});

// Access the generated/stored external ID
const storedId = localStorage.getItem('altan-external-id');
```

### Complete JavaScript Example

```html
<!DOCTYPE html>
<html>
<head>
  <title>Custom Widget Integration</title>
</head>
<body>
  <button id="start-chat">Start Chat</button>
  <button id="destroy-chat">Close Chat</button>

  <script src="https://cdn.altan.ai/sdk/altan-widget.js"></script>
  <script>
    // Wait for widget to load
    document.addEventListener('DOMContentLoaded', () => {
      
      // Set up event listeners
      document.addEventListener('altan-auth-success', (event) => {
        console.log('User authenticated:', event.detail.guest);
        document.getElementById('start-chat').textContent = 'Chat Active';
      });

      document.addEventListener('altan-conversation-ready', (event) => {
        console.log('Conversation ready with agent');
      });

      document.addEventListener('altan-error', (event) => {
        console.error('Chat error:', event.detail.error);
        alert('Chat unavailable. Please try again later.');
      });

      // Manual initialization on button click
      document.getElementById('start-chat').addEventListener('click', () => {
        window.AltanWidget.init({
          accountId: 'your-account-id',
          agentId: 'support-agent',
          mode: 'compact',
          placeholder: 'How can we help you today?',
          guestName: 'Customer',
          theme: 'light',
          voice_enabled: true,
          position: 'bottom-right'
        });
      });

      // Destroy widget
      document.getElementById('destroy-chat').addEventListener('click', () => {
        window.AltanWidget.destroy();
        document.getElementById('start-chat').textContent = 'Start Chat';
      });
    });
  </script>
</body>
</html>
```

### API Configuration Options

All the same configuration options from data attributes are available in the JavaScript API:

```javascript
window.AltanWidget.init({
  // Core required
  accountId: 'string',          // Required
  agentId: 'string',           // Required* (or roomId)
  roomId: 'string',            // Required* (or agentId)
  
  // Basic config
  mode: 'compact',             // 'compact' (default)
  placeholder: 'string',       // Input placeholder text
  guestName: 'string',         // User display name
  guestEmail: 'string',        // User email
  externalId: 'string',        // Custom user ID
  
  // API endpoints (advanced)
  apiBaseUrl: 'string',        // Default: 'https://api.altan.ai/platform/guest'
  authBaseUrl: 'string',       // Default: 'https://api.altan.ai/auth/login/guest'
  roomBaseUrl: 'string',       // Default: 'https://altan.ai/r'
  
  // Room personalization
  tabs: true/false,            // Show tabs
  conversation_history: true/false,  // Show history
  members: true/false,         // Show members
  settings: true/false,        // Show settings
  theme: 'light'|'dark'|'system',  // Theme mode
  title: 'string',             // Custom title
  description: 'string',       // Custom description
  voice_enabled: true/false,   // Enable voice
  suggestions: ['string'],     // Message suggestions
  
  // Widget styling
  primary_color: '#hex',       // Primary color
  background_color: '#hex',    // Background color
  background_blur: true/false, // Glassmorphism effect
  position: 'bottom-right'|'bottom-left'|'bottom-center',
  widget_width: 350,           // Width in pixels
  room_width: 450,             // Room width in pixels
  room_height: 600,            // Room height in pixels
  border_radius: 16            // Border radius in pixels
});
```

---

## 💻 React Integration

For React/Next.js applications, install the npm package:

```bash
npm install @altanlabs/sdk
```

## Usage

### Agent Mode (1-on-1 Chat)

Chat with an AI agent. Automatically finds existing conversation or creates new one.

```jsx
import { Room } from '@altan/sdk';

<Room
  mode="agent"
  accountId="your-account-id"
  agentId="agent-123"
  guestInfo={{ first_name: "John", external_id: "user-123" }}
/>
```

### Room Mode (Group Chat)

Join a specific room by ID. Perfect for community chat, support channels, etc.

```jsx
import { Room } from '@altan/sdk';

<Room
  mode="room"
  accountId="your-account-id"
  roomId="room-456"
  guestInfo={{ first_name: "John", external_id: "user-123" }}
/>
```

### Compact Mode (Floating Widget)

Shows a floating text field that expands to full chat on click.

```jsx
import { Room } from '@altan/sdk';

<Room
  mode="compact"
  accountId="your-account-id"
  agentId="agent-123"  // OR roomId="room-456"
  placeholder="Ask me anything..."
  guestInfo={{ first_name: "John", external_id: "user-123" }}
/>
```

## 🎨 Room Personalization

Customize the room interface and behavior with configuration props:

```jsx
import { Room } from '@altan/sdk';

<Room
  mode="agent"
  accountId="your-account-id"
  agentId="agent-123"
  // Room personalization options
  tabs={false}                    // Hide/show tabs
  members={false}                 // Hide/show members panel
  conversation_history={true}     // Show conversation history
  settings={true}                 // Show settings panel
  theme="dark"                    // Theme: 'light', 'dark', or 'system'
  title="Custom Support Chat"     // Custom room title
  description="Get help here"     // Custom room description
  voice_enabled={true}            // Enable voice chat
  suggestions={[                  // Predefined message suggestions
    "How can I help you?",
    "Tell me about your services",
    "I need technical support"
  ]}
/>
```

### Room Configuration Options

| Property               | Type     | Default     | Description                              |
| ---------------------- | -------- | ----------- | ---------------------------------------- |
| `tabs`                 | boolean  | `true`      | Show/hide tab navigation                 |
| `conversation_history` | boolean  | `true`      | Show/hide conversation history           |
| `members`              | boolean  | `true`      | Show/hide members panel                  |
| `settings`             | boolean  | `true`      | Show/hide settings panel                 |
| `theme`                | string   | `undefined` | Theme mode: 'light', 'dark', or 'system' |
| `title`                | string   | `undefined` | Custom room title                        |
| `description`          | string   | `undefined` | Custom room description                  |
| `voice_enabled`        | boolean  | `true`      | Enable/disable voice functionality       |
| `suggestions`          | string[] | `[]`        | Predefined message suggestions           |

### Widget Styling Options

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

### TypeScript Support

Import the configuration interface for full TypeScript support:

```typescript
import { Room, RoomConfigProps } from '@altan/sdk';

const roomConfig: RoomConfigProps = {
  tabs: false,
  theme: 'dark',
  voice_enabled: true,
  suggestions: ['Hello', 'How can I help?']
};

<Room
  mode="agent"
  accountId="your-account-id"
  agentId="agent-123"
  {...roomConfig}
/>
```

## Props

| Prop          | Type                                 | Required | Description                                            |
| ------------- | ------------------------------------ | -------- | ------------------------------------------------------ |
| `mode`        | `"agent"` \| `"room"` \| `"compact"` | ✅        | Chat mode type                                         |
| `accountId`   | string                               | ✅        | Your Altan account ID                                  |
| `agentId`     | string                               | ✅*       | Agent ID (required for agent/compact mode)             |
| `roomId`      | string                               | ✅*       | Room ID (required for room mode, optional for compact) |
| `placeholder` | string                               | ❌        | Text field placeholder (compact mode only)             |
| `guestInfo`   | object                               | ❌        | User info (name, external_id, email)                   |

*Required based on mode

## Requirements

- **Agents must be public** for agent mode to work
- **Rooms must be public** for room mode to work  
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
import { Room } from '@altan/sdk';

function App() {
  return (
    <div style={{ height: '600px' }}>
      <Room
        mode="agent"
        accountId="your-account-id"
        agentId="support-agent"
        guestInfo={{
          first_name: 'Jane',
          last_name: 'Doe',
          email: 'jane@example.com',
          external_id: 'user-456'
        }}
        // Room personalization
        theme="light"
        title="Customer Support"
        description="We're here to help!"
        voice_enabled={true}
        suggestions={[
          "I need help with my order",
          "Technical support",
          "Billing question"
        ]}
        // Widget styling
        primary_color="#6366f1"
        background_color="#ffffff"
        background_blur={true}
        position="bottom-right"
        widget_width={400}
        room_width={550}
        room_height={700}
        border_radius={20}
        onConversationReady={(room) => console.log('Chat ready!')}
        onAuthSuccess={(guest) => console.log('User authenticated:', guest.id)}
      />
    </div>
  );
}
```