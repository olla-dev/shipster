"""shipster backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers
from vessels import views as vessel_views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from core.settings import MEDIA_URL, MEDIA_ROOT


router = routers.SimpleRouter(trailing_slash=True)
router.register('vessels', vessel_views.VesselView, 'vessel-list')
locations_router = routers.NestedSimpleRouter(router, r'vessels', lookup='vessel')
locations_router.register(r'locations', vessel_views.LocationView, basename='vessel-locations')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include(locations_router.urls)),
    path('api/v1/vessels/csv', vessel_views.VesselCsvView.as_view()),
    path('api/v1/vessels/geo', vessel_views.VesselGeoView.as_view()),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
