from django.conf.urls.static import static
from django.urls import path, include , re_path
from django.contrib import admin
from django.conf import settings
from account.views import (
        Login, 
        Register, 
        activate
    )

urlpatterns = [
    path('login/', Login.as_view(), name = 'login'),
    path('signup/',Register.as_view(), name = 'signUp'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('admin/', admin.site.urls),
    path('', include('exchange.urls')),
    path('account/', include('account.urls')),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls', namespace='social')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = "config.views.page_not_found_view"
handler500 = "config.views.handler500"
handler403 = "config.views.handler403"