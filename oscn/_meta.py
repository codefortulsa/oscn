import requests
import functools

from bs4 import BeautifulSoup

from . import settings

@functools.lru_cache()
def courts():
    try:
        response = requests.get('https://www.oscn.net/dockets/',
                                headers=settings.OSCN_REQUEST_HEADER,
                                verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form', action='Results.aspx')
        select = form.find('select', id='db')
        options = select.find_all('option')
        court_vals = [option['value'] for option in options]
        court_vals.remove('all')
        return court_vals
    except:
        return settings.ALL_COURTS
