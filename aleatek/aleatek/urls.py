"""aleatek URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from .views import get_csrf_token
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from collaborateurs.views import UtilisateurConnecteView, CollaborateursAdminViewsetAdmin
from entreprise.views import ResponsableAdminViewsetAdmin, EntrepriseAdminViewsetAdmin
from Dashbord.views import AffaireAdminViewsetAdmin, PlanAffaireAdminViewsetAdmin, ProduitAdminViewsetAdmin, DestinationAdminViewsetAdmin, ChantierAdminViewsetAdmin

router = routers.SimpleRouter()
router.register('admin/destination', DestinationAdminViewsetAdmin, basename='admin-batiment')
router.register('admin/chantier', ChantierAdminViewsetAdmin, basename='admin-chantier')

router.register('admin/affaire', AffaireAdminViewsetAdmin, basename='admin-affaoire')
router.register('admin/planafaire', PlanAffaireAdminViewsetAdmin, basename='admin-paffaire')
router.register('admin/produit', ProduitAdminViewsetAdmin, basename='admin-collab')
router.register('admin/responsable', ResponsableAdminViewsetAdmin, basename='admin-collab')
router.register('admin/entreprise', EntrepriseAdminViewsetAdmin, basename='admin-entreprise')
router.register('admin/collaborateurs', CollaborateursAdminViewsetAdmin, basename='admin-collab')

urlpatterns = [
    path('utilisateur-connecte/', UtilisateurConnecteView.as_view(), name='utilisateur_connecte'),
    path('api/get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('admin/', admin.site.urls),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/users/dj-rest-auth/', include('dj_rest_auth.urls')),  # new
    path('api/users/dj-rest-auth/registration/',  # new
         include('dj_rest_auth.registration.urls')),
]
