def extraer_clase_v7(soup2):
    # Lo primero es crear la clase
    c1 = Clase()

    # Nombre de la Clase
    nombre = soup2.find("h2", class_="title")

    # Tipo de clase (Class o Interface)
    if "Class" in nombre.text:
        c1.nombre = nombre.text.replace('Class ','')
        c1.tipo = "clase"
    else:
        if "Interface" in nombre.text:
            c1.nombre = nombre.text.replace('Interface ','')
            c1.tipo = "interface"
        else:
            if "Enum" in nombre.text:
                c1.nombre = nombre.text.replace('Enum ','')
                c1.tipo = "enum"
            else:
                if "Annotation" in nombre.text:
                    c1.nombre = nombre.text.replace('Annotation ','')
                    c1.tipo = "annotation"

    # Paquete
    paquete = soup2.find("div", class_="subTitle")
    c1.paquete = paquete.text

    # Sintaxis

    # De la clase "Description" obtenemos
    # en un pre la sintaxis de la clase
    # de un dl > dd la versión desde la que está disponible

    descripcion = soup2.find("div", class_="description")
    sintaxis = descripcion.find("pre")
    c1.sintaxis = limpiar(sintaxis.text)

    # Versión
    versiones = descripcion.find_all("dd")

    for version in versiones:
        # Comprobamos que el anterior dt al dd tiene un span con el texto "Since:"
        since = version.find_previuos_sibling("dt").find("span")
        if since:
            if since.text == "Since:":
                c1.version = version.text
                break

    ## Campos
    # La primera tabla tiene los campos
    # En la tabla buscamos los td
    # De cada td el primer code es el que tiene el modificador o nombre del campo
    # Ya que hay td que tienen varios code. Nos vale el primero

    tabla_campos = soup2.find("table", summary="Field Summary table, listing fields, and an explanation")
    if (tabla_campos):
        filas_campos = tabla_campos.find_all("td")
        x = 0

        for fila in filas_campos:
            if ((x % 2) == 0):
                modificador = fila.find("code").text
            else:
                campo = Campo()
                campo.nombre = fila.find("code").text
                campo.sintaxis = modificador + " " + fila.find("code").text
                c1.add_campo(campo)
            x = x+1

    ## Enumerados
    tabla_enumerados = soup2.find("table", summary="Enum Constant Summary table, listing enum constants, and an explanation")
    if (tabla_enumerados):
        enumerados = tabla_enumerados.find_all("code")

        detalle = soup2.find("div", class_="details")

        for enumerado in enumerados:
            en = Enumerado()
            en.nombre = enumerado.text
            en.sintaxis = obtener_sintaxis_enumerado(detalle,en.nombre)
            c1.add_enumerado(en)

    ## Constructores
    # La segunda tabla tiene los campos
    # En la tabla buscamos los td
    # El primer code es el que tiene el constructor

    tabla_campos = soup2.find("table", summary="Constructor Summary table, listing constructors, and an explanation")
    if (tabla_campos):

        filas_campos = tabla_campos.find_all("td")

        for fila in filas_campos:
            cs = Metodo()
            cs_sintaxis = limpiar(fila.find("code").text)
            cs_nombre = c1.nombre # Constructor mismo nombre que la clase
            cs_parametros = cs_sintaxis[cs_sintaxis.find("(")+1:-1].split(",")

            cs.nombre = cs_nombre
            cs.sintaxis = cs_sintaxis

            if cs_parametros:
                    for parametro in cs_parametros:
                        cs.add_parametros(limpiar(parametro))

            c1.add_constructor(cs)

    ## Métodos
    # La tercera tabla tiene los métodos
    # En la tabla buscamos los td
    # De cada td el primer code es el que tiene el modificador o nombre del campo
    # Ya que hay td que tienen varios code. Nos vale el primero

    tabla_campos = soup2.find("table", summary="Method Summary table, listing methods, and an explanation")
    if (tabla_campos):
        filas_campos = tabla_campos.find_all("td")
        x = 0

        for fila in filas_campos:
            if ((x % 2) == 0):
                modificador = fila.find("code").text
            else:

                nombre_parametros = limpiar(fila.find("code").text)
                sintaxis = modificador + " " + nombre_parametros
                nombre = nombre_parametros[0:nombre_parametros.find("(")]

                parametros = nombre_parametros[nombre_parametros.find("(")+1:-1].split(",")

                # Las Excepciones no están en el resumen hay que buscarlas en el detale
                detalle = soup2.find("div", class_="details")
                excepciones = obtener_excepciones(detalle,sintaxis).split(",")

                m1 = Metodo()
                m1.nombre = nombre
                m1.add_sintaxis(sintaxis)

                if ((parametros) and (parametros[0]!="")):
                    for p in parametros:
                        m1.add_parametros(limpiar(p))

                if ((excepciones) and (excepciones[0]!="")):
                    for e in excepciones:
                        m1.add_excepciones(limpiar(e))

                c1.add_metodo(m1)

            x = x+1

    return c1