from django.urls import path
from account.views.register_view import RegisterView, GoogleLoginView
from account.views.user_view import UserDataView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('google-login/', GoogleLoginView.as_view(), name='google-login'),

    path('user-data/', UserDataView.as_view(), name='user-data'),
]
