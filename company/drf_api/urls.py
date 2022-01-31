from django.urls import include, path
from rest_framework import routers
from drf_api import views
from rest_framework_jwt.views import obtain_jwt_token

from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()



router.register(r'departament-legal-entity', views.DepartmentLegalEntityRefViewSet)
router.register(r'departament-client', views.DepartmentClientRefViewSet)
router.register(r'social-network', views.SocialNetworksViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'legal-entity', views.LegalEntityViewSet)
router.register(r'departament', views.DepartmentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/',     include('djoser.urls.authtoken')),
    path('api-token-auth/', obtain_jwt_token),
    path('api-auth/', include('rest_framework.urls')),
]