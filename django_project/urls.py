"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
#i18n
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

if settings.DEBUG:
    import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include('allauth.urls')),
    path("accounts/", include('accounts.urls')),
    path("", include('pages.urls')),
    #accounting
    path("books/", include('acc_books.urls')),
    path("codes/", include('acc_codes.urls')),
    path("transactions/", include('transactions.urls')),
    path("__debug__/", include('debug_toolbar.urls')),
    path("i18n/", include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path(_("accounts/"), include('allauth.urls')),
    path(_("accounts/"), include('accounts.urls')),
    path(_(""), include('pages.urls')),
    path(_("books/"), include('acc_books.urls')),
    path(_("codes/"), include('acc_codes.urls')),
    path(_("transactions/"), include('transactions.urls')),
    path(_("__debug__/"), include('debug_toolbar.urls')),
    path(_("i18n/"), include('django.conf.urls.i18n')),
)