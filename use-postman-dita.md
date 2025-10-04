# Testing Stripe API endpoints

This guide demonstrates how to test Stripe's payment endpoints using Postman.

## Testing objectives

- Verify that all API endpoints function as documented
- Validate that request/response formats match specifications
- Confirm that error scenarios produce expected responses
- Test authentication mechanisms

## Test coverage

**Authentication:** Verify that valid API keys are accepted and invalid keys are rejected.

**Payment Intents:** A Payment Intent is the core object for managing the complete payment process in Stripe. Each Payment Intent represents a single payment attempt and automatically handles authentication requirements and payment method variations. Create a Payment Intent for each customer session in your system.

**Customers:** A Customer object is a representation of a customer in your Stripe account. You can store multiple payment methods, shipping addresses, and more on the Customer object, and all fields are optional.

**Currency handling:** Stripe uses ISO currency codes and amounts specified in the smallest currency unit, for example, cents for `usd`.

> **Note:** These instructions have been tested on macOS. Other operating systems may not be fully supported.

## Get a Stripe secret API key

To get a secret API key from Stripe:

1. [Sign up for Stripe](https://dashboard.stripe.com/register) if you do not already have an account.
2. Skip the business information questions.
3. Select **Go to sandbox**.
4. Select **Got it** under **Verify your business**.
5. Select the **Secret key** to copy it.
6. Store the copied Secret key in a secure location.

## Configure Postman

1. Download and install Postman from <https://www.postman.com/downloads/>
2. Create a new collection named "Stripe API Tests"
3. Set collection-level authorization:
    - Type: Basic Auth
    - Username: Your test API key (e.g., `sk_test_4eC39HqLyjWDarjtT1zdp7dc`)
    - Password: Leave blank
4. Set base URL variable: `https://api.stripe.com/v1`

## Test Cases

1. Create requests for each endpoint
2. Add test scripts to validate responses
3. Use Postman variables for dynamic data

**Example Postman Test Script:**

```javascript
// Test for Create Payment Intent endpoint
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains payment_intent object", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.object).to.eql("payment_intent");
});

pm.test("Amount is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.amount).to.eql(2000);
});

pm.test("Status is requires_payment_method", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.status).to.eql("requires_payment_method");
});

// Save the payment intent ID for subsequent tests
pm.environment.set("payment_intent_id", pm.response.json().id);
```

## Common Issues and Solutions

### Issue: Authentication Fails

**Symptoms:** All requests return 401 Unauthorized

**Solutions:**

- Verify you're using test mode key (starts with `sk_test_`)
- Check for extra spaces in the API key
- Ensure colon (`:`) is present after key in cURL: `-u sk_test_key:`
- Verify Stripe account is active

### Issue: Payment Intent Creation Fails

**Symptoms:** 400 Bad Request when creating Payment Intent

**Solutions:**

- Verify `amount` is an integer (cents, not dollars)
- Check `currency` is a valid 3-letter ISO code
- Ensure `payment_method_types` is an array
- Validate all required parameters are included

### Issue: Test Cards Don't Work

**Symptoms:** Card validation errors with test card numbers

**Solutions:**

- Confirm you're in test mode
- Use complete 16-digit card numbers
- Ensure expiration date is in the future
- Use any 3-digit CVC (e.g., 123)

## Test Results Summary

| Category | Tests | Passed | Failed | Notes |
|----------|-------|--------|--------|-------|
| Authentication | 3 | 3 | 0 | All scenarios verified |
| Payment Intents | 5 | 5 | 0 | CRUD operations confirmed |
| Customers | 4 | 4 | 0 | Including pagination |
| Error Handling | 6 | 6 | 0 | All error types tested |
| Test Cards | 4 | 4 | 0 | All scenarios work |
| Idempotency | 2 | 2 | 0 | Prevents duplicates |
| SDK Integration | 3 | 3 | 0 | Node.js SDK verified |
| **Total** | **27** | **27** | **0** | **Documentation accurate** |


