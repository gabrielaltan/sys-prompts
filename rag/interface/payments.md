# Payment Integration
**ALWAYS use Altan's payment API for Stripe Connect integration**

**USE THE EXACT ENDPOINT AND HEADERS SPECIFIED BELOW WITHOUT MODIFICATION**

- **Endpoint**: `POST https://pay.altan.ai/v2/connect/checkout/{account_id}/create_checkout_session?stripe_connect_id={stripe_connect_id}`

**If `stripe_connect_id` is not present in the message trail, ask Altan Pay to provide the ID!**

- **Headers**: `{"Content-Type": "application/json"}`

**NO API KEYS NEEDED FOR THIS END POINT IN THE HEADER**

- **Request Body**:
```json
{
  "payload": {
    "success_url": "https://your.app.com/success/",
    "cancel_url": "https://your.app.com/cancel/",
    "line_items": [
      {
        "price": "price_ABC123",
        "quantity": 1
      }
    ],
    "mode": "payment"
  }
}
```

**Response Handling**:
- Extract checkout URL from response: `{ "url": "https://checkout.stripe.com/pay/..." }`
- Redirect user to Stripe Checkout securely
- Implement webhook handling for payment confirmation

**Critical Implementation Rules**:
1. **URL Substitution**: Replace `{account_id}` and `{stripe_connect_id}` with actual values
2. **Mode Selection**: Use "payment" for one-time, "subscription" for recurring
3. **Line Items**: Include actual cart items with correct price IDs and quantities
4. **URL Configuration**: Set appropriate success/cancel URLs for your application
5. **Error Handling**: Implement proper error handling for failed API calls