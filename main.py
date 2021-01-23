'''
 Código que realiza el parseo de la documentación de Java para generar el contenido de W3Api
 Se basa de partida en todas las clases Java que existen. https://docs.oracle.com/javase/7/docs/api/allclasses-frame.html
'''

import requests, logging, writer
from bs4 import BeautifulSoup, Comment
from elementos import Clase, Metodo, Enumerado, Campo, Elemento

LOG_FILENAME = 'javadoc-parser.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.ERROR)


def limpiar(cadena):
    # En algunos casos aparece el caracter \u200b para no romper la línea en los estilos. Se elimina
    cadena = cadena.replace("\u200b","")
    return " ".join(cadena.split())

def adaptar_version(version):

    # Valores de Versión

    # 1.0 a 1.8 -> Lo convertimos a Java 1.x
    # 9 -> Lo convertimos a Java 9
    # 1.8u40 -> Lo convertimos a Java 1.8
    # JAXB 1.0
    # DOM Level 2
    # JavaFX 8u40 -> Lo convertimos a JavaFX 8.0
    # JavaFX 2.0
    # JAX-WS 2.1
    # J2SE 1.5 -> Lo convertimos a Java 1.5
    # JAX-WS 2.2
    # JavaFX 8.0
    # JDK1.2 -> Lo convertimos a Java 1.2

    if "1.0" in version:
        version = version.replace("1.0","Java 1.0")
    if "1.1" in version:
        version = version.replace("1.1","Java 1.1")
    if "JSK1.2" in version:
        version = version.replace("JDK1.2","Java 1.2")
    else:
            if "1.2" in version:
                version = version.replace("1.2","Java 1.2")
    if "1.3" in version:
        version = version.replace("1.3","Java 1.3")
    if "1.4" in version:
        version = version.replace("1.4","Java 1.4")
    if "J2SE 1.5" in version:
        version = version.replace("J2SE 1.5","Java 1.5")
    else:
        if "1.5" in version:
            version = version.replace("1.5","Java 1.5")
    if "1.6" in version:
        version = version.replace("1.6","Java 1.6")
    if "1.7" in version:
        version = version.replace("1.7","Java 1.7")
    if "1.8u40" in version:
        version = version.replace("1.8u40","Java 1.8")
    else:
        if "1.8" in version:
            version = version.replace("1.8","Java 1.8")
    if "9" in version:
        version = version.replace("9","Java 9")

    if "JavaFX 8u40" in version:
        version = version.replace("JavaFX 8u40","JavaFX 8.0")

    return version


def detalle_signatura(detalle,signatura):
    # Buscamos por todos los pre
    metodos = detalle.find_all("pre")

    for metodo in metodos:
        if signatura in limpiar(metodo.text):
            return limpiar(metodo.text)

    logging.log(logging.ERROR,"Signatura " + signatura + " no encontrada en detalle")
    # Devuelve la original
    return signatura

# Busca lo que hay en el campo Throws
def detalle_excecpiones(detalle,signatura):

    # Buscamos por todos los pre
    metodos = detalle.find_all("pre")

    excepciones = []

    for metodo in metodos:
        if signatura in limpiar(metodo.text):
            tag_throw = metodo.find_next("dl")
            if tag_throw:
                tag_span = tag_throw.find("span", class_="throwsLabel")
                if tag_span:
                    tag_dds = tag_span.find_previous("dt").find_next_siblings("dd")
                    for tag_dd in tag_dds:
                        ## Las excecpiones van en dd seguidos, si hay un dt antes ya no vale
                        ## De momento chequeamos que lleve la palabara "Exception"
                        e = tag_dd.find("code")
                        if e:
                            if "Exception" in e.text:
                                excepciones.append(e.text)
                    return excepciones

    logging.log(logging.ERROR,"Signatura " + signatura + " no encontrada en detalle")
    return []


def obtener_sintaxis_enumerado(detalle,signatura):

    enumerados = detalle.find_all("pre")
    for enumerado in enumerados:
        if signatura in limpiar(enumerado.text):
            return limpiar(enumerado.text)

    logging.log(logging.ERROR,"Signatura " + signatura + " para el Enumerado")
    return ""



