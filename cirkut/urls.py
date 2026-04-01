from django.contrib import admin
from django.urls import path, include
from . import views
from cirkut.corn import backup_database

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('chat/', include('chat.urls')),
    path('api/', include('api.urls')),

    # ডাটাবেস ব্যাকআপের জন্য একটি URL পাথ (যদি ম্যানুয়ালি ট্রিগার করতে চাও)
    path('backup/', backup_database, name='backup_database'),
]
