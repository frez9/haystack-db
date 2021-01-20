import braintree 
import json 

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="cthsw4zt5hj2gpfx",
        public_key="qsvsw7x938tw44g5",
        private_key="ae0f72cf6fe69818a87943b503224fc7"
    )
)

def generate_client_token(customer_id):
    client_token = gateway.client_token.generate({
    "customer_id": customer_id
    })

def process_payments(listing, payment_nonce, device_data):
    price = str(listing.price)

    result = gateway.transaction.sale({
    "amount": price,
    "payment_method_nonce": payment_nonce,
    "device_data": device_data,
    "options": {
      "submit_for_settlement": True
    }
    })
    result_json = {
        'success': result.is_success
    }
    return result_json

