import requests
from bs4 import BeautifulSoup
from src.core.constants import MONTHS
from datetime import datetime
import re

# Method to order the elements from data obtained

def _sort_by_date(arr):
    return [x[i] for i in range(3) for x in arr if x[i] != '']

# Method to scrap UF web

def _scrap_uf(response, month, day):
    try:
        soup = BeautifulSoup(response, "html.parser")
        month_data = soup.find("div", attrs={"id": f"mes_{MONTHS[int(month)]}", "class": "meses"})
        table = month_data.find('table', {'class':'table table-hover table-bordered'})
        rows = [[el.text.strip() for el in row.find_all("td")] for row in table.find_all("tr")[1:]]
        element = _sort_by_date(rows)[int(day)-1]
        return { 'message': 'Data obtained!', 'result': element, 'success': True }
    
    except Exception:
        return { 'message': 'Cannot obtain data from UF web', 'success': False }

# Method to validate the input date

def _validate_date(date):
    try:
        format = datetime.strptime(date.replace("/", "-" ), '%d-%m-%Y')
        if format < datetime(2013, 1, 1):
            return { 'message': 'The minimum date is 01/01/2013', 'success': False }
        
        return { 'message': 'Valid date', 'success': True}
    
    except Exception:
        return { 'message': 'Invalid date format', 'success': False }

# Public method for obtain data from scrapper

def get_uf_value(date: str):
    obj = re.split(r"/|\.|-", date)
    year, month, day = obj[2], obj[1], obj[0]
    validate_date = _validate_date(date)
    if not validate_date['success']:
        return validate_date

    response = requests.get("https://www.sii.cl/valores_y_fechas/uf/uf" + year + ".htm")
    if response.status_code != 200:
        return { 'success': False, 'status': response.status_code, 'message': 'UF web got unexpected state' }
    
    return _scrap_uf(response.content, month, day)