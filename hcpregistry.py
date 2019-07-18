# Script for HCP registry validation on Superintendencia de salud (Chile Local Authority)
# for Health Care professionals registration (This Registry does not include midwives)

import requests
from bs4 import BeautifulSoup
import pandas as pd


class HcpRegistry:
    """ A class for HCP Registry validation from Chile local authority"""

    def __init__(self, rut="", nombre=""):
        self.rut = rut
        self.nombre = nombre
        self.titulo = ""
        self.institucion_habilitante = ""
        self.especialidad = ""
        self.valid_registry = False

    """ Check online database to see if hcp registry exists """

    def check_registry(self):
        """ 
        Check online for HCP validation using their unique identifier (self.rut)

        """
        base_url = "http://webserver.superdesalud.gob.cl/bases/prestadoresindividuales.nsf/(searchAll2)/Search?SearchView&Query="
        search_type = "SearchView"
        Start = "1"
        count = "10"
        rut_pres = self.rut

        query_url = base_url + "(FIELD rut_pres="+rut_pres+")" + \
            "&Start="+Start+"&count="+count
        print("Connecting to URL: %s" % query_url)

        response = requests.get(query_url)
        if response.status_code == 200:
            print('Successfully connected to Superintendencia de salud database!')
        elif response.status_code == 404:
            print('Could not connect to Superintencia de salud database at ' + query_url)
            return False
        soup = BeautifulSoup(response.content, 'html.parser',
                             from_encoding="latin-1")
        # Grab the first table of the response
        table = soup.find_all('table')[0]
        row_marker = 0
        for row in table.find_all('tr'):
            # print(row)
            columns = row.find_all('td')
            if row_marker == 1:
                self.nombre = columns[0].a.contents[0].encode('latin-1')
                self.especialidad = columns[2].contents[0]
                self.institucion_habilitante = columns[3].contents
                self.valid_registry = True
            row_marker += 1
        return True
