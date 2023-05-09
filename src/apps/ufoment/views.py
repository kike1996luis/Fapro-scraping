from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi
from rest_framework.views import APIView
from src.services.scrapper import get_uf_value


class FomentUnitAPI(APIView):

    param = openapi.Parameter('date', openapi.IN_QUERY,
                              description="Fecha para hacer la consulta de unidad de fomento",type=openapi.FORMAT_DATE,)

    @swagger_auto_schema(
        operation_description="Endpoint al que se le pasa una fecha y se obtiene el registro de unidad de fomento en la fecha dada",
        manual_parameters=[param]
    )
    def get(self, request):
        if "date" in self.request.GET:
            resp = get_uf_value(self.request.GET.get('date'))
            if resp['success']:
                return Response(resp, status=status.HTTP_200_OK)

            return Response(resp, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "success": False, 
                "message": "Param not found!"
            }, status=status.HTTP_404_NOT_FOUND
        )