def imprimir_clase(c):
    print ("-----")
    print("Clase: " + c.nombre)
    print ("-----")
    print("Paquete: " + c.paquete)
    print ("-----")
    print("Modulo: " + c.modulo)
    print ("-----")
    print("Tipo: " + c.tipo)
    print ("-----")
    print("Versión: " + c.version)
    print ("-----")
    print("Sintaxis: ")
    for sintaxis in c.sintaxis:
        print("Sintaxis " + sintaxis)
    print ("-----")
    print ("Campos: ")
    for campo in c.campos:
        print("Nombre: " + str(campo.nombre))
        print("Sintaxis " + str(campo.sintaxis))
    print ("-----")
    print ("Enumerados: ")
    for enumerado in c.enumerados:
        print("Nombre: " + str(enumerado.nombre))
        print("Sintaxis " + str(enumerado.sintaxis))
    print ("-----")
    print ("Constructores: ")
    for constructor in c.constructores:
        print("Nombre: " + str(constructor.nombre))
        print("Sintaxis: " + str(constructor.sintaxis))
        print("Parámetros " + str(constructor.parametros))
        print("Excepciones: " + str(constructor.excepciones))
    print ("-----")
    print ("Métodos: ")
    for metodo in c.metodos:
        print("Nombre: " + str(metodo.nombre))
        print("Sintaxis: " + str(metodo.sintaxis))
        print("Parámetros " + str(metodo.parametros))
        print("Excepciones: " + str(metodo.excepciones))

