# Set up a Stripe API

Use this guide as a supplement to the link:https://docs.stripe.com/api[Stripe API documentation].
This documentation covers the core Stripe payment processing endpoints.

**Base URL:** `https://api.stripe.com`

**API Version:** `2024-10-28`

## Authentication

All API requests require authentication using your Stripe API key. Include your secret key in the `Authorization` header using Bearer authentication.

```
Authorization: Bearer sk_test_your_secret_key
```

### API Keys

Stripe provides two types of API keys:

- **Test keys:** Use these for development and testing. Test keys have the prefix `sk_test_`
- **Live keys:** Use these in production. Live keys have the prefix `sk_live_`

**Important:** Never expose your secret API keys in client-side code or public repositories.

### Example Authentication

```bash
curl https://api.stripe.com/v1/customers \
  -u sk_test_4eC39HqLyjWDarjtT1zdp7dc: \
  -X GET
```

Note: The colon (`:`) after the API key is required when using basic authentication.

## Rate Limiting

Stripe's API implements rate limiting to ensure service stability:

- **Standard limit:** 100 requests per second in live mode
- **Test mode:** 25 requests per second

When you exceed the rate limit, the API returns a `429 Too Many Requests` status code. Implement exponential backoff to handle rate limit errors gracefully.

## Idempotency

To safely retry API requests without accidentally performing the same operation twice, include an `Idempotency-Key` header with a unique value (such as a UUID).

```bash
curl https://api.stripe.com/v1/charges \
  -u sk_test_4eC39HqLyjWDarjtT1zdp7dc: \
  -H "Idempotency-Key: unique_key_here" \
  -d amount=2000 \
  -d currency=usd
```

Stripe saves the result of the initial request and returns the same response for subsequent requests with the same idempotency key for 24 hours.

## Core Resources

### Payment Intents

Payment Intents track the lifecycle of a customer payment and handle complex payment flows, including authentication and error handling.

### Customers

Customer objects represent your users in Stripe. Store customer information to enable faster checkout and subscription management.

### Payment Methods

Payment Methods represent ways customers can pay, such as credit cards, bank accounts, or digital wallets.

## API Endpoints

### Create a Payment Intent

Creates a Payment Intent object to track a payment from creation through checkout and charge.

**Endpoint:** `POST /v1/payment_intents`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `amount` | integer | Yes | Amount in cents (e.g., 2000 for $20.00) |
| `currency` | string | Yes | Three-letter ISO currency code (e.g., "usd") |
| `customer` | string | No | ID of an existing customer |
| `payment_method` | string | No | ID of the payment method to use |
| `description` | string | No | Arbitrary description for the payment |
| `metadata` | object | No | Key-value pairs for storing additional information |

**Example Request:**

```bash
curl https://api.stripe.com/v1/payment_intents \
  -u sk_test_4eC39HqLyjWDarjtT1zdp7dc: \
  -d amount=2000 \
  -d currency=usd \
  -d "payment_method_types[]"=card \
  -d description="Payment for order #12345"
```

**Example Response:**

```json
{
  "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",
  "object": "payment_intent",
  "amount": 2000,
  "currency": "usd",
  "status": "requires_payment_method",
  "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",
  "created": 1680800504,
  "description": "Payment for order #12345",
  "metadata": {},
  "payment_method_types": ["card"]
}
```

**Response Fields:**

- `id` - Unique identifier for the Payment Intent
- `status` - Current status of the payment (see Payment Intent Statuses below)
- `client_secret` - Secret key used to complete payment on the client side
- `amount` - Amount in cents
- `currency` - Three-letter ISO currency code

### Retrieve a Payment Intent

Retrieves the details of a Payment Intent that has been previously created.

**Endpoint:** `GET /v1/payment_intents/:id`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The ID of the Payment Intent to retrieve |

**Example Request:**

```bash
curl https://api.stripe.com/v1/payment_intents/pi_3MtwBwLkdIwHu7ix28a3tqPa \
  -u sk_test_4eC39HqLyjWDarjtT1zdp7dc:
```

**Example Response:**

```json
{
  "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",
  "object": "payment_intent",
  "amount": 2000,
  "currency": "usd",
  "status": "succeeded",
  "created": 1680800504,
  "description": "Payment for order #12345"
}
```

### Confirm a Payment Intent

Confirms a Payment Intent, attempting to complete the payment.

**Endpoint:** `POST /v1/payment_intents/:id/confirm`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The ID of the Payment Intent to confirm |
| `payment_method` | string | No | ID of the payment method to use |
| `return_url` | string | Conditional | Required if payment requires redirect (e.g., 3D Secure) |

**Example Request:**

