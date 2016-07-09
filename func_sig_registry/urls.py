"""func_sig_registry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import (
    url,
    include,
)
from django.views.generic import TemplateView
from rest_framework import routers


from func_sig_registry.registry.views import (
    SiteIndexView,
    SignatureListView,
    SignatureCreateView,
    SolidityImportView,
)
from func_sig_registry.registry.api_views import (
    SignatureViewSet,
)


router = routers.SimpleRouter()
router.register(r'signatures', SignatureViewSet)

urlpatterns = [
    url(r'^$', SiteIndexView.as_view(), name='site-index'),
    url(r'^signatures/$', SignatureListView.as_view(), name='signature-list'),
    url(r'^submit/$', SignatureCreateView.as_view(), name='signature-create'),
    url(r'^import-solidity/$', SolidityImportView.as_view(), name='import-solidity'),
    url(
        r'^docs/$',
        TemplateView.as_view(template_name='documentation.html'),
        name='documentation',
    ),

    # API
    url(r'^api/v1/', include(router.urls, namespace='api')),
]
