import os
import firebase_admin
from firebase_admin import messaging, credentials
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

def send_notification(token, title, body):
    # ১. চেক করুন Firebase অলরেডি কানেক্টেড কি না
    if not firebase_admin._apps:
        cred_path = r'C:\Users\siam\projects\cirkut\cirkut\firebaseKey.json'
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

    # ২. অ্যান্ড্রয়েডে পপ-আপ আসার জন্য সঠিক কনফিগুরেশন
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        android=messaging.AndroidConfig(
            priority='high', # এটি মেসেজ ডেলিভারি প্রায়োরিটি
            notification=messaging.AndroidNotification(
                priority='max', # এটি দিয়ে পপ-আপ (Heads-up) নোটিফিকেশন নিশ্চিত হয়
                default_sound=True,
                notification_count=1,
            ),
        ),
        token=token,
    )

    # ৩. মেসেজ পাঠানো
    try:
        response = messaging.send(message)
        print('Successfully sent message:', response)
        return response
    except Exception as e:
        print(f"Firebase Error: {e}")
        return str(e)