def extraer_clase_v10(soup2):
    # Lo primero es crear la clase
    c1 = Clase()

    # Nombre de la Clase
    nombre = soup2.find("h2", class_="title")

    # Eliminamos si hay campos de tipo <>
    if nombre.text.find("<") > 0:
        nombre = nombre.text[:nombre.text.find("<")]
    else:
        nombre = nombre.text

    # Tipo de clase (Class o Interface)
    if "Class " in nombre:
        c1.nombre = nombre.replace('Class ','')
        c1.tipo = "clase"
    else:
        if "Interface " in nombre:
            c1.nombre = nombre.replace('Interface ','')
            c1.tipo = "interface"
        else:
            if "Enum " in nombre:
                c1.nombre = nombre.replace('Enum ','')
                c1.tipo = "enumerado"
            else:
                if "Annotation Type " in nombre:
                    c1.nombre = nombre.replace('Annotation Type ','')
                    c1.tipo = "anotacion"
                else:
                    if "Annotation" in nombre:
                        c1.nombre = nombre.replace('Annotation ','')
                        c1.tipo = "anotacion"

    # Paquete y Módulo
    paquete_modulo = soup2.find_all("div", class_="subTitle")
    c1.modulo = paquete_modulo[0].text[7:]
    c1.paquete = paquete_modulo[1].text[8:]

    # Sintaxis

    # De la clase "Description" obtenemos
    # en un pre la sintaxis de la clase
    # de un dl > dd la versión desde la que está disponible

    descripcion = soup2.find("div", class_="description")
    sintaxis = descripcion.find("pre")
    c1.add_sintaxis(limpiar(sintaxis.text))

    ## Versión
    # Hay un texto que pone "Since" que está en un span con clase "simpleTagLabel". Ojo que hay más de una!!

    etiquetas_version = descripcion.find_all("span",class_="simpleTagLabel")

    for etiqueta_version in etiquetas_version:

        if ((etiqueta_version) and (etiqueta_version.text == "Since:")):
            numero_version = etiqueta_version.find_previous("dt").find_next_sibling("dd")
            version = numero_version.text
            break

    if not 'version' in locals():
        version = "1.0"

    c1.version = adaptar_version(version)

    ## Campos
    # La primera tabla tiene los campos
    # En la tabla buscamos los td
    # De cada td el primer code es el que tiene el modificador o nombre del campo
    # Ya que hay td que tienen varios code. Nos vale el primero

    resumen_campos = soup2.find("a", id="field.summary")

    if resumen_campos:
        tabla_campos = resumen_campos.find_next_sibling("table")

        if tabla_campos:

            modificadores = []

            for col1 in tabla_campos.find_all("td",class_="colFirst"):
                modificadores.append(col1.find("code").text)

            x = 0
            for col2 in tabla_campos.find_all("th",class_="colSecond",scope="row"):
                codigo_campos = col2.find("code")

                nombre = limpiar(codigo_campos.text)
                sintaxis = modificadores[x] + " " + nombre

                c = Campo()
                c.nombre = nombre
                c.add_sintaxis(sintaxis)

                c1.add_campo(c)
                x = x+1

    ## Enumerados
    resumen_enumerados = soup2.find("a", id="enum.constant.summary")

    if resumen_enumerados:
        tabla_enumerados = resumen_enumerados.find_next_sibling("table")

        if tabla_enumerados:

            for col in tabla_enumerados.find_all("th",class_="colFirst",scope="row"):
                codigo_metodos = col.find("code")

                detalle = soup2.find("div", class_="details")


                sintaxis_inicial = limpiar(codigo_metodos.text)
                sintaxis = detalle_signatura(detalle,sintaxis_inicial)

                nombre = sintaxis_inicial

                en1 = Enumerado()
                en1.nombre = nombre
                en1.add_sintaxis(sintaxis)

                c1.add_enumerado(en1)


    ## Elementos
    # Las anotaciones tienen elementos opcionales que se le pueden pasar a la anotación

    resumen_elementos = soup2.find("a", id="annotation.type.optional.element.summary")

    if resumen_elementos:
        tabla_elementos = resumen_elementos.find_next_sibling("table")

        if tabla_elementos:

            modificadores = []

            for col1 in tabla_elementos.find_all("td",class_="colFirst"):
                modificadores.append(col1.find("code").text)

            x = 0
            for col2 in tabla_elementos.find_all("th",class_="colSecond",scope="row"):
                codigo_elementos = col2.find("code")

                nombre = limpiar(codigo_elementos.text)
                sintaxis = modificadores[x] + " " + nombre

                e = Elemento()
                e.nombre = nombre
                e.add_sintaxis(sintaxis)

                c1.add_elemento(e)
                x = x+1


    ## Constructores
    # Hay una tabla donde los th son de la class colConstructorName
    # En el code está el constructor

    thconstructores = soup2.find_all("th", class_="colConstructorName")
    if (thconstructores):

        cs = Metodo()
        for thconstructor in thconstructores:

            constructor = thconstructor.find("code").text

            cs_nombre = c1.nombre # Constructor mismo nombre que la clase
            cs_sintaxis_inicial = limpiar(constructor)
            cs_parametros = cs_sintaxis_inicial[cs_sintaxis_inicial.find("(")+1:-1].split(",")

            detalle = soup2.find("div", class_="details")
            cs_sintaxis = detalle_signatura(detalle,cs_sintaxis_inicial)
            cs_excepciones = detalle_excecpiones(detalle,cs_sintaxis_inicial)


            cs.nombre = cs_nombre
            cs.add_sintaxis(cs_sintaxis)
            if ((cs_parametros) and (cs_parametros[0]!="")):
                for parametro in cs_parametros:
                    cs.add_parametros(limpiar(parametro))

            if ((cs_excepciones) and (cs_excepciones[0]!="")):
                for e in cs_excepciones:
                    cs.add_excepciones(limpiar(e))


        c1.add_constructor(cs)

    ## Métodos
    # Hay una tabla resumen a la que llegamos mediante el id "Method Summary"
    # La tabla es de tres columnas, nos interesa la primera y segunda. ya que son modificador y signatura
    # Navegamos por code ya que es lo más representativo

    resumen_metodos = soup2.find("a", id="method.summary")

    if resumen_metodos:
        tabla_metodos = resumen_metodos.find_next_sibling("table")

        if tabla_metodos:

            modificadores = []

            for col1 in tabla_metodos.find_all("td",class_="colFirst"):
                modificadores.append(col1.find("code").text)

            x = 0
            metodo_temporal = ""

            for col2 in tabla_metodos.find_all("th",class_="colSecond",scope="row"):
                codigo_metodos = col2.find("code")

                detalle = soup2.find("div", class_="details")

                nombre_parametros = limpiar(codigo_metodos.text)
                sintaxis_inicial = modificadores[x] + " " + nombre_parametros
                sintaxis = detalle_signatura(detalle,sintaxis_inicial)
                nombre = nombre_parametros[0:nombre_parametros.find("(")]
                parametros = nombre_parametros[nombre_parametros.find("(")+1:-1].split(",")
                excepciones = detalle_excecpiones(detalle,sintaxis_inicial)


                if metodo_temporal != nombre:

                    if metodo_temporal != "":
                        c1.add_metodo(m1)

                    m1 = Metodo()
                    m1.nombre = nombre
                    m1.add_sintaxis(sintaxis)

                    if ((parametros) and (parametros[0]!="")):
                        for p in parametros:
                            m1.add_parametros(limpiar(p))

                    if ((excepciones) and (excepciones[0]!="")):
                        for e in excepciones:
                            m1.add_excepciones(limpiar(e))
                else:

                    m1.add_sintaxis(sintaxis)

                    if ((parametros) and (parametros[0]!="")):
                        for p in parametros:
                            m1.add_parametros(limpiar(p))

                    if ((excepciones) and (excepciones[0]!="")):
                        for e in excepciones:
                            m1.add_excepciones(limpiar(e))


                metodo_temporal = nombre
                x = x+1

            c1.add_metodo(m1)

    return c1



