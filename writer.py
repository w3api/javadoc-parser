from datetime import datetime
import os, html, json


__OUT__ = "/Users/victor/GitHub/w3api-dev/_posts/java/"
__OUTTAGS__ = "/Users/victor/GitHub/w3api-edv/tags/java/"
__OUTJSON__ = "/Users/victor/GitHub/w3api-dev/_data/java/"



def doc_JSON(clase,duplicada):

    # Control de clases duplicadas
    if duplicada:
        basepath = clase.nombre  + "-" +  clase.paquete.replace(".","-")
    else:
        basepath = clase.nombre

    if not os.path.exists(__OUTJSON__ + clase.nombre[0]):
        os.makedirs(__OUTJSON__ + clase.nombre[0])

    # Clases como AbstractDocument.AttributeContext se generan en un directorio
    f = open(__OUTJSON__ + clase.nombre[0] + "/" + basepath + ".json","w")

    data_json = {}
    data_json["description"] = ""
    data_json["code"] = ""
    data_json["ldc"] = []

    if clase.constructores:
        c = []
        for constructor in clase.constructores:
            constructor_json = {}
            constructor_json["nombre"] = constructor.nombre
            constructor_json["description"] = ""
            if constructor.parametros:
                p = []
                for parametro in constructor.parametros:
                    parametro_json = {}
                    parametro_json["nombre"] = parametro
                    parametro_json["description"] = ""
                    p.append(parametro_json)
                constructor_json["parametros"] = p

            c.append(constructor_json)
        data_json["constructores"] = c

    if clase.metodos:
        m = []
        for metodo in clase.metodos:
            metodo_json = {}
            metodo_json["nombre"] = metodo.nombre
            metodo_json["description"] = ""
            if metodo.parametros:
                p = []
                for parametro in metodo.parametros:
                    parametro_json = {}
                    parametro_json["nombre"] = parametro
                    parametro_json["description"] = ""
                    p.append(parametro_json)
                metodo_json["parametros"] = p

            m.append(metodo_json)
        data_json["metodos"] = m

    if clase.campos:
        cp = []
        for campo in clase.campos:
            campo_json = {}
            campo_json["nombre"] = campo.nombre
            campo_json["description"] = ""
            cp.append(campo_json)
        data_json["campos"] = cp

    if clase.enumerados:
        e = []
        for enumerado in clase.enumerados:
            enumerado_json = {}
            enumerado_json["nombre"] = enumerado.nombre
            enumerado_json["description"] = ""
            e.append(enumerado_json)
        data_json["enumerados"] = e

    if clase.elementos:
        el = []
        for elemento in clase.elementos:
            elemento_json = {}
            elemento_json["nombre"] = elemento.nombre
            elemento_json["description"] = ""
            el.append(elemento_json)
        data_json["elementos"] = el

    f.write(json.dumps(data_json,indent=4))
    f.close()




## Genera los ficheros desde una clase
def gen_cabecera(nombre,path,clave,tags):

    c = ["---" + "\n",
                "title: " + nombre + "\n",
                "permalink: " + path + "\n",
                "date: " + str(datetime.datetime.now()) + "\n",
                "key: Java" + clave + "\n",
                "category: java" + "\n",
                "tags: " + str(tags) + "\n",
                "sidebar: " + "\n",
                "  nav: java" + "\n",
                "---" + "\n\n"]
    return c

def gen_cabecera_tag(tipo, nombre, titulo):

    c = ["---" + "\n",
                "title: \"" + titulo + " " + nombre + "\"\n",
                "layout: tag\n",
                "permalink: /java/tag/" + nombre + "/\n",
                "date: " + str(date.today()) + "\n",
                "key: Java" + tipo + nombre + "\n",
                "sidebar: " + "\n",
                "  nav: java" + "\n",
                "aside: " + "\n",
                "  toc: true" + "\n",
                "pagination: " + "\n",
                "  enabled: true" + "\n",
                "  tag: \"" + nombre + "\"\n",
                "  permalink: /:num/" + "\n",
                "---" + "\n\n"]
    return c

