from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from comum.serializers import ProfissionalSerializer, VinculoSerializer
from comum.models import Profissional, Vinculo
from comum.utils import buscar_vinculos


class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get']


class VinculoViewSet(viewsets.ModelViewSet):
    queryset = Vinculo.objects.all()
    serializer_class = VinculoSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get']

    @action(detail=False, methods=['get'])
    def buscar_vinculos(self, request):
        cpf = request.query_params.get('cpf')

        # Chama a função buscar_vinculos e obtém o resultado
        buscar_vinculos(cpf)
        vinculos = Vinculo.objects.filter(profissional__cpf=cpf)
        serializer = VinculoSerializer(vinculos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