# Analiza todas las clases
# Genera los ficheros de dicha clase
# Si la clase está repetida hay que crearlo con el paquete y crear el desambigüador

def todas_las_clases():

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    print("Hay " + str(len(soup.find_all('a'))) + " clases")
    enlaces = soup.find_all('a')

    # Clase anterior a la analizada
    clase_anterior = Clase()
    clase_anterior.nombre = ""

    # Estoy en secuencia de clase iguales
    secuencia = False

    # Lista y nombre de Clases a Desambiguar
    nombre_desambiguar = ""
    lista_desambiguar = []

    versiones = set()


    for enlace in enlaces:



        link = BaseURL + enlace.get('href')
        pagina = requests.get(link)
        soup2 = BeautifulSoup(pagina.content, 'html.parser')
        clase = extraer_clase_v10(soup2)

        print("Analizando Clase: " + clase.nombre + " .Clase Anterior: " + clase_anterior.nombre)
        versiones.add(clase.version)

        # Evito volcar la vacía
        if clase_anterior.nombre != "":

            # Ojo que hay clases como Runtime y RunTime que cambian las mayúsculas
            # Por lo que para la comparación se pasan a mayúsuclas
            if (clase_anterior.nombre.upper() != clase.nombre.upper()):

                # Las clases consecutivas son diferentes
                # Si estoy en secuencia hay que realizar la sustitución
                # Generar la clase de desambiguación
                # Y romper la secuencia

                if secuencia:
                    writer.doc_clase(clase_anterior,True)
                    lista_desambiguar.append(clase_anterior)
                    writer.doc_desambiguar(nombre_desambiguar,lista_desambiguar)
                else:
                    writer.doc_clase(clase_anterior,False)

                secuencia = False
                lista_desambiguar = []
                nombre_desambiguar = ""
            else:
                # Las clases consecutivas son iguales
                # Hay que cambiarle el nombre
                nombre_desambiguar = clase_anterior.nombre
                lista_desambiguar.append(clase_anterior)
                writer.doc_clase(clase_anterior,True)
                secuencia = True

        clase_anterior = clase

    # Imprimo la última
    writer.doc_clase(clase_anterior,False)

    print("----Versiones-----")
    for v in versiones:
        print (v)



# Analiza por nombre de clase
# REVISAR, NO FUNCIONA
def una_clase(nombre_clase):

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    enlaces = soup.find_all('a')

    for enlace in enlaces:
        if (enlace.text == nombre_clase):
            break

    link = BaseURL + enlace.get('href')
    pagina = requests.get(link)
    soup2 = BeautifulSoup(pagina.content, 'html.parser')
    clase = extraer_clase_v10(soup2)
    imprimir_clase(clase)
    writer.doc_clase(clase,False)




print("Inicio del proceso de parsing")
URL = 'https://docs.oracle.com/javase/10/docs/api/allclasses-frame.html'
BaseURL = 'https://docs.oracle.com/javase/10/docs/api/'




# >> Cuidado con las duplicadas no usarlo
una_clase("RuntimeOperations")



#Action
#AbstractRegionPainter.PaintContext.CacheMode
#ModuleReader
#JAXBContext
#SecureRandomSpi


#todas_las_clases()


# ToDo
# Elementos deprecados como Interface ClassDoc
# Listar todas las versiones

#----
# Revisar el
# Nombre: createBinder
# Sintaxis: public static final String JAXB_CONTEXT_FACTORY


# Clases de Ejemplo
# Clases con campos

# Clase con Elementos
# BeanProperty

# Clase con Enumerados es también un Enum
# ClientInfoStatus

# Interface
# ClassDeclarationTree

# Annotation Type
# Action