def gen_sintaxis(sintaxis):

    s = ["## Sintaxis\n",
          "~~~java\n"]
    for sin in sintaxis:
         s.append(sin + "\n")
    s.append("~~~\n\n")
    return s

def gen_ldc(clave):
    ldc = ["## Líneas de Código\n",
           "<ul>\n",
            "{%- for _ldc in " + clave + ".ldc -%}\n",
            "   <li>\n",
                "       <a href=\"{{_ldc['url'] }}\">{{ _ldc['nombre'] }}</a>\n",
            "   </li>\n",
            "{%- endfor -%}\n",
          "</ul>\n"]
    return ldc

def gen_ejemplo(base):

    e = ["## Ejemplo\n"
         "~~~java\n",
         "{{ " + base + ".code}}\n",
         "~~~\n\n",
         ]
    return e

def gen_descripcion(base):
    d = ["## Descripción\n",
         "{{" + base + ".description }}\n\n"
         ]
    return d


def gen_metodos(metodos,nombre):
    m = ["## Métodos\n"]
    for metodo in metodos:
        m.append("* [" + metodo.nombre + "()](/Java/" + nombre.replace(".","/") + "/" + metodo.nombre + ")\n")
    m.append("\n")
    return m


def gen_constructores(constructores,nombre):
    c = ["## Constructores\n"]
    for constructor in constructores:
        c.append("* [" + constructor.nombre + "()](/Java/" + nombre.replace(".","/") + "/" + constructor.nombre.replace(".","/") + "/)\n")
    c.append("\n")
    return c

def gen_campos(campos,nombre):
    c = ["## Campos\n"]
    for campo in campos:
        c.append("* [" + campo.nombre + "](/Java/" + nombre.replace(".","/") + "/" + campo.nombre + ")\n")
    c.append("\n")
    return c

def gen_enumerados(enumerados,nombre):
    e = ["## Enumerados\n"]
    for enumerado in enumerados:
        e.append("* [" + enumerado.nombre + "](/Java/" + nombre.replace(".","/") + "/" + enumerado.nombre + ")\n")
    e.append("\n")
    return e

def gen_elementos(elementos,nombre):
    el = ["## Elementos\n"]
    for elemento in elementos:
        el.append("* [" + elemento.nombre + "](/Java/" + nombre.replace(".","/") + "/" + elemento.nombre + ")\n")
    el.append("\n")
    return el

def gen_parametros(parametros):
    p = ["## Parámetros\n"]
    for parametro in parametros:
        p.append("* **" + html.escape(parametro) + "**,  ")
        p.append("{% include w3api/param_description.html metodo=_dato parametro=\"" + parametro + "\" %}\n")
    p.append("\n")
    return p

def gen_excepciones(excepciones):
    e = ["## Excepciones\n"]
    x = 0
    for excepcion in excepciones:
        e.append("[" + excepcion + "](/Java/" + excepcion + "/)")
        if x!=len(excepciones)-1:
            e.append(", ")
        x = x+1
    e.append("\n\n")
    return e

def gen_clasepadre(nombre,path):
    cp = ["## Clase Padre\n",
          "[" + nombre + "](/Java/"+ path.replace(".","/") + "/)\n\n"]

    return cp

def gen_infometodo(clave,tipo,valor):
    bm = ["{% include w3api/datos.html clase=site.data." + clave + "." + tipo + " valor=\"" + valor +"\" %}\n\n"]
    return bm

def doc_tags(tags,tipo,titulo):

    for tag in tags:

            f = open(__OUTTAGS__ + tipo + "/" + tag + ".md","w")
            cabecera = gen_cabecera_tag(tipo,tag,titulo)
            f.writelines(cabecera)

            contenido = ["<h2>Elementos</h2>\n",
                         "Todos los elementos del " + tipo + " <strong>" + tag + "</strong>\n"]
            f.writelines(contenido)

            f.close()

