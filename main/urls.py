from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from main.api import RefBookListView, RefBookElementListView, CheckElementView

urlpatterns = [
    path('refbooks/', RefBookListView.as_view(), name='refbook-list'),
    path('refbooks/<int:id>/elements/', RefBookElementListView.as_view(), name='refbook-elements'),
    path('refbooks/<int:id>/check_element/', CheckElementView.as_view(), name='check-element'),
]

schema_view = get_schema_view(
   openapi.Info(
      title="API проекта",
      default_version='v1',
      description="Документация для API проекта",
      terms_of_service="https://www.google.com/policies/terms/",
   ),
   public=True,
   permission_classes=[permissions.AllowAny,],
)