modulos = ["java.activation",
"java.base",
"java.compiler",
"java.corba",
"java.datatransfer",
"java.desktop",
"java.instrument",
"java.jnlp",
"java.logging",
"java.management",
"java.management.rmi",
"java.naming",
"java.prefs",
"java.rmi",
"java.scripting",
"java.se",
"java.se.ee",
"java.security.jgss",
"java.security.sasl",
"java.smartcardio",
"java.sql",
"java.sql.rowset",
"java.transaction",
"java.xml",
"java.xml.bind",
"java.xml.crypto",
"java.xml.ws",
"java.xml.ws.annotation",
"javafx.base",
"javafx.controls",
"javafx.fxml",
"javafx.graphics",
"javafx.media",
"javafx.swing",
"javafx.web",
"jdk.accessibility",
"jdk.attach",
"jdk.charsets",
"jdk.compiler",
"jdk.crypto.cryptoki",
"jdk.crypto.ec",
"jdk.dynalink",
"jdk.editpad",
"jdk.hotspot.agent",
"jdk.httpserver",
"jdk.incubator.httpclient",
"jdk.jartool",
"jdk.javadoc",
"jdk.jcmd",
"jdk.jconsole",
"jdk.jdeps",
"jdk.jdi",
"jdk.jdwp.agent",
"jdk.jfr",
"jdk.jlink",
"jdk.jshell",
"jdk.jsobject",
"jdk.jstatd",
"jdk.localedata",
"jdk.management",
"jdk.management.agent",
"jdk.management.cmm",
"jdk.management.jfr",
"jdk.management.resource",
"jdk.naming.dns",
"jdk.naming.rmi",
"jdk.net",
"jdk.pack",
"jdk.packager.services",
"jdk.rmic",
"jdk.scripting.nashorn",
"jdk.sctp",
"jdk.security.auth",
"jdk.security.jgss",
"jdk.snmp",
"jdk.xml.dom",
"jdk.zipfs"]

#writer.doc_tags(modulos,"modulo","Módulo")

