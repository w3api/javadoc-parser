from datetime import date
import os, html, json


__OUT__ = "/Users/victor/github/w3api/_posts/javascript/"
__OUTTAGS__ = "/Users/victor/github/w3api/tags/javascript/"
__OUTJSON__ = "/Users/victor/github/w3api/_data/javascript/"

def doc_JSON(objeto):

    basepath = objeto.nombre

    if not os.path.exists(__OUTJSON__ + objeto.nombre[0].upper()):
        os.makedirs(__OUTJSON__ + objeto.nombre[0].upper())

    # Clases como AbstractDocument.AttributeContext se generan en un directorio
    f = open(__OUTJSON__ + objeto.nombre[0].upper() + "/" + basepath + ".json","w")

    data_json = {}
    data_json["description"] = ""
    data_json["code"] = ""
    data_json["ldc"] = []

    if objeto.constructores:
        c = []
        for constructor in objeto.constructores:
            constructor_json = {}
            constructor_json["nombre"] = constructor.nombre
            constructor_json["description"] = ""
            constructor_json["code"]= ""
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

    if objeto.metodos:
        m = []
        for metodo in objeto.metodos:
            metodo_json = {}
            metodo_json["nombre"] = metodo.nombre
            metodo_json["description"] = ""
            metodo_json["code"] = ""
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

    if objeto.propiedades:
        p = []
        for propiedad in objeto.propiedades:
            propiedad_json = {}
            propiedad_json["nombre"] = propiedad.nombre
            propiedad_json["description"] = ""
            propiedad_json["code"] = ""
            p.append(propiedad_json)
        data_json["propiedades"] = p

    f.write(json.dumps(data_json,indent=4))
    f.close()


## Genera los ficheros desde una clase
def gen_cabecera(nombre,path,clave,tags):

    c = ["---" + "\n",
                "title: " + nombre + "\n",
                "permalink: " + path + "\n",
                "date: " + str(date.today()) + "\n",
                "key: Javascript" + clave + "\n",
                "category: javascript" + "\n",
                "tags: " + str(tags) + "\n",
                "sidebar: " + "\n",
                "  nav: javascript" + "\n",
                "---" + "\n\n"]
    return c

def gen_cabecera_tag(tipo, nombre, titulo):

    c = ["---" + "\n",
                "title: \"" + titulo + " " + nombre + "\"\n",
                "layout: tag\n",
                "permalink: /javascript/tag/" + nombre + "/\n",
                "date: " + str(date.today()) + "\n",
                "key: Javascript" + tipo + nombre + "\n",
                "sidebar: " + "\n",
                "  nav: javascript" + "\n",
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
          "~~~javascript\n"]
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
        m.append("* [" + metodo.nombre + "()](/javascript/" + nombre.replace(".","/") + "/" + metodo.nombre + ")\n")
    m.append("\n")
    return m


def gen_constructores(constructores,nombre):
    c = ["## Constructores\n"]
    for constructor in constructores:
        c.append("* [" + constructor.nombre + "()](/javascript/" + nombre.replace(".","/") + "/" + constructor.nombre.replace(".","/") + "/)\n")
    c.append("\n")
    return c

def gen_campos(campos,nombre):
    c = ["## Campos\n"]
    for campo in campos:
        c.append("* [" + campo.nombre + "](/javascript/" + nombre.replace(".","/") + "/" + campo.nombre + ")\n")
    c.append("\n")
    return c

def gen_propiedades(propiedades,nombre):
    p = ["## Propiedades\n"]
    for propiedad in propiedades:
        p.append("* [" + propiedad.nombre + "](/javascript/" + nombre.replace(".","/") + "/" + propiedad.nombre + ")\n")
    p.append("\n")
    return p

def gen_enumerados(enumerados,nombre):
    e = ["## Enumerados\n"]
    for enumerado in enumerados:
        e.append("* [" + enumerado.nombre + "](/javascript/" + nombre.replace(".","/") + "/" + enumerado.nombre + ")\n")
    e.append("\n")
    return e

def gen_elementos(elementos,nombre):
    el = ["## Elementos\n"]
    for elemento in elementos:
        el.append("* [" + elemento.nombre + "](/javascript/" + nombre.replace(".","/") + "/" + elemento.nombre + ")\n")
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
    cp = ["## Objeto Padre\n",
          "[" + nombre + "](/javascript/"+ path.replace(".","/") + "/)\n\n"]

    return cp

def gen_infometodo(clave,tipo,valor):
    bm = ["{% include w3api/datos.html clase=site.data." + clave + "." + tipo + " valor=\"" + valor +"\" %}\n\n"]
    return bm

