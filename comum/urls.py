from django.urls import path,include
from comum.views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'profissionais', ProfissionalViewSet)
router.register(r'vinculos', VinculoViewSet)
urlpatterns = [

    path('', include(router.urls)),
    path('vinculos/buscar_vinculos/', VinculoViewSet.as_view({'get': 'buscar_vinculos'}),
         name='buscar_vinculos'),
    path('vinculos/buscar_especialidade/', VinculoViewSet.as_view({'get': 'buscar_especialidade'}),
         name='buscar_especialidade')
]

urlpatterns += router.urls