from django.urls import path, include, re_path
from .router import router
from . import views
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="StayHome",
      default_version='v1',
      description="Stayhome api",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="mellnikovaaaa@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

view_routes = [
    path('auth/register', views.RegisterView.as_view()),
    path('auth/login', views.LoginView.as_view()),
    path('auth/logout', views.LogoutView.as_view()),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns = [
    path('api/', include(router.urls + view_routes)),
]