```bash
curl https://api.stripe.com/v1/payment_intents/pi_3MtwBwLkdIwHu7ix28a3tqPa/confirm \
  -u sk_test_4eC39HqLyjWDarjtT1zdp7dc: \
  -d payment_method=pm_card_visa \
  -X POST
```

### Create a Customer

Creates a new customer object to store payment information and track multiple charges.

**Endpoint:** `POST /v1/customers`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `email` | string | No | Customer's email address |
| `name` | string | No | Customer's full name |
| `description` | string | No | Arbitrary description of the customer |
| `metadata` | object | No | Key-value pairs for storing additional information |
| `payment_method` | string | No | ID of payment method to attach to customer |

**Example Request:**

```bash
curl https://api.stripe.com/v1/customers \
  -u sk_test_4eC39HqLyjWDarjtT1zdp7dc: \
  -d email="customer@example.com" \
  -d name="Jenny Rosen" \
  -d description="Customer for jenny.rosen@example.com"
```

**Example Response:**

```json
{
  "id": "cus_NffrFeUfNV2Hib",
  "object": "customer",
  "email": "customer@example.com",
  "name": "Jenny Rosen",
  "description": "Customer for jenny.rosen@example.com",
  "created": 1680800504,
  "metadata": {}
}
```

### Retrieve a Customer

Retrieves details of an existing customer.

**Endpoint:** `GET /v1/customers/:id`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The ID of the customer to retrieve |

**Example Request:**

```bash
curl https://api.stripe.com/v1/customers/cus_NffrFeUfNV2Hib \
  -u sk_test_4eC39HqLyjWDarjtT1zdp7dc:
```

### List All Customers

Returns a list of your customers. Customers are returned in sorted order, with the most recent customers appearing first.

**Endpoint:** `GET /v1/customers`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Number of results to return (default: 10, max: 100) |
| `starting_after` | string | No | Cursor for pagination - customer ID to start after |
| `ending_before` | string | No | Cursor for pagination - customer ID to end before |
| `email` | string | No | Filter by customer email address |

**Example Request:**

```bash
curl -G https://api.stripe.com/v1/customers \
  -u sk_test_4eC39HqLyjWDarjtT1zdp7dc: \
  -d limit=3
```

**Example Response:**

```json
{
  "object": "list",
  "data": [
    {
      "id": "cus_NffrFeUfNV2Hib",
      "object": "customer",
      "email": "customer@example.com",
      "name": "Jenny Rosen"
    }
  ],
  "has_more": true,
  "url": "/v1/customers"
}
```

### Create a Payment Method

Creates a Payment Method object representing a customer's payment instrument.

**Endpoint:** `POST /v1/payment_methods`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `type` | string | Yes | Type of payment method (e.g., "card", "us_bank_account") |
| `card` | object | Conditional | Required if type is "card" |
| `billing_details` | object | No | Billing information associated with the payment method |

**Example Request:**

```bash
curl https://api.stripe.com/v1/payment_methods \
  -u sk_test_4eC39HqLyjWDarjtT1zdp7dc: \
  -d type=card \
  -d "card[number]"=4242424242424242 \
  -d "card[exp_month]"=12 \
  -d "card[exp_year]"=2025 \
  -d "card[cvc]"=314
```

**Example Response:**

```json
{
  "id": "pm_1MtwhRLkdIwHu7ixUEgbide",
  "object": "payment_method",
  "type": "card",
  "card": {
    "brand": "visa",
    "last4": "4242",
    "exp_month": 12,
    "exp_year": 2025
  },
  "created": 1680800695
}
```

## Payment Intent Statuses

Payment Intents progress through several statuses during their lifecycle:

| Status | Description |
|--------|-------------|
| `requires_payment_method` | Initial state - waiting for payment method |
| `requires_confirmation` | Payment method attached, needs confirmation |
| `requires_action` | Customer action required (e.g., 3D Secure authentication) |
| `processing` | Payment is being processed |
| `succeeded` | Payment completed successfully |
| `canceled` | Payment Intent was canceled |

## Pagination

List endpoints return paginated results. Use the `limit` parameter to control the number of results and cursor-based pagination for navigation.

**Forward Pagination:**
```bash
curl -G https://api.stripe.com/v1/customers \
  -u sk_test_4eC39HqLyjWDarjtT1zdp7dc: \
  -d limit=10 \
  -d starting_after=cus_NffrFeUfNV2Hib
```

**Backward Pagination:**
```bash
curl -G https://api.stripe.com/v1/customers \
  -u sk_test_4eC39HqLyjWDarjtT1zdp7dc: \
  -d limit=10 \
  -d ending_before=cus_NffrFeUfNV2Hib
```

## Webhooks

