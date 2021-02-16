"""rookly URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from drf_yasg2 import openapi
from drf_yasg2.views import get_schema_view
from rest_framework import permissions

from rookly.api.v1 import urls as rookly_api_v1_urls
from rookly.health.views import ping, r200
from rookly.sitemap import ServicesViewSitemap

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1.0.19",
        description="Documentation",
        terms_of_service="https://rookly.com.br/Termos",
        contact=openapi.Contact(email="contact@rookly.com.br"),
        license=openapi.License(name="GPL-3.0 License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", schema_view.with_ui("redoc")),
    path("admin/", admin.site.urls),
    path("v1/", include(rookly_api_v1_urls)),
    path(
        "sitemap.xml",
        sitemap,
        {
            "sitemaps": {
                "services": ServicesViewSitemap,
            }
        },
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("ping/", ping, name="ping"),
    path("200/", r200, name="200"),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:

    def render_template(template_name, **kwargs):
        def wrapper(request):
            from django.shortcuts import render

            return render(request, template_name, kwargs)

        return wrapper

    urlpatterns += [
        path(
            "emails/",
            include(
                [
                    path(
                        "welcome/",
                        render_template(
                            "authentication/emails/welcome.html",
                            name="Daniel",
                            base_url=settings.BASE_URL,
                        ),
                    ),
                    path(
                        "reset_password/",
                        render_template(
                            "authentication/emails/reset_password.html",
                            base_url=settings.BASE_URL,
                            responsible_name="User",
                            name="Daniel",
                        ),
                    ),
                ]
            ),
        )
    ]
