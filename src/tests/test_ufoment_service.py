from django.test import TestCase
from rest_framework.test import APIClient
from src.services.scrapper import get_uf_value
from datetime import datetime

# Test para probar la función del scrapper directamente

class FomentUnitServiceTest(TestCase):

    def setUp(self):
        self.client = APIClient()
    
    def test_correct_date(self):
        # Prueba el proceso directo de pasar la fecha al método público
        self.assertEqual("24.627,10", get_uf_value('12/12/2014')['result'], "Debe mostrar el dato correcto")

    def test_minimun_date(self):
        # Prueba la fecha abajo de la mínima esperada
        self.assertEqual(False, get_uf_value('12/12/2012')['success'], "Debe mostrar error debido de fecha inválida")

    def test_invalid_date(self):
        # Prueba la fecha con un formato inválido
        self.assertEqual(False, get_uf_value('12/12-/*2012')['success'], "Debe mostrar error debido de fecha inválida")

    def test_error_date_too_far(self):
        # Prueba mensaje de error en caso de que no esté la fecha registrada aún en la página
        today = datetime.now()
        next_year = today.replace(year=today.year + 2)
        self.assertEqual(False, get_uf_value(next_year.strftime("%d-%m-%Y"))['success'], "Debe mostrar error debido de fecha inválida")