from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from key_holding.settings import SWAGGER_BASE_URL

schema_view = get_schema_view(
    openapi.Info(
        title="Key Holding Challenge API",
        default_version="v1",
        description="Key Holding Challenge Open API Documentation",
        contact=openapi.Contact(email="aabhilash3007@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    url=SWAGGER_BASE_URL,
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)
