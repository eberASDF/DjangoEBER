from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import ExternalServiceError, avatar_character_images, country_capital


class AvatarScenesView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(summary='Imágenes de personajes desde Last Airbender API', responses={200: dict, 503: dict})
    def get(self, request):
        try:
            images = avatar_character_images()
            return Response({'fuente': 'Last Airbender API', 'total': len(images), 'imagenes': images})
        except ExternalServiceError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class SoapCapitalView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary='Consumir SOAP público con zeep',
        parameters=[OpenApiParameter('pais', str, description='Código ISO de dos letras; por defecto MX')],
        responses={200: dict, 400: dict, 503: dict},
    )
    def get(self, request):
        country_code = request.query_params.get('pais', 'MX').strip().upper()
        if len(country_code) != 2 or not country_code.isalpha():
            return Response({'detail': 'El país debe ser un código ISO de dos letras.'}, status=400)
        try:
            capital = country_capital(country_code)
        except ExternalServiceError as exc:
            return Response({'detail': str(exc)}, status=503)
        return Response({'pais': country_code, 'capital': capital, 'servicio': 'CountryInfoService SOAP'})
