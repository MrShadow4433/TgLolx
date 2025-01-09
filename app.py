import stripe
from flask import Flask, request, jsonify

app = Flask(__name__)

# Настройка ключа API
stripe.api_key = 'sk_test_51QZ1BAKK0Td3MYcEKztSFhPT6yjhIVQYk63Ibd7Kt3MNzgDcC0AYNz1Tzc3gdCsV5LP9AX7zI5nCDm2QHgaArNKk00hmmsubyM'  # Ваш секретный ключ

# Секрет подписи для вебхука
endpoint_secret = 'whsec_YIxaCyU78PCnTyZBf3gjufNnx3A2uTZL'

@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Недопустимая нагрузка
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        # Недопустимая подпись
        return 'Invalid signature', 400

    # Обработка события
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Логика обработки успешной оплаты
        user_id = session['client_reference_id']
        course_name = session['metadata']['course_name']
        # Здесь добавьте логику для выдачи курса пользователю

    return '', 200

if __name__ == '__main__':
    app.run(port=5000)