def doc_elementos(clase,duplicada):

    # Control de clases duplicadas
    if duplicada:
        basepath = clase.nombre + "-" + clase.paquete.replace(".","-")
    else:
        basepath = clase.nombre

    for elemento in clase.elementos:

            f = open(__OUT__ + clase.nombre[0] + "/" + basepath + "/2021-01-01-" + clase.nombre + "." + elemento.nombre + ".md","w")
            clave = "Java."+clase.nombre[0]+"."+basepath
            path = "Java/"+basepath.replace(".","/") + "/" + elemento.nombre
            nombre = clase.nombre + "." + elemento.nombre

            tags = []
            tags.append("java se")
            tags.append(clase.paquete)  #Paquete creamos espacios en los puntos
            tags.append(clase.modulo)  #Módulo creamos espacios en los puntos
            tags.append("elemento java")
            versiones = clase.version.split(", ")
            for version in versiones:
                tags.append(version)

            cabecera = gen_cabecera(nombre,path,clave,tags)
            f.writelines(cabecera)

            info_elemento = gen_infometodo(clave,"elementos",elemento.nombre)
            f.writelines(info_elemento)

            descripcion = gen_descripcion("_dato")
            f.writelines(descripcion)

            sintaxis = gen_sintaxis(elemento.sintaxis)
            f.writelines(sintaxis)

            clase_padre = gen_clasepadre(clase.nombre,basepath)
            f.writelines(clase_padre)

            ejemplo = gen_ejemplo("_dato")
            f.writelines(ejemplo)

            ldc = gen_ldc("_dato")
            f.writelines(ldc)

            f.close()


def doc_campos(clase,duplicada):

    # Control de clases duplicadas
    if duplicada:
        basepath = clase.nombre    + "-" +  clase.paquete.replace(".","-")
    else:
        basepath = clase.nombre

    for campo in clase.campos:

            f = open(__OUT__ + clase.nombre[0] + "/" + basepath + "/2021-01-01-" + clase.nombre + "." + campo.nombre + ".md","w")
            clave = "Java."+clase.nombre[0]+"."+basepath
            path = "Java/"+basepath.replace(".","/") + "/" + campo.nombre
            nombre = clase.nombre + "." + campo.nombre

            tags = []
            tags.append("java se")
            tags.append(clase.paquete)  #Paquete creamos espacios en los puntos
            tags.append(clase.modulo)  #Módulo creamos espacios en los puntos
            tags.append("campo java")
            versiones = clase.version.split(", ")
            for version in versiones:
                tags.append(version)

            cabecera = gen_cabecera(nombre,path,clave,tags)
            f.writelines(cabecera)

            info_metodo = gen_infometodo(clave,"campos",campo.nombre)
            f.writelines(info_metodo)

            descripcion = gen_descripcion("_dato")
            f.writelines(descripcion)

            sintaxis = gen_sintaxis(campo.sintaxis)
            f.writelines(sintaxis)

            clase_padre = gen_clasepadre(clase.nombre,basepath)
            f.writelines(clase_padre)

            ejemplo = gen_ejemplo("_dato")
            f.writelines(ejemplo)

            ldc = gen_ldc("_dato")
            f.writelines(ldc)

            f.close()

def doc_enumerados(clase,duplicada):

    # Control de clases duplicadas
    if duplicada:
        basepath = clase.nombre    + "-" +  clase.paquete.replace(".","-")
    else:
        basepath = clase.nombre

    for enumerado in clase.enumerados:

            f = open(__OUT__ + clase.nombre[0] + "/" + basepath + "/2021-01-01-" + clase.nombre + "." + enumerado.nombre + ".md","w")
            clave = "Java."+clase.nombre[0]+"."+basepath
            path = "Java/"+basepath.replace(".","/") + "/" + enumerado.nombre
            nombre = clase.nombre + "." + enumerado.nombre

            tags = []
            tags.append("java se")
            tags.append(clase.paquete)  #Paquete creamos espacios en los puntos
            tags.append(clase.modulo)  #Módulo creamos espacios en los puntos
            tags.append("campo java")
            versiones = clase.version.split(", ")
            for version in versiones:
                tags.append(version)

            cabecera = gen_cabecera(nombre,path,clave,tags)
            f.writelines(cabecera)

            info_metodo = gen_infometodo(clave,"enumeraodos",enumerado.nombre)
            f.writelines(info_metodo)

            descripcion = gen_descripcion("_dato")
            f.writelines(descripcion)

            sintaxis = gen_sintaxis(enumerado.sintaxis)
            f.writelines(sintaxis)

            clase_padre = gen_clasepadre(clase.nombre,basepath)
            f.writelines(clase_padre)

            ejemplo = gen_ejemplo("_dato")
            f.writelines(ejemplo)

            ldc = gen_ldc("_dato")
            f.writelines(ldc)

            f.close()

