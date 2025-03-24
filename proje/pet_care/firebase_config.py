import firebase_admin
from firebase_admin import credentials, messaging

def initialize_firebase():
    try:
        # Firebase Admin SDK'yı başlat
        cred = credentials.Certificate('firebase-credentials.json')
        firebase_admin.initialize_app(cred)
        return True
    except Exception as e:
        print(f"Firebase başlatma hatası: {str(e)}")
        return False

def send_notification(token, title, body):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            token=token
        )
        response = messaging.send(message)
        return True, response
    except Exception as e:
        return False, str(e) 