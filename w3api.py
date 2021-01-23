
import requests, logging, json, os
from bs4 import BeautifulSoup

__OUT__ = "/Users/victor/github/w3api_actual/"
__OUTJSON__ = "/Users/victor/github/w3api/_data/Javascript/"

def limpiar(cadena):
    return " ".join(cadena.split())


def generar_redirect():
    print("Pendiente Implementar")

def cargar_json():

    # Cargar ficheros
    directorio = os.listdir(__OUT__)

    for fichero in directorio:

        print (fichero)

        if fichero != ".DS_Store":


            try:

                with open(__OUT__ + fichero) as json_file:
                    data_json = json.load(json_file)
                    nombre = data_json["nombre"]
                    descripcion =  data_json["descripcion"]
                    codigo =  data_json["codigo"]
                    tipo = data_json["tipo"]
                    links = data_json["ldc"]


                #Si el nombre tiene punto es ún método, si no, un objeto
                if not "." in nombre:

                    # Intentamos abrir el fichero con ese nombre en W3Api
                    with open(__OUTJSON__ + nombre[0] + "/" + nombre + ".json") as json_file_w3api:
                        data_w3api_json = json.load(json_file_w3api)
                        data_w3api_json["description"] = descripcion
                        data_w3api_json["code"] = codigo
                        data_w3api_json["ldc"] = links

                    f = open(__OUTJSON__ + nombre[0] + "/" + nombre + ".json","w")
                    f.write(json.dumps(data_w3api_json,indent=4))
                    f.close()

                else:

                    metodo = nombre[nombre.find(".")+1:]
                    nombre = nombre[:nombre.find(".")]

                    # Intentamos abrir el fichero con ese nombre en W3Api
                    with open(__OUTJSON__ + nombre[0] + "/" + nombre + ".json") as json_file_w3api:
                        data_w3api_json = json.load(json_file_w3api)
                        metodos = data_w3api_json[tipo]
                        x = 0
                        for m in metodos:
                            if m["nombre"] == metodo:
                                m["description"] = descripcion
                                m["code"] = codigo
                                m["ldc"] = links
                                data_w3api_json["metodos"][x] = m
                            x= x+1

                    f = open(__OUTJSON__ + nombre[0] + "/" + nombre + ".json","w")
                    f.write(json.dumps(data_w3api_json,indent=4))
                    f.close()

            except EnvironmentError:
                print ("Fichero >>" + fichero + "<< no encontrado")


def generar_json():

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Vamos por el main
    main = soup.find("div",class_="mw-content-ltr")

    print("Hay " + str(len(main.find_all('a'))) + " enlaces")
    enlaces = main.find_all('a',href=True)

    for enlace in enlaces:

            codigo = ""
            descripcion = ""
            links = []

            print (enlace.text)
            page2 = requests.get(BaseURL + enlace.get("href"))
            soup2 = BeautifulSoup(page2.content, 'html.parser')

            ejemplo = soup2.find("span",id="Ejemplo")
            if ejemplo:
                pre = ejemplo.find_next("pre")
                if pre:
                    codigo = pre.text

            texto_descripcion = soup2.find("span",id="Descripci.C3.B3n")
            if texto_descripcion:
                p = texto_descripcion.find_next("p")
                if p:
                    descripcion = p.text

            contenido = soup2.find("div",id="bodyContent")
            if contenido:
                aes = contenido.find_all("a")
                if aes:
                    for a in aes:
                        if a.has_attr("href"):
                            if "lineadecodigo.com" in a["href"]:
                                e = {}
                                e["nombre"] = a.text
                                e["url"] = a["href"]
                                links.append(e)

            if descripcion!="" or codigo!="" or len(links) > 0:

                # Tipo si es un método, constructor o propiedad
                tipo = enlace.text[enlace.text.find(":")+1:]
                nombre = enlace.text[enlace.text.find(":")+1:].replace("(","").replace(")","")
                data_json = {}

                if not "(" in tipo:
                    data_json["tipo"] = "propiedades"
                else:
                    if tipo[:tipo.find(".")] == tipo[tipo.find(".")+1:]:
                        data_json["tipo"] = "constructores"
                    else:
                        data_json["tipo"] = "metodos"


                data_json["nombre"] = nombre
                data_json["codigo"] = codigo
                data_json["descripcion"] = descripcion
                data_json["ldc"] = links

                f = open(__OUT__ + nombre + ".json","w")

                f.write(json.dumps(data_json,indent=4))
                f.close()





URL = 'http://w3api.com/wiki/Categor%C3%ADa:JavaScript'
BaseURL = 'http://w3api.com/'
#generar_json()
cargar_json()




