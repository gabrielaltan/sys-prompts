## Stripe Connect Checkout via Altan Pay

> **⚠️ Always use Altan’s Payment API (no substitutions or extra headers).**

### 1. Endpoint & Headers

```http
POST https://pay.altan.ai/v2/connect/checkout/{account_id}/create_checkout_session?stripe_connect_id={stripe_connect_id}
Content-Type: application/json
```

* **Do not** include any API key in the headers for this endpoint.
* If you don’t yet have `stripe_connect_id`, **prompt Altan Pay** to provide it before proceeding.

---

### 2. Request Body

```json
{
  "payload": {
    "success_url": "https://your.app.com/success/",
    "cancel_url":  "https://your.app.com/cancel/",
    "line_items": [
      {
        "price":    "price_ABC123",
        "quantity": 1
      }
    ],
    "mode": "payment"
  }
}
```

* **success\_url / cancel\_url**
  Set to your application’s endpoints to handle post-checkout flow.
* **line\_items**
  List each cart item with its Stripe price ID and desired quantity.
* **mode**

  * `"payment"` = one-time purchase
  * `"subscription"` = recurring billing

---

### 3. Handling the Response

1. **Parse** the JSON response:

   ```json
   { "url": "https://checkout.stripe.com/pay/..." }
   ```
2. **Redirect** your user’s browser to the returned `url`.
3. **Implement** a webhook listener on your server to confirm payment events.

---

### 4. Critical Implementation Rules

1. **URL Substitution**
   Replace `{account_id}` and `{stripe_connect_id}` with the real values before calling.
2. **Mode Selection**
   Choose `"payment"` for one-time charges or `"subscription"` for recurring.
3. **Accurate Line Items**
   Ensure each item’s `price` ID and `quantity` reflect the actual cart.
4. **URL Configuration**
   Use your own application URLs for success and cancellation.
5. **Error Handling**
   Gracefully handle HTTP failures and malformed responses (e.g., retry, log, alert).
