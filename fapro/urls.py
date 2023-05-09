
from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from src.apps.ufoment.views import FomentUnitAPI

schema_view = get_schema_view(
    openapi.Info(
        title="Prueba Técnica Fapro",
        default_version='v1',
        description="Swagger",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),

    # from django REST framework

    path('api/v1/foment_unit/', FomentUnitAPI.as_view(), name='Get Foment Unit'),
]
