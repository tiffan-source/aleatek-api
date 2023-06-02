from django.contrib import admin
from django.urls import path, include
from .views import get_csrf_token
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from mission.views import MissionAdminViewsetAdmin, MissionActiveAdminViewsetAdmin, ITAdminViewsetAdmin, MissionActiveForCurrentAffaire, VerifyExistITForMissionSignAndCollab, VerifyExistMissionActive

from collaborateurs.views import UtilisateurConnecteView, CollaborateursAdminViewsetAdmin, AllCollabAssignToMission
from entreprise.views import ResponsableAdminViewsetAdmin, EntrepriseAdminViewsetAdmin, GetEntrepriseWithCollaborateur
from Dashbord.views import AffaireAdminViewsetAdmin, PlanAffaireAdminViewsetAdmin, ProduitAdminViewsetAdmin, \
    BatimentAdminViewsetAdmin, ChantierAdminViewsetAdmin, GetPlanAffaireDetail, EntrepriseAffaireViewsetAdmin, GetAllEntrepriseForAffaire, GetAllEntrepriseDetailForAffaire
from adresse.views import AdressdminViewsetAdmin
from ouvrage.views import AsoSerializerAdminViewsetAdmin, AffaireOuvrageAdminViewsetAdmin, OuvrageAdminViewsetAdmin, EntrepriseAffaireOuvrageViewset, GetAllAffaireOuvrageByAffaire, VerifyEntrepriseCollabOnOuvrage, AllEntreprisebAssignToAffaireOuvrage

from ouvrage.views import DocumentSerializerAdminViewsetAdmin, AvisSerializerAdminViewsetAdmin, FichierSerializerAdminViewsetAdmin, RapportVisiteSerializerAdminViewsetAdmin, VerifyExistAffaireOuvrage

from commentaire.views import CommentaireAdminViewsetAdmin

router = routers.SimpleRouter()
router.register('admin/rapport/visite', RapportVisiteSerializerAdminViewsetAdmin, basename='admin-rapport')
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

router.register('admin/batiment', BatimentAdminViewsetAdmin, basename='admin-batiment')
router.register('admin/entreprise_affaire', EntrepriseAffaireViewsetAdmin, basename='admin-entrepriseaffaire')
router.register('admin/entreprise_affaire_ouvrage', EntrepriseAffaireOuvrageViewset, basename='admin-entrepriseaffaireouvrage')
router.register('admin/chantier', ChantierAdminViewsetAdmin, basename='admin-chantier')
router.register('admin/affaire', AffaireAdminViewsetAdmin, basename='admin-affaoire')
router.register('admin/planaffaire', PlanAffaireAdminViewsetAdmin, basename='admin-paffaire')
router.register('admin/produit', ProduitAdminViewsetAdmin, basename='admin-collab')
router.register('admin/responsable', ResponsableAdminViewsetAdmin, basename='admin-collab')
router.register('admin/entreprise', EntrepriseAdminViewsetAdmin, basename='admin-entreprise')
router.register('admin/collaborateurs', CollaborateursAdminViewsetAdmin, basename='admin-collab')

urlpatterns = [

    path('api/entreprise_and_responsable/', GetEntrepriseWithCollaborateur.as_view()),
    path('api/entreprise_and_responsable/<int:id_entreprise>/', GetEntrepriseWithCollaborateur.as_view()),
    
    path('api/detail_plan_affaire/', GetPlanAffaireDetail.as_view()),
    path('api/mission_sign/<int:id_plan>/', MissionActiveForCurrentAffaire.as_view()),

    path('api/get_ouvrage_affaire/<int:id_affaire>/', GetAllAffaireOuvrageByAffaire.as_view()),

    path('api/it_mission_collab/<int:id_collab>/<int:id_mission_sign>/', VerifyExistITForMissionSignAndCollab.as_view()),
    path('api/mission_affaire/<int:id_affaire>/<int:id_mission>/', VerifyExistMissionActive.as_view()),
    
    path('api/ouvrage_affaire/<int:id_affaire>/<int:id_ouvrage>/', VerifyExistAffaireOuvrage.as_view()),

    path('api/verify_entreprise_collab_on_ouvrage/<int:id_entreprise_affaire>/<int:id_ouvrage_affaire>/', VerifyEntrepriseCollabOnOuvrage.as_view()),

    path('api/collab_for_mission_sign/<int:id_mission_sign>/', AllCollabAssignToMission.as_view()),
    path('api/entreprise_for_affaire_ouvrage/<int:id_affaire_ouvrage>/', AllEntreprisebAssignToAffaireOuvrage.as_view()),
    path('api/entreprise_collab_affaire/<int:id_affaire>/', GetAllEntrepriseForAffaire.as_view()),
    path('api/entreprise_collab_affaire_detail/<int:id_affaire>/', GetAllEntrepriseDetailForAffaire.as_view()),


    path('api/utilisateur-connecte/', UtilisateurConnecteView.as_view(), name='utilisateur_connecte'),
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
