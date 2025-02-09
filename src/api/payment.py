import streamlit as st
import razorpay

# Razorpay API Keys (Replace with your credentials)
RAZORPAY_KEY_ID = "your_key_id"
RAZORPAY_KEY_SECRET = "your_key_secret"
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def create_order(amount):
    order_data = {
        "amount": amount * 100,  # Razorpay accepts amount in paise
        "currency": "INR",
        "payment_capture": 1  # Auto-capture after payment
    }
    return client.order.create(order_data)


def payment_web(RAZORPAY_KEY_ID, amount):
    """
    Generates the Razorpay payment gateway script for donation.
    
    Parameters:
        RAZORPAY_KEY_ID (str): Your Razorpay Key ID for the payment gateway.
        amount (float): The amount to be donated in INR.

    Returns:
        str: The Razorpay checkout script template as HTML.
    """
    # Create Razorpay order (this should ideally be done via an API call to your backend)
    order = create_order(amount)
    order_id = order["id"]
    
    razorpay_script = f"""
    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
    <script>
        var options = {{
            "key": "{RAZORPAY_KEY_ID}",
            "amount": {amount * 100},  # Amount in paise
            "currency": "INR",
            "name": "Disaster Relief Fund",
            "description": "Your support can make a difference!",
            "order_id": "{order_id}",
            "handler": function (response){{
                alert('Payment Successful! Payment ID: ' + response.razorpay_payment_id);
            }},
            "theme": {{
                "color": "#3399cc"
            }}
        }};
        var rzp1 = new Razorpay(options);
        rzp1.open();
    </script>
    """
    return razorpay_script