def doc_constructores(clase,duplicada):

    # Control de clases duplicadas
    if duplicada:
        basepath = clase.nombre + "-" +  clase.paquete.replace(".","-")
    else:
        basepath = clase.nombre

    for constructor in clase.constructores:

            f = open(__OUT__ + clase.nombre[0] + "/" + basepath + "/2021-01-01-" + clase.nombre + "." + constructor.nombre + ".md","w")
            clave = "Java."+clase.nombre[0]+"."+basepath
            path = "Java/"+basepath.replace(".","/") + "/" + constructor.nombre.replace(".","/")
            nombre = clase.nombre + "." + constructor.nombre + "()"

            tags = []
            tags.append("java se")
            tags.append(clase.paquete)  #Paquete creamos espacios en los puntos
            tags.append(clase.modulo)  #Módulo creamos espacios en los puntos
            tags.append("metodo java")
            versiones = clase.version.split(", ")
            for version in versiones:
                tags.append(version)


            cabecera = gen_cabecera(nombre,path,clave,tags)
            f.writelines(cabecera)

            info_metodo = gen_infometodo(clave,"constructores",constructor.nombre)
            f.writelines(info_metodo)

            descripcion = gen_descripcion("_dato")
            f.writelines(descripcion)

            sintaxis = gen_sintaxis(constructor.sintaxis)
            f.writelines(sintaxis)

            if constructor.parametros:
                parametros = gen_parametros(constructor.parametros)
                f.writelines(parametros)

            if constructor.excepciones:
                excepciones = gen_excepciones(constructor.excepciones)
                f.writelines(excepciones)

            clase_padre = gen_clasepadre(clase.nombre,basepath)
            f.writelines(clase_padre)

            ejemplo = gen_ejemplo("_dato")
            f.writelines(ejemplo)

            ldc = gen_ldc("_dato")
            f.writelines(ldc)

            f.close()



def doc_metodos(clase,duplicada):

    # Control de clases duplicadas
    if duplicada:
        basepath = clase.nombre  + "-" + clase.paquete.replace(".","-")
    else:
        basepath = clase.nombre

    for metodo in clase.metodos:

            f = open(__OUT__ + clase.nombre[0] + "/" + basepath + "/2021-01-01-" + clase.nombre + "." + metodo.nombre + ".md","w")
            clave = "Java."+clase.nombre[0]+"."+basepath
            path = "Java/"+basepath.replace(".","/") + "/" + metodo.nombre
            nombre = clase.nombre + "." + metodo.nombre + "()"

            tags = []
            tags.append("java se")
            tags.append(clase.paquete)  #Paquete creamos espacios en los puntos
            tags.append(clase.modulo)  #Módulo creamos espacios en los puntos
            tags.append("metodo java")
            versiones = clase.version.split(", ")
            for version in versiones:
                tags.append(version)


            cabecera = gen_cabecera(nombre,path,clave,tags)
            f.writelines(cabecera)

            info_metodo = gen_infometodo(clave,"metodos",metodo.nombre)
            f.writelines(info_metodo)

            descripcion = gen_descripcion("_dato")
            f.writelines(descripcion)

            sintaxis = gen_sintaxis(metodo.sintaxis)
            f.writelines(sintaxis)

            if metodo.parametros:
                parametros = gen_parametros(metodo.parametros)
                f.writelines(parametros)

            if metodo.excepciones:
                excepciones = gen_excepciones(metodo.excepciones)
                f.writelines(excepciones)

            clase_padre = gen_clasepadre(clase.nombre,basepath)
            f.writelines(clase_padre)

            ejemplo = gen_ejemplo("_dato")
            f.writelines(ejemplo)

            ldc = gen_ldc("_dato")
            f.writelines(ldc)

            f.close()