paquetes = ["com.sun.jarsigner",
"com.sun.java.accessibility.util",
"com.sun.javadoc",
"com.sun.jdi",
"com.sun.jdi.connect",
"com.sun.jdi.connect.spi",
"com.sun.jdi.event",
"com.sun.jdi.request",
"com.sun.management",
"com.sun.net.httpserver",
"com.sun.net.httpserver.spi",
"com.sun.nio.sctp",
"com.sun.security.auth",
"com.sun.security.auth.callback",
"com.sun.security.auth.login",
"com.sun.security.auth.module",
"com.sun.security.jgss",
"com.sun.source.doctree",
"com.sun.source.tree",
"com.sun.source.util",
"com.sun.tools.attach",
"com.sun.tools.attach.spi",
"com.sun.tools.javac",
"com.sun.tools.javadoc",
"com.sun.tools.jconsole",
"java.applet",
"java.awt",
"java.awt.color",
"java.awt.datatransfer",
"java.awt.desktop",
"java.awt.dnd",
"java.awt.event",
"java.awt.font",
"java.awt.geom",
"java.awt.im",
"java.awt.im.spi",
"java.awt.image",
"java.awt.image.renderable",
"java.awt.print",
"java.beans",
"java.beans.beancontext",
"java.io",
"java.lang",
"java.lang.annotation",
"java.lang.instrument",
"java.lang.invoke",
"java.lang.management",
"java.lang.module",
"java.lang.ref",
"java.lang.reflect",
"java.math",
"java.net",
"java.net.spi",
"java.nio",
"java.nio.channels",
"java.nio.channels.spi",
"java.nio.charset",
"java.nio.charset.spi",
"java.nio.file",
"java.nio.file.attribute",
"java.nio.file.spi",
"java.rmi",
"java.rmi.activation",
"java.rmi.dgc",
"java.rmi.registry",
"java.rmi.server",
"java.security",
"java.security.acl",
"java.security.cert",
"java.security.interfaces",
"java.security.spec",
"java.sql",
"java.text",
"java.text.spi",
"java.time",
"java.time.chrono",
"java.time.format",
"java.time.temporal",
"java.time.zone",
"java.util",
"java.util.concurrent",
"java.util.concurrent.atomic",
"java.util.concurrent.locks",
"java.util.function",
"java.util.jar",
"java.util.logging",
"java.util.prefs",
"java.util.regex",
"java.util.spi",
"java.util.stream",
"java.util.zip",
"javafx.animation",
"javafx.application",
"javafx.beans",
"javafx.beans.binding",
"javafx.beans.property",
"javafx.beans.property.adapter",
"javafx.beans.value",
"javafx.collections",
"javafx.collections.transformation",
"javafx.concurrent",
"javafx.css",
"javafx.css.converter",
"javafx.embed.swing",
"javafx.event",
"javafx.fxml",
"javafx.geometry",
"javafx.print",
"javafx.scene",
"javafx.scene.canvas",
"javafx.scene.chart",
"javafx.scene.control",
"javafx.scene.control.cell",
"javafx.scene.control.skin",
"javafx.scene.effect",
"javafx.scene.image",
"javafx.scene.input",
"javafx.scene.layout",
"javafx.scene.media",
"javafx.scene.paint",
"javafx.scene.shape",
"javafx.scene.text",
"javafx.scene.transform",
"javafx.scene.web",
"javafx.stage",
"javafx.util",
"javafx.util.converter",
"javax.accessibility",
"javax.activation",
"javax.activity",
"javax.annotation",
"javax.annotation.processing",
"javax.crypto",
"javax.crypto.interfaces",
"javax.crypto.spec",
"javax.imageio",
"javax.imageio.event",
"javax.imageio.metadata",
"javax.imageio.plugins.bmp",
"javax.imageio.plugins.jpeg",
"javax.imageio.plugins.tiff",
"javax.imageio.spi",
"javax.imageio.stream",
"javax.jnlp",
"javax.jws",
"javax.jws.soap",
"javax.lang.model",
"javax.lang.model.element",
"javax.lang.model.type",
"javax.lang.model.util",
"javax.management",
"javax.management.loading",
"javax.management.modelmbean",
"javax.management.monitor",
"javax.management.openmbean",
"javax.management.relation",
"javax.management.remote",
"javax.management.remote.rmi",
"javax.management.timer",
"javax.naming",
"javax.naming.directory",
"javax.naming.event",
"javax.naming.ldap",
"javax.naming.spi",
"javax.net",
"javax.net.ssl",
"javax.print",
"javax.print.attribute",
"javax.print.attribute.standard",
"javax.print.event",
"javax.rmi",
"javax.rmi.CORBA",
"javax.rmi.ssl",
"javax.script",
"javax.security.auth",
"javax.security.auth.callback",
"javax.security.auth.kerberos",
"javax.security.auth.login",
"javax.security.auth.spi",
"javax.security.auth.x500",
"javax.security.cert",
"javax.security.sasl",
"javax.smartcardio",
"javax.sound.midi",
"javax.sound.midi.spi",
"javax.sound.sampled",
"javax.sound.sampled.spi",
"javax.sql",
"javax.sql.rowset",
"javax.sql.rowset.serial",
"javax.sql.rowset.spi",
"javax.swing",
"javax.swing.border",
"javax.swing.colorchooser",
"javax.swing.event",
"javax.swing.filechooser",
"javax.swing.plaf",
"javax.swing.plaf.basic",
"javax.swing.plaf.metal",
"javax.swing.plaf.multi",
"javax.swing.plaf.nimbus",
"javax.swing.plaf.synth",
"javax.swing.table",
"javax.swing.text",
"javax.swing.text.html",
"javax.swing.text.html.parser",
"javax.swing.text.rtf",
"javax.swing.tree",
"javax.swing.undo",
"javax.tools",
"javax.transaction",
"javax.transaction.xa",
"javax.xml",
"javax.xml.bind",
"javax.xml.bind.annotation",
"javax.xml.bind.annotation.adapters",
"javax.xml.bind.attachment",
"javax.xml.bind.helpers",
"javax.xml.bind.util",
"javax.xml.catalog",
"javax.xml.crypto",
"javax.xml.crypto.dom",
"javax.xml.crypto.dsig",
"javax.xml.crypto.dsig.dom",
"javax.xml.crypto.dsig.keyinfo",
"javax.xml.crypto.dsig.spec",
"javax.xml.datatype",
"javax.xml.namespace",
"javax.xml.parsers",
"javax.xml.soap",
"javax.xml.stream",
"javax.xml.stream.events",
"javax.xml.stream.util",
"javax.xml.transform",
"javax.xml.transform.dom",
"javax.xml.transform.sax",
"javax.xml.transform.stax",
"javax.xml.transform.stream",
"javax.xml.validation",
"javax.xml.ws",
"javax.xml.ws.handler",
"javax.xml.ws.handler.soap",
"javax.xml.ws.http",
"javax.xml.ws.soap",
"javax.xml.ws.spi",
"javax.xml.ws.spi.http",
"javax.xml.ws.wsaddressing",
"javax.xml.xpath",
"jdk.dynalink",
"jdk.dynalink.beans",
"jdk.dynalink.linker",
"jdk.dynalink.linker.support",
"jdk.dynalink.support",
"jdk.incubator.http",
"jdk.javadoc.doclet",
"jdk.jfr",
"jdk.jfr.consumer",
"jdk.jshell",
"jdk.jshell.execution",
"jdk.jshell.spi",
"jdk.jshell.tool",
"jdk.management.cmm",
"jdk.management.jfr",
"jdk.management.resource",
"jdk.nashorn.api.scripting",
"jdk.nashorn.api.tree",
"jdk.net",
"jdk.packager.services",
"jdk.packager.services.singleton",
"jdk.security.jarsigner",
"netscape.javascript",
"org.ietf.jgss",
"org.omg.CORBA",
"org.omg.CORBA_2_3",
"org.omg.CORBA_2_3.portable",
"org.omg.CORBA.DynAnyPackage",
"org.omg.CORBA.ORBPackage",
"org.omg.CORBA.portable",
"org.omg.CORBA.TypeCodePackage",
"org.omg.CosNaming",
"org.omg.CosNaming.NamingContextExtPackage",
"org.omg.CosNaming.NamingContextPackage",
"org.omg.Dynamic",
"org.omg.DynamicAny",
"org.omg.DynamicAny.DynAnyFactoryPackage",
"org.omg.DynamicAny.DynAnyPackage",
"org.omg.IOP",
"org.omg.IOP.CodecFactoryPackage",
"org.omg.IOP.CodecPackage",
"org.omg.Messaging",
"org.omg.PortableInterceptor",
"org.omg.PortableInterceptor.ORBInitInfoPackage",
"org.omg.PortableServer",
"org.omg.PortableServer.CurrentPackage",
"org.omg.PortableServer.POAManagerPackage",
"org.omg.PortableServer.POAPackage",
"org.omg.PortableServer.portable",
"org.omg.PortableServer.ServantLocatorPackage",
"org.omg.SendingContext",
"org.omg.stub.java.rmi",
"org.w3c.dom",
"org.w3c.dom.bootstrap",
"org.w3c.dom.css",
"org.w3c.dom.events",
"org.w3c.dom.html",
"org.w3c.dom.ls",
"org.w3c.dom.ranges",
"org.w3c.dom.stylesheets",
"org.w3c.dom.traversal",
"org.w3c.dom.views",
"org.w3c.dom.xpath",
"org.xml.sax",
"org.xml.sax.ext",
"org.xml.sax.helpers"]