def doc_propiedades(objeto):

    basepath = objeto.nombre

    for propiedad in objeto.propiedades:

            f = open(__OUT__ + objeto.nombre[0].upper() + "/" + basepath + "/2021-01-01-" + objeto.nombre + "." + propiedad.nombre + ".md","w")
            clave = "Javascript."+objeto.nombre[0].upper()+"."+basepath
            path = "Javascript/"+basepath.replace(".","/") + "/" + propiedad.nombre
            nombre = objeto.nombre + "." + propiedad.nombre

            tags = []
            tags.append("propiedad javascript")

            cabecera = gen_cabecera(nombre,path,clave,tags)
            f.writelines(cabecera)

            info_metodo = gen_infometodo(clave,"propiedades",propiedad.nombre)
            f.writelines(info_metodo)

            descripcion = gen_descripcion("_dato")
            f.writelines(descripcion)

            sintaxis = gen_sintaxis(propiedad.sintaxis)
            f.writelines(sintaxis)

            clase_padre = gen_clasepadre(objeto.nombre,basepath)
            f.writelines(clase_padre)

            ejemplo = gen_ejemplo("_dato")
            f.writelines(ejemplo)

            ldc = gen_ldc("_dato")
            f.writelines(ldc)

            f.close()



def doc_constructores(objeto):

    basepath = objeto.nombre

    for constructor in objeto.constructores:

            f = open(__OUT__ + objeto.nombre[0].upper() + "/" + basepath + "/2021-01-01-" + objeto.nombre + "." + constructor.nombre + ".md","w")
            clave = "Javascript."+objeto.nombre[0].upper()+"."+basepath
            path = "Javascript/"+basepath.replace(".","/") + "/" + constructor.nombre.replace(".","/")
            nombre = objeto.nombre + "." + constructor.nombre + "()"

            tags = []
            tags.append("constructor javascript")

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


            clase_padre = gen_clasepadre(objeto.nombre,basepath)
            f.writelines(clase_padre)

            ejemplo = gen_ejemplo("_dato")
            f.writelines(ejemplo)

            ldc = gen_ldc("_dato")
            f.writelines(ldc)

            f.close()



def doc_metodos(objeto):

    basepath = objeto.nombre

    for metodo in objeto.metodos:

            f = open(__OUT__ + objeto.nombre[0].upper() + "/" + basepath + "/2021-01-01-" + objeto.nombre + "." + metodo.nombre + ".md","w")
            clave = "Javascript."+objeto.nombre[0].upper()+"."+basepath
            path = "Javascript/"+basepath.replace(".","/") + "/" + metodo.nombre
            nombre = objeto.nombre + "." + metodo.nombre + "()"

            tags = []
            tags.append("metodo javascript")

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

            clase_padre = gen_clasepadre(objeto.nombre,basepath)
            f.writelines(clase_padre)

            ejemplo = gen_ejemplo("_dato")
            f.writelines(ejemplo)

            ldc = gen_ldc("_dato")
            f.writelines(ldc)

            f.close()



def doc_objeto(objeto):

    basepath = objeto.nombre

    if not os.path.exists(__OUT__ + objeto.nombre[0].upper() + "/" + basepath + "/"):
        os.makedirs(__OUT__ + objeto.nombre[0].upper() + "/" + basepath + "/")

    # Clases como AbstractDocument.AttributeContext se generan en un directorio


    f = open(__OUT__ + objeto.nombre[0].upper() + "/" + basepath + "/2021-01-01-" + objeto.nombre + ".md","w")
    clave = "Javascript."+objeto.nombre[0].upper()+"."+basepath
    path = "Javascript/"+basepath.replace(".","/")

    tags = []
    if objeto.tipo:
        tags.append(objeto.tipo + " javascript")

    cabecera = gen_cabecera(objeto.nombre,path,clave, tags)
    f.writelines(cabecera)

    descripcion = gen_descripcion("site.data." + clave)
    f.writelines(descripcion)

    sintaxis = gen_sintaxis(objeto.sintaxis)
    f.writelines(sintaxis)

    if objeto.constructores:
        constructores = gen_constructores(objeto.constructores,basepath)
        f.writelines(constructores)

    if objeto.propiedades:
        campos = gen_propiedades(objeto.propiedades,basepath)
        f.writelines(campos)

    if objeto.metodos:
        metodos = gen_metodos(objeto.metodos,basepath)
        f.writelines(metodos)

    ejemplo = gen_ejemplo("site.data." + clave)
    f.writelines(ejemplo)

    ldc = gen_ldc("site.data." + clave)
    f.writelines(ldc)


    f.close()

    if objeto.constructores:
        doc_constructores(objeto)

    if objeto.metodos:
        doc_metodos(objeto)

    if objeto.propiedades:
        doc_propiedades(objeto)

    doc_JSON(objeto)