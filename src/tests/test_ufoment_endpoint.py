from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime
import requests

# Test para probar el endpoint foment_unit en cada caso posible

class FomentUnitEndpointTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_url_ufoment(self):
        # Prueba conexión con la página de unidad de fomento
        response = requests.get("https://www.sii.cl/valores_y_fechas/uf/uf2023.htm")
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Debe mostrar status 200")
        
    def test_endpoint_param_not_found(self):
        # Prueba mensaje de error si el parámetro de facha no es encontrado
        response = self.client.get(
            '/api/v1/foment_unit/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, "Debe mostrar error 404 debido a que no se especificó el parámetro")

    def test_endpoint_correct_date(self):
        # Prueba si el endpoint da el resultado esperado
        params = {
            'date': '11/12/2022'
        }
        response = self.client.get(
            '/api/v1/foment_unit/', 
            params
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Muestra si la petición fue efectuada")
        self.assertEqual("34.886,31", response.data['result'], "Muestra si la data obtenida es correcta")

    def test_endpoint_correct_another_format(self):
        # Prueba si el endpoint da el resultado esperado con un formato distinto
        params = {
            'date': '09/09-2015'
        }
        response = self.client.get(
            '/api/v1/foment_unit/', 
            params
        )
        self.assertEqual("25.223,42", response.data['result'], "Muestra si es correcto, esta vez con la fecha formato distinto")

    def test_endpoint_minimun_date(self):
        # Prueba si el endpoint da error en caso de introducir fecha menor al mínimo
        params = {
            'date': '07/10/2012'
        }
        response = self.client.get(
            '/api/v1/foment_unit/', 
            params
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, "Muestra mensaje de error debido a que la fecha es menor a la mínima")

    def test_endpoint_invalid_format(self):
        # Prueba si el endpoint da error si la fecha es inválida
        params = {
            'date': '07--/10-/-2012'
        }
        response = self.client.get(
            '/api/v1/foment_unit/', 
            params
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, "Muestra mensaje de error debido a que el formato de fecha es inválido")

    def test_endpoint_date_too_far(self):
        # Prueba si el endpoint da error si la fecha no se encuentra en registro
        today = datetime.now()
        next_year = today.replace(year=today.year + 2)
        params = {
            'date': next_year.strftime("%d-%m-%Y")
        }
        response = self.client.get(
            '/api/v1/foment_unit/', 
            params
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, "Muestra mensaje de error debido a que es una fecha mayor a la esperada")