from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import landing_page
from accounts.views import admin_dashboard, user_dashboard

urlpatterns = [
    

    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),

    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/', user_dashboard, name='user_dashboard'),

    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)