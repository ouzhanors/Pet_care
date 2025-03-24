from django.test import TestCase
from .firebase_config import send_notification

# Create your tests here.

class FirebaseNotificationTest(TestCase):
    def test_send_notification(self):
        # Test için örnek bir FCM token (gerçek token ile değiştirilmeli)
        test_token = "YOUR_TEST_FCM_TOKEN"
        title = "Test Bildirimi"
        body = "Bu bir test bildirimidir."
        
        success, response = send_notification(test_token, title, body)
        print(f"Bildirim gönderme sonucu: {'Başarılı' if success else 'Başarısız'}")
        print(f"Yanıt: {response}")