#writer.doc_tags(paquetes,"paquete","Paquete")


'''
TAGS

Java 1.6, JAX-WS 2.0
Java 1.6, JAXB 2.1
Java 1.3, JNDI Java 1.1
Java 1.4
Java 1.5
Java 1.4, SAX 2.0
8u40
Java 1.7
Java 1.2
Java 1.4.2
Java 1.4, DOM Level 2
Java 1.6
Java 1.4, SAX Java 1.0
Java 1.5, SAX 2.0.2
JavaFX 2.2
Java 1.3
Java 1.6, Common Annotations Java 1.0
Java 1.5, DOM Level 2
Java 1.1, Java 1.1
JavaFX 2.0
Java 1.4, SAX 2.0 (extensions Java 1.0)
Java 1.6, JAXB Java 1.0
10
Java 9, DOM Level 2
Java 1.0
JDKJava 1.2
Java 1.8, DOM Level 2
Java 1.5, SAX 2.0 (extensions Java 1.1 alpha)
Java 1.7, JAXB 2.2
6u25
Java 1.7, JAX-WS 2.2
Java 1.8
JavaFX 8.0
Java 1.5, DOM Level 3
Java 9
JavaFX 2.1
Java 9, JAXB 2.3
Java 1.6, JAXB 2.0
Java 1.6, JAX-WS 2.1
Java 1.1
Java 1.6, SAAJ Java 1.3
6.0.18

'''