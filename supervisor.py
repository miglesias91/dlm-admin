
import datetime
import pytz
from bd.kioscomongo import Kiosco

class Supervisor():
    def __init__(self):
        pass

    def reportar_noticias(self, fecha, medios, secciones=None):
        kiosco = Kiosco('conexiones.json')

        reporte = {}
        for medio in medios:
            cantidad = kiosco.contar_noticias(fecha, medio)
            reporte[medio] = cantidad

        if len(reporte) is 0:
            reporte = None
            
        return reporte

    def reportar_faltantes(self, fecha, medios, secciones=None):
        kiosco = Kiosco('conexiones.json')

        reporte = {}
        for medio in medios:
            cantidad = kiosco.contar_noticias(fecha, medio)
            if cantidad is 0:
                reporte[medio] = cantidad

        if len(reporte) is 0:
            reporte = None
            
        return reporte