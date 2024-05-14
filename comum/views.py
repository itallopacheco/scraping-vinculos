from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from comum.serializers import ProfissionalSerializer, VinculoSerializer
from comum.models import Profissional, Vinculo
from comum.utils import buscar_vinculos

import time

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

        start_time = time.time()
        buscar_vinculos(cpf)
        elapsed_time = time.time() - start_time
        print(f"Tempo: {elapsed_time}")
        return Response(data={'tempo': elapsed_time}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def buscar_especialidade(self, request):
        cpf = request.query_params.get('cpf')
        competencia = request.query_params.get('competencia')
        cnes = request.query_params.get('cnes')

        vinculos = Vinculo.objects.filter(profissional__cpf=cpf,competencia=competencia,cnes=cnes)
        if not vinculos.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VinculoSerializer(vinculos, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