Stripe uses webhooks to notify your application when events occur in your account. Configure webhook endpoints in your Stripe Dashboard to receive real-time updates.

### Common Webhook Events

- `payment_intent.succeeded` - Payment completed successfully
- `payment_intent.payment_failed` - Payment attempt failed
- `customer.created` - New customer created
- `customer.updated` - Customer information updated
- `charge.refunded` - Charge was refunded

### Webhook Endpoint Example

```javascript
// Node.js/Express example
app.post('/webhook', express.raw({type: 'application/json'}), (request, response) => {
  const sig = request.headers['stripe-signature'];
  let event;

  try {
    event = stripe.webhooks.constructEvent(request.body, sig, endpointSecret);
  } catch (err) {
    response.status(400).send(`Webhook Error: ${err.message}`);
    return;
  }

  // Handle the event
  switch (event.type) {
    case 'payment_intent.succeeded':
      const paymentIntent = event.data.object;
      console.log('PaymentIntent was successful!');
      break;
    default:
      console.log(`Unhandled event type ${event.type}`);
  }

  response.send();
});
```

### Verifying Webhook Signatures

Always verify webhook signatures to ensure requests originate from Stripe:

1. Retrieve your webhook signing secret from the Stripe Dashboard
2. Extract the signature from the `stripe-signature` header
3. Use Stripe's library to verify the signature matches the payload

## Error Handling

Stripe uses conventional HTTP response codes to indicate success or failure.

### HTTP Status Codes

| Code | Description |
|------|-------------|
| `200` | Success - request completed successfully |
| `400` | Bad Request - invalid parameters |
| `401` | Unauthorized - invalid API key |
| `402` | Request Failed - parameters valid but request failed |
| `403` | Forbidden - insufficient permissions |
| `404` | Not Found - resource doesn't exist |
| `429` | Too Many Requests - rate limit exceeded |
| `500`, `502`, `503`, `504` | Server Errors - something went wrong on Stripe's end |

### Error Response Format

```json
{
  "error": {
    "type": "card_error",
    "code": "card_declined",
    "message": "Your card was declined.",
    "param": "card_number"
  }
}
```

**Error Object Fields:**

- `type` - Category of error (`api_error`, `card_error`, `invalid_request_error`)
- `code` - Specific error code for programmatic handling
- `message` - Human-readable error message
- `param` - Parameter related to the error (if applicable)

### Common Error Codes

| Code | Description |
|------|-------------|
| `card_declined` | Card was declined by the issuer |
| `expired_card` | Card has expired |
| `incorrect_cvc` | CVC verification failed |
| `insufficient_funds` | Insufficient funds in the account |
| `invalid_number` | Card number is invalid |
| `rate_limit` | Too many requests in a short period |

### Error Handling Best Practices

1. **Log all errors** for debugging and monitoring
2. **Display user-friendly messages** - don't expose technical details to end users
3. **Implement retry logic** with exponential backoff for rate limit errors
4. **Validate input** on the client side before making API requests
5. **Use idempotency keys** to safely retry failed requests

## Testing

Stripe provides test mode for development without processing real payments.

### Test Card Numbers

Use these card numbers in test mode to simulate different scenarios:

| Card Number | Scenario |
|-------------|----------|
| `4242424242424242` | Successful payment |
| `4000000000000002` | Card declined |
| `4000002500003155` | Requires authentication (3D Secure) |
| `4000000000009995` | Insufficient funds |
| `4000000000000069` | Expired card |

### Test CVC and Expiration

- **CVC:** Any 3-digit number (e.g., 123)
- **Expiration:** Any future date

## SDKs and Libraries

Stripe provides official libraries for popular programming languages:

- **Node.js:** `npm install stripe`
- **Python:** `pip install stripe`
- **Ruby:** `gem install stripe`
- **PHP:** `composer require stripe/stripe-php`
- **Java:** Maven or Gradle
- **Go:** `go get github.com/stripe/stripe-go`

### Node.js Example

```javascript
const stripe = require('stripe')('sk_test_4eC39HqLyjWDarjtT1zdp7dc');

async function createPayment() {
  const paymentIntent = await stripe.paymentIntents.create({
    amount: 2000,
    currency: 'usd',
    payment_method_types: ['card'],
  });
  
  console.log(paymentIntent.id);
}
```

## Additional Resources

- **Stripe Dashboard:** Monitor payments and manage your account at https://dashboard.stripe.com
- **API Reference:** Complete API documentation at https://stripe.com/docs/api
- **Support:** Contact Stripe support through your Dashboard
- **Status Page:** Check API status at https://status.stripe.com

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2024-10-28 | v1.0 | Initial API documentation release |
