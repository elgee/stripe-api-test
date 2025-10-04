Go to https://dashboard.stripe.com/register
Sign up with your email (I see you have email4lg@gmail.com - you can use that or a different one)
go to sandbox
You'll need to verify your email
you do not have to add business details
select developers under settings icon
select python as the language
select settings icon in lower right
go to workbench
copy the secret api key select and then select Copy key

open the terminal
this is for mac

command to set up environment:
cd ~/Desktop
mkdir stripe-api-test
cd stripe-api-test

then
export STRIPE_SECRET_KEY="sk_test_your_actual_key_here"


pip3 install stripe
