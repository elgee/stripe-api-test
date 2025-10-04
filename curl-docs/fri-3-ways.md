# Testing Stripe API endpoints with cURL

This guide demonstrates how to test Stripe's payment endpoints using cURL.
cURL is widely available across operating systems.

1. Check that cURL is installed on your computer. A version number, for example `curl 7.78.0`, is displayed if cURL is installed:

    ```bash
    curl --version
    ```

> **Note:** These instructions have been tested on macOS. Other operating systems may require slightly different instructions.

## Testing objectives

Each test is performed to show that the API behavior matches the documented specifications.

- Verify that all API endpoints function as documented
- Validate that request/response formats match specifications
- Confirm that error scenarios produce expected responses
- Test authentication mechanisms

## Test coverage

**Authentication:** Verify that valid API keys are accepted and invalid keys are rejected.

**Payment Intents:** A Payment Intent is the core object for managing the complete payment process in Stripe. Each Payment Intent represents a single payment attempt and automatically handles authentication requirements and payment method variations. Create a Payment Intent for each customer session in your system.

**Customers:** A Customer object is a representation of a customer in your Stripe account. You can store multiple payment methods, shipping addresses, and more on the Customer object, and all fields are optional.

**Currency handling:** Stripe uses ISO currency codes and amounts specified in the smallest currency unit, for example, cents for `usd`.

## Use a Stripe secret API key to authenticate

Get a secret API key from Stripe and set an environment variable with the key, so you can authenticate in your terminal.

1. [Sign up for Stripe](https://dashboard.stripe.com/register) if you do not already have an account.
2. Skip the business information questions.
3. Select **Go to sandbox**.
4. Select **Got it** under **Verify your business**.
5. Select the **Secret key** to copy it.
6. Replace `<your Stripe Secret API key>` with [your copied key](#get-a-stripe-secret-api-key):

    ```bash
    export STRIPE_SECRET_KEY="<your Stripe Secret API key>"
    ```

## Run cURL tests

1. Verify authentication:

    ```bash
    curl https://api.stripe.com/v1/customers \
      -u $STRIPE_SECRET_KEY:
    ```

    Expected response (empty customer list):

    ```json
    {
      "object": "list",
      "data": [],
      "has_more": false,
      "url": "/v1/customers"
    }
    ```

    Testing using no authentication should fail:

    ```bash
    curl https://api.stripe.com/v1/customers
    ```

    Testing with an invalid key should fail:

    ```bash
    curl https://api.stripe.com/v1/customers \
     -u sk_test_invalid_key:
    ```

2. Create a Payment Intent (POST request):

    ```bash
    curl https://api.stripe.com/v1/payment_intents \
      -u $STRIPE_SECRET_KEY: \
      -d amount=12500 \
      -d currency=usd \
      -d description="Payment for order" \
      -d "payment_method_types[]"=card
    ```

    Expected response includes:

    - Payment Intent ID (starts with `pi_`)
    - Amount: 12500
    - Currency: usd
    - Status: requires_payment_method

3. Retrieve the Payment Intent (GET request). Replace `<payment_intent_id>` with the ID from step 2:

    ```bash
    curl https://api.stripe.com/v1/payment_intents/<payment_intent_id> \
      -u $STRIPE_SECRET_KEY:
    ```

    Expected response is a matching Payment Intent ID.

4. Test error handling by removing a required parameter:

    ```bash
    curl https://api.stripe.com/v1/payment_intents \
      -u $STRIPE_SECRET_KEY: \
      -d currency=eur
    ```

    Expected error response includes:

    ```json
    {
      "error": {
        "code": "parameter_missing",
        "message": "Missing required param: amount.",
        "param": "amount",
        "type": "invalid_request_error"
      }
    }
    ```

5. Create a Customer:

    ```bash
    curl https://api.stripe.com/v1/customers \
      -u $STRIPE_SECRET_KEY: \
      -d email="customer@example.com" \
      -d name="Example Customer"
    ```

    Expected response includes:

    - Customer ID (starts with `cus_`)
    - Email: <customer@example.com>
    - Name: Example Customer

6. Test error handling by including an invalid parameter:

    ```bash
    curl https://api.stripe.com/v1/customers \
      -u $STRIPE_SECRET_KEY: \
      -d notaparameter="test"
    ```

    Expected error response includes:

    ```json
    {
      "error": {
        "code": "parameter_unknown",
        "message": "Received unknown parameter: notaparameter",
        "param": "notaparameter",
        "type": "invalid_request_error"
      }
    }
    ```

## Troubleshooting

The table below will help you fix problems in your testing.

| Issue | Reason | Possible fixes |
|-------|----------|-----------|
| All requests return 401 Unauthorized | Authentication fails | - Verify Stripe account is active <br>- Verify secret key starts with `sk_test_` <br>- Verify environment variable is entered correctly <br>- Verify colon (`:`) is present after key in cURL:`-u $STRIPE_SECRET_KEY:` |
| 400 Bad Request when creating Payment Intent | Payment Intent creation fails | - Verify `amount` is a positive integer<br>- Verify `currency` is a valid 3-letter ISO code <br>- Verify that all required parameters are set
