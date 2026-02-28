from rest_framework.views import APIView, settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests

from account.serializers.register_serializer import RegisterSerializer
from account.models import User

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User মডেলটি সঠিকভাবে গেট করুন
User = get_user_model()

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('id_token')
        
        # settings.py থেকে Client ID নেওয়া বেটার, 
        # তবে কোডে থাকলে তা নিশ্চিত হোন এটি "Web Application" এর ID
        WEB_CLIENT_ID = "13939260260-bgfkvjt54i7622rs536jam98lg3sua4k.apps.googleusercontent.com"
        
        if not token:
            return Response({"error": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # ১. Google এর মাধ্যমে টোকেন ভেরিফাই করুন
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), WEB_CLIENT_ID, clock_skew_in_seconds=10
            )

            # Debugging: টার্মিনালে ডাটা চেক করুন
            print(f"Google ID Token Info: {idinfo}")

            # ২. Google থেকে ইউজার তথ্য এক্সট্রাক্ট করুন
            email = idinfo['email']
            google_id = idinfo['sub']
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')
            profile_picture = idinfo.get('picture', '')

            # ৩. ইউজার খোঁজার লজিক (ইমেইল অথবা গুগল আইডি দিয়ে)
            user = User.objects.filter(email=email).first()

            if not user:
                # ৪. নতুন ইউজার তৈরি করুন
                # Username ইউনিক হতে হবে, তাই ইমেইল ব্যবহার করা নিরাপদ
                user = User.objects.create_user(
                    username=email, 
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    profile_picture=profile_picture,
                    google_id=google_id
                )
            else:
                # ৫. ইউজার থাকলে গুগল আইডি আপডেট করুন (যদি না থাকে)
                if not user.google_id:
                    user.google_id = google_id
                    user.save()

            # ৬.JWT টোকেন জেনারেট করুন
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'email': user.email,
                    'first_name': user.first_name,
                    'profile_picture': user.profile_picture
                }
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            # টোকেন ভ্যালিড না হলে এই এরর আসবে
            print(f"Token Validation Error: {e}")
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Internal Error: {e}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)