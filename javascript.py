
import requests, logging, writerJS, re
from bs4 import BeautifulSoup, Comment
from elementos import ObjetoJS, Metodo, Campo


LOG_FILENAME = 'javadoc-parser.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.ERROR)


def limpiar(cadena):
    return " ".join(cadena.split())



# Extraer el API Core de Javascript de https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects


def imprimir_objetoJS(oJS):
    print ("-----")
    print("Objeto: " + oJS.nombre)
    print ("-----")
    print("Tipo: " + oJS.tipo)
    print ("-----")
    print("Sintaxis: ")
    for sintaxis in oJS.sintaxis:
        print("Sintaxis " + sintaxis)
    print ("-----")
    print ("Constructores: ")
    for constructor in oJS.constructores:
        print("Nombre: " + str(constructor.nombre))
        print("Sintaxis: " + str(constructor.sintaxis))
        print("Parámetros " + str(constructor.parametros))
        print("Excepciones: " + str(constructor.excepciones))
    print ("-----")
    print ("Métodos: ")
    for metodo in oJS.metodos:
        print("Nombre: " + metodo.nombre)
        print("Sintaxis: " + str(metodo.sintaxis))
        print("Parámetros " + str(metodo.parametros))
        print("Excepciones: " + str(metodo.excepciones))
    print ("-----")
    print ("Propiedades: ")
    for propiedad in oJS.propiedades:
        print("Nombre: " + str(propiedad.nombre))
        print("Sintaxis: " + str(propiedad.sintaxis))



# Recibe el contenido HTML con el metodo y el nombre del objeto
def extaer_metodo(metodo,nombre_objeto):

    # Hay que ir a cada página del método para extraer la sintaxis
    m = Metodo()
    nombre = metodo.text[0:metodo.text.find("(")]

    # Quitamos el Objeto.Prototype.
    nombre = nombre.replace(nombre_objeto+".prototype.","")

    # Casos que hay como Objeto.prototype[@@iterator](). Ya se habrá eliminado el Objeto.
    nombre = nombre.replace("prototype[","").replace("]","")

    # Quitamos el Objeto.
    nombre = nombre.replace(nombre_objeto+".","")

    # Hay casos de objetos complejos como WebAssembly.Table que tiene los métodos como Table.
    # No hacerlo para constructores nombre y nombre_objeto iguales
    if ("." in nombre_objeto) and (nombre != nombre_objeto):
        nombre = nombre.replace(nombre_objeto[nombre_objeto.find(".")+1:]+".prototype.","")
        nombre = nombre.replace(nombre_objeto[nombre_objeto.find(".")+1:],"")

    m.nombre  = nombre

    #print("Método " + m.nombre)

    enlace_metodo = metodo.find('a').get('href')

    # Algunos métodos no tienen página de explicación
    if enlace_metodo:
        pagina = requests.get(BaseURL + enlace_metodo)
        soup3 = BeautifulSoup(pagina.content, 'html.parser')
        sintaxis = soup3.find("pre", class_ = "syntaxbox notranslate")

        if not sintaxis:
            sintaxis = soup3.find("pre", class_ = "notranslate")

        # Hay algunos casos que más que sintaxis es un ejemplo y aparece como "<pre class='notranslate'>"
        if sintaxis:
            sintaxis = limpiar(sintaxis.text)
            m.add_sintaxis(sintaxis)

            # Parámetros
            parametros = sintaxis[sintaxis.find("(")+1:-1]\
                        .replace("new " + nombre_objeto,",")\
                        .replace("[","")\
                        .replace("]","")\
                        .replace("...,","")\
                        .replace(", ...","")\
                        .replace(" ","")\
                        .replace("callback","")\
                        .replace("(","")\
                        .replace(")","")\


            # Eliminamos los que tienen cuerpo { contenido }
            parametros = re.sub("{.*?}", "", parametros)

            # Extraemos los parámetros
            m.parametros = parametros.split(",")

            # Si se nos queda algún elemento vacío lo eliminamos
            m.parametros = [string for string in m.parametros if string != ""]

    return m



