from django.contrib import admin
from django.urls import path, include
from main.views import index
from main.urls import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('main.urls')),
    path('', index, name='home'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
]
