from django.contrib import admin
from django.urls import path, include
from .views import get_csrf_token
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from mission.views import MissionAdminViewsetAdmin, MissionActiveAdminViewsetAdmin, ITAdminViewsetAdmin

from collaborateurs.views import UtilisateurConnecteView, CollaborateursAdminViewsetAdmin
from entreprise.views import ResponsableAdminViewsetAdmin, EntrepriseAdminViewsetAdmin, GetEntrepriseWithCollaborateur
from Dashbord.views import AffaireAdminViewsetAdmin, PlanAffaireAdminViewsetAdmin, ProduitAdminViewsetAdmin, \
    DestinationAdminViewsetAdmin, ChantierAdminViewsetAdmin
from adresse.views import AdressdminViewsetAdmin
from ouvrage.views import AsoSerializerAdminViewsetAdmin, AffaireOuvrageAdminViewsetAdmin, OuvrageAdminViewsetAdmin

from ouvrage.views import DocumentSerializerAdminViewsetAdmin, AvisSerializerAdminViewsetAdmin, FichierSerializerAdminViewsetAdmin

from commentaire.views import CommentaireAdminViewsetAdmin

router = routers.SimpleRouter()
router.register('admin/commentaire', CommentaireAdminViewsetAdmin, basename='admin=commentaire')
router.register('admin/fichierattacher', FichierSerializerAdminViewsetAdmin, basename='admin=avis')
router.register('admin/avis', AvisSerializerAdminViewsetAdmin, basename='admin=avis')
router.register('admin/documents', DocumentSerializerAdminViewsetAdmin, basename='admin=document')
router.register('admin/ouvrage', OuvrageAdminViewsetAdmin, basename='admin=ouvrage')
router.register('admin/affaireouvrage', AffaireOuvrageAdminViewsetAdmin, basename='admin=aafffaireouvrage')
router.register('admin/aso', AsoSerializerAdminViewsetAdmin, basename='admin=aso')
router.register('admin/mission', MissionAdminViewsetAdmin, basename='admin-mission')
router.register('admin/missions/active', MissionActiveAdminViewsetAdmin, basename='admin-mission-active')
router.register('admin/intervention/technique', ITAdminViewsetAdmin, basename='admin-it')

router.register('admin/adresse', AdressdminViewsetAdmin, basename='admin-adresse')

router.register('admin/destination', DestinationAdminViewsetAdmin, basename='admin-batiment')
router.register('admin/chantier', ChantierAdminViewsetAdmin, basename='admin-chantier')
router.register('admin/affaire', AffaireAdminViewsetAdmin, basename='admin-affaoire')
router.register('admin/planaffaire', PlanAffaireAdminViewsetAdmin, basename='admin-paffaire')
router.register('admin/produit', ProduitAdminViewsetAdmin, basename='admin-collab')
router.register('admin/responsable', ResponsableAdminViewsetAdmin, basename='admin-collab')
router.register('admin/entreprise', EntrepriseAdminViewsetAdmin, basename='admin-entreprise')
router.register('admin/collaborateurs', CollaborateursAdminViewsetAdmin, basename='admin-collab')

urlpatterns = [

    path('api/entreprise_and_responsable/', GetEntrepriseWithCollaborateur.as_view()),


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
