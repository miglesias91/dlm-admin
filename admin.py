import getopt, sys
import datetime
import pytz
import json

from medios.diarios.diario import Diario

from supervisor import Supervisor
from correo import Correo

def reportar(parametros=None):
    s = Supervisor()

    tz = pytz.timezone('America/Argentina/Buenos_Aires')
    hoy = datetime.datetime.now(tz)

    diarios = Diario.leer_etiquetas('medios.yaml')
    diarios = [d for d in diarios if d not in ['casarosada', 'popular']]

    reporte = {}
    if parametros['solo_faltantes']:
        reporte = s.reportar_faltantes(hoy, diarios)
    else:
        reporte = s.reportar_noticias(hoy, diarios)

    if reporte is None:
        return

    c = Correo('config.json')
    c.enviar('visualizadordecontexto@gmail.com','✔️ Chequeo diario de la base de dicenlosmedios', json.dumps(reporte, indent=2))


def main():
    accion = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "reportar", "solo-faltantes"])
    except getopt.GetoptError as err:
        print(err)
        usage(None)
        # sys.exit(2)

    # parametros = {'medios':args, 'fecha':datetime.datetime.now().date(), 'twittear':False, 'solo_titulos':False, 'secciones':''}
    parametros = {'fecha':datetime.datetime.now(pytz.timezone('America/Argentina/Buenos_Aires')).date(), 'solo_faltantes': False}
    for o, a in opts:
        if o == "--help" or o == "-h":
            accion=usage
        elif o == "--reportar":
            accion=reportar
        elif o == "--solo-faltantes":
            parametros['solo_faltantes'] = True
        elif o == "--fecha":
            fecha = None
            if len(a.split('-')) == 2:
                desde = datetime.datetime.strptime(a.split('-')[0], "%Y%m%d")
                desde.replace(hour=0, minute=0, second=0)
                hasta = datetime.datetime.strptime(a.split('-')[1], "%Y%m%d")
                hasta.replace(hour=23, minute=59, second=59)
                fecha = {'desde':desde, 'hasta':hasta}
            else:
                fecha = datetime.datetime.strptime(a, "%Y%m%d")

            parametros['fecha'] = fecha
        else:
            assert False, "opción desconocida"
    
    # ejecuto accion con sus parametros
    accion(parametros)

def usage(parametros):
    print("dlm-lector (dicenlosmedios scrapper) v1.0")
    print("ACCIONES")
    print("--leer [MEDIO_1] [MEDIO_2] ... [MEDIO_N] - actualiza las noticias de todos los diarios, a menos que se especifiquen los MEDIOS en particular")
    print("--leer-historico - lee historico de 'casarosada': discursos desde la fecha hasta 2003")
    print("PARAMETROS OPCIONALES")
    print("--secciones s1-s2-...-sn - lee noticias de las secciones s1, s2, ..., sn: SECCIONES DISPONIBLES: 'politica', 'economia', 'sociedad', 'internacional', 'cultura', 'espectaculos', 'deportes'")
    print("--fecha AAAAMMDD - lee noticias con fecha AAAMMDD")
    print("--fecha AAAAMMDD-AAAAMMDD - lee noticias dentro del rango de fechas AAAAMMDD->AAAAMMDD")
    print("--solo-titulos - lee solo títulos")

if __name__ == "__main__":
    main()