def doc_clase(clase,duplicada):

    # Control de clases duplicadas
    if duplicada:
        basepath = clase.nombre  + "-" + clase.paquete.replace(".","-")
    else:
        basepath = clase.nombre

    if not os.path.exists(__OUT__ + clase.nombre[0] + "/" + basepath + "/"):
        os.makedirs(__OUT__ + clase.nombre[0] + "/" + basepath + "/")

    # Clases como AbstractDocument.AttributeContext se generan en un directorio


    f = open(__OUT__ + clase.nombre[0] + "/" + basepath + "/2021-01-01-" + clase.nombre + ".md","w")
    clave = "Java."+clase.nombre[0]+"."+basepath
    path = "Java/"+basepath.replace(".","/")

    tags = []
    tags.append("java se")
    tags.append(clase.paquete)  #Paquete creamos espacios en los puntos
    tags.append(clase.modulo)  #Módulo creamos espacios en los puntos
    tags.append(clase.tipo + " java")
    versiones = clase.version.split(", ")
    for version in versiones:
        tags.append(version)

    cabecera = gen_cabecera(clase.nombre,path,clave, tags)
    f.writelines(cabecera)

    descripcion = gen_descripcion("site.data." + clave)
    f.writelines(descripcion)

    sintaxis = gen_sintaxis(clase.sintaxis)
    f.writelines(sintaxis)

    if clase.constructores:
        constructores = gen_constructores(clase.constructores,basepath)
        f.writelines(constructores)

    if clase.campos:
        campos = gen_campos(clase.campos,basepath)
        f.writelines(campos)

    if clase.enumerados:
        enumerados = gen_enumerados(clase.enumerados,basepath)
        f.writelines(enumerados)

    if clase.elementos:
        elementos = gen_elementos(clase.elementos,basepath)
        f.writelines(elementos)

    if clase.metodos:
        metodos = gen_metodos(clase.metodos,basepath)
        f.writelines(metodos)

    ejemplo = gen_ejemplo("site.data." + clave)
    f.writelines(ejemplo)

    ldc = gen_ldc("site.data." + clave)
    f.writelines(ldc)


    f.close()

    if clase.constructores:
        doc_constructores(clase,duplicada)

    if clase.metodos:
        doc_metodos(clase,duplicada)

    if clase.campos:
        doc_campos(clase,duplicada)

    if clase.enumerados:
        doc_enumerados(clase,duplicada)

    if clase.elementos:
        doc_elementos(clase,duplicada)

    doc_JSON(clase,duplicada)



# Genera un documento que desmabigua clases con el mismo nombre
def doc_desambiguar(nombre,lista):

    if not os.path.exists(__OUT__ + nombre[0] + "/" + nombre + "/"):
        os.makedirs(__OUT__ + nombre[0] + "/" + nombre + "/")

    # Clases como AbstractDocument.AttributeContext se generan en un directorio
    f = open(__OUT__ + nombre[0] + "/" + nombre + "/2021-01-01-" + nombre + ".md","w")
    clave = "Java." + nombre[0] + "." + nombre
    path = "Java/" + nombre.replace(".","/") + "/"

    tags = []
    tags.append("java se")

    cabecera = gen_cabecera(nombre,path,clave,tags)
    f.writelines(cabecera)


    texto = ["Existen varios elementos con el nombre **" + nombre + "**. ¿Cuál de ellas estás buscando?\n",
             "<ul>\n"]

    for clase in lista:
        pathli = "Java/" + clase.nombre.replace(".","/") + "-" + clase.paquete.replace(".","-") + "/"
        texto.append("<li><a href=\"/" +pathli + "\">"+ nombre + "</a> en el paquete <strong>" + clase.paquete + "</strong></li>\n")

    texto.append("<ul>\n")
    f.writelines(texto)

    f.close()