from django.urls import path
from account.views.register_view import RegisterView, GoogleLoginView, LoginView
from account.views.user_view import UserDataView, UserSearchView

from account.views.user_presence_view import UserPresenceView, SelectedUserPresenceView

urlpatterns = [
    
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('google-login/', GoogleLoginView.as_view(), name='google-login'),

    path('user-data/', UserDataView.as_view(), name='user-data'),

    path('user-presence/', UserPresenceView.as_view(), name='user-presence'),
    path('user-presence/<int:user_id>/', SelectedUserPresenceView.as_view(), name='selected-user-presence'),
    path('user-search/', UserSearchView.as_view(), name='user-search'),
]
