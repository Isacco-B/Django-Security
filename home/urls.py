from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('accounts.urls', namespace='columns')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]


admin.site.site_title = "Django Security Tutorial"
admin.site.site_header = "Django Security Tutorial"
