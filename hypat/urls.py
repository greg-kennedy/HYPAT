"""
URL configuration for hypat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from django.conf import settings
from django.conf.urls.static import static

from debug_toolbar.toolbar import debug_toolbar_urls


from django.contrib.flatpages.views import flatpage

# from django.views.generic.base import TemplateView

urlpatterns = (
    [
        path("game/", include("hypat.games.urls")),
        path("user/", include("hypat.user_profiles.urls")),
        path("review/", include("hypat.reviews.urls")),
        path("admin/doc/", include("django.contrib.admindocs.urls")),
        path("admin/", admin.site.urls),
        path("accounts/", include("allauth.urls")),
        path("", flatpage, {"url": "/"}, name="index"),
    ]
    + debug_toolbar_urls()
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