def extraer_objetoJS(soup2,nombre):

    # Lo primero es crear el ObjetoJS
    oJS = ObjetoJS()

    # Nombre del Objeto. Si es una función hay que quitarle el ()
    if "(" in nombre:
        oJS.nombre = nombre[0:nombre.find("(")]
    else:
        oJS.nombre = nombre

    # En el listado los objetos empiezan en mayúsucula y las funciones en minúsucla
    if nombre[0].isupper():
        oJS.tipo = "objeto"
    else:
        oJS.tipo = "funcion"

    # Sintaxis
    oJS.add_sintaxis(nombre)

    # Constructores
    contenido_constructor = soup2.find("h2", id="constructor")
    if contenido_constructor:
        constructor = contenido_constructor.find_next("div").find("dt")

        # Hay objetos como Generator que no tienen constuctor
        if constructor:
            m = extaer_metodo(constructor,nombre)
            oJS.add_constructor(m)

    contenido_metodos = soup2.find("h2", id="static_methods")
    if contenido_metodos:
        metodos = contenido_metodos.find_next("div").find_all("dt")

        for metodo in metodos:
            m = extaer_metodo(metodo,nombre)
            oJS.add_metodo(m)

    contenido_metodos = soup2.find("h2", id="instance_methods")
    if contenido_metodos:
        metodos = contenido_metodos.find_next("div").find_all("dt")

        for metodo in metodos:
            m = extaer_metodo(metodo,nombre)
            oJS.add_metodo(m)

    contenido_propiedades = soup2.find("h2", id="static_properties")
    if contenido_propiedades:
        propiedades = contenido_propiedades.find_next("div").find_all("dt")

        for propiedad in propiedades:
            p = Campo()

            # Quitams el Objeto.Prototype.
            nombre_propiedad = propiedad.text.replace(nombre+".prototype.","")

            # Quitamos el Objeto.
            nombre_propiedad = nombre_propiedad.replace(nombre+".","")

            # Hay casos Objeto.prototype[@@unscopables]. Ya le hemos quitado el Objeto
            if "[@" in nombre_propiedad:
                nombre_propiedad = nombre_propiedad.replace("prototype[","").replace("]","")

            # Hay casos get Array[@@species]
            if "get " in nombre_propiedad:
                nombre_propiedad = nombre_propiedad.replace("get " + nombre+"[","").replace("]","")

            p.nombre = nombre_propiedad
            p.add_sintaxis(propiedad.text)
            oJS.add_propiedad(p)


    contenido_propiedades = soup2.find("h2", id="instance_properties")
    if contenido_propiedades:
        propiedades = contenido_propiedades.find_next("div").find_all("dt")

        for propiedad in propiedades:
            p = Campo()

            # Quitams el Objeto.Prototype.
            nombre_propiedad = propiedad.text.replace(nombre+".prototype.","")

            # Quitamos el Objeto.
            nombre_propiedad = nombre_propiedad.replace(nombre+".","")

            # Hay casos Objeto.prototype[@@unscopables]. Ya le hemos quitado el Objeto
            if "[@" in nombre_propiedad:
                nombre_propiedad = nombre_propiedad.replace("prototype[","").replace("]","")


            # Hay casos get Array[@@species]
            if "get " in nombre_propiedad:
                nombre_propiedad = nombre_propiedad.replace("get " + nombre+"[","").replace("]","")

            p.nombre = nombre_propiedad
            p.add_sintaxis(propiedad.text)
            oJS.add_propiedad(p)

    return oJS




def todos_los_elementos():

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Vamos por el main
    main = soup.find("main")

    print("Hay " + str(len(main.find_all('a'))) + " enlaces")
    enlaces = main.find_all('a',href=True)


    for enlace in enlaces:

        if "/en-US/docs/Web/JavaScript/Reference/" in enlace['href']:


            ##if enlace.text == "BigUint64Array":
                #print (enlace.text + "-" + enlace['href'])
                #print (enlace.text)

                link = enlace.get('href')
                pagina = requests.get(BaseURL + link)
                soup2 = BeautifulSoup(pagina.content, 'html.parser')
                objetoJS = extraer_objetoJS(soup2,enlace.text)

                print("Analizando ObjetoJS: " + objetoJS.nombre)
                #imprimir_objetoJS(objetoJS)
                writerJS.doc_objeto(objetoJS)



URL = 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects'
BaseURL = 'https://developer.mozilla.org'
todos_los_elementos()


# Revisar
# 1. http://localhost:4000/Javascript/BigUint64Array/prototype[@@iterator]
