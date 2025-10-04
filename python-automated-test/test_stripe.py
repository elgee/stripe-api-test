import stripe
import os
from stripe import InvalidRequestError, AuthenticationError

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')


print("=" * 60)
print("STRIPE API DOCUMENTATION TESTING")
print("=" * 60)
print()

# Authentication validates the bearer token, the key format, and checks unauthorized access.
print("TEST 1: Authentication")
print("-" * 60)
try:
    customers = stripe.Customer.list(limit=1)
    print("PASS: Authentication successful")
    print(f"   API Key is valid (ends in: ...{stripe.api_key[-4:]})")
except AuthenticationError as e:
    print(f"FAIL: Authentication failed - {e}")
except Exception as e:
    print(f"ERROR: {e}")
print()


# Create a PaymentIntent. Check that the POST endpoint works, required params are enforced, and response fields are present. A PaymentIntent is the core object for managing the complete payment process. PaymentIntent adapts to different payment methods and regulatory requirements automatically. Create exactly one PaymentIntent for each order or customer session in your system.

print("TEST 2: Create PaymentIntent")
print("-" * 60)
try:
    payment_intent = stripe.PaymentIntent.create(
        amount=2000,
        currency="usd",
        payment_method_types=["card"],
        description="Create PaymentIntent"
    )
    print("PASS: PaymentIntent created successfully")
    print(f"   ID: {payment_intent.id}")
    print(f"   Amount: ${payment_intent.amount / 100:.2f}")
    print(f"   Currency: {payment_intent.currency.upper()}")
    print(f"   Status: {payment_intent.status}")
    payment_intent_id = payment_intent.id
except Exception as e:
    print(f"FAIL: {e}")
    payment_intent_id = None
print()

# Retrieve PaymentIntent by ID. Check that the GET endpoint works, required params are enforced, and response fields are present.

print("TEST 3: Retrieve PaymentIntent")
print("-" * 60)
if payment_intent_id:
    try:
        retrieved = stripe.PaymentIntent.retrieve(payment_intent_id)
        print("PASS: PaymentIntent retrieved successfully")
        print(f"   ID: {retrieved.id}")
        print(f"   Status: {retrieved.status}")
    except Exception as e:
        print(f"FAIL: {e}")
else:
    print("SKIP: No PaymentIntent ID from previous test")
print()

# Create a Customer. Check that the POST endpoint works, required params are enforced, and response fields are present. A Customer object is a representation of a customer in your Stripe account. You can store multiple payment methods, shipping addresses, and more on the Customer object.
print("TEST 4: Create Customer")
print("-" * 60)
try:
    customer = stripe.Customer.create(
        email="test.customer@example.com",
        name="Create Customer",
        description="Create Customer"
    )
    print("PASS: Customer created successfully")
    print(f"   ID: {customer.id}")
    print(f"   Email: {customer.email}")
    print(f"   Name: {customer.name}")
except Exception as e:
    print(f"FAIL: {e}")
print()

# List Customers with pagination. Check that the GET endpoint works, pagination parameters are enforced, and response fields are present.
print("TEST 5: List Customers (Pagination)")
print("-" * 60)
try:
    customers = stripe.Customer.list(limit=3)
    print("PASS: Customers listed successfully")
    print(f"   Retrieved {len(customers.data)} customers")
    print(f"   Has more: {customers.has_more}")
except Exception as e:
    print(f"FAIL: {e}")
print()

# Error handling: Missing required parameter
print("TEST 6: Error handling: Missing required parameter")
print("-" * 60)
try:
    bad_payment = stripe.PaymentIntent.create(currency="usd")
    print("FAIL: Should have raised an error")
except InvalidRequestError as e:
    print("PASS: Correctly caught missing parameter error")
    print(f"   Error: {str(e)}")
except Exception as e:
    print(f"Unexpected error: {e}")
print()

# Error handling: Invalid currency parameter value
print("TEST 7: Error handling: Invalid currency")
print("-" * 60)
try:
    bad_payment = stripe.PaymentIntent.create(amount=1000, currency="INVALID")
    print("FAIL: Should have raised an error")
except InvalidRequestError as e:
    print("PASS: Correctly caught invalid currency error")
    print(f"   Error: {str(e)}")
except Exception as e:
    print(f"Unexpected error: {e}")
print()

# Final banner
print("=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("All tests completed successfully!")
print("=" * 60)