'''
-- Clase Java --
Los atributos que tiene son:
 * Nombre
 * Clave
 * Sintaxis de la clase
 * Versión desde la que está disponible
 * Listado de campos
 * Listado de constructores
 * Listado de métodos
'''

class Clase:

    nombre = ""
    paquete = ""
    modulo = ""
    tipo = "" #Clase, Interface o Enum
    sintaxis = []
    version = "1.0" # Por defecto asumimos que está desde la versión 1
    campos = []
    enumerados = []
    constructores = []
    metodos = []
    elementos = []

    def __init__(self):
        self.sintaxis = []
        self.campos = []
        self.constructores = []
        self.metodos = []
        self.enumerados = []
        self.elementos = []

    def nombre(self,nombre):
        self.nombre = nombre

    def paquete(self,paquete):
        self.paquete = paquete

    def modulo(self,modulo):
        self.modulo = modulo

    def tipo(self,tipo):
        self.tipo = tipo

    def version(self,numero):
        self.version = numero

    def add_sintaxis(self,sintaxis):
        self.sintaxis.append(sintaxis)

    def add_campo(self,campo):
        self.campos.append(campo)

    def add_constructor(self,constructor):
        self.constructores.append(constructor)

    def add_metodo(self,metodo):
        self.metodos.append(metodo)

    def add_enumerado(self,enumerado):
        self.enumerados.append(enumerado)

    def add_elemento(self,elemento):
        self.elementos.append(elemento)


class Metodo:

    nombre = ""  #nombre del método
    sintaxis = [] # Sintáxis del método
    parametros = {} # Lista de parámetros del método
    excepciones = {} # Conjunto de excepciones del método (ya que no se pueden repetir

    def __init__(self):
        self.nombre = ""
        self.sintaxis = []
        self.parametros = set()
        self.excepciones = set()

    def nombre(self,nombre):
        self.nombre = nombre

    def add_sintaxis(self,sintaxis):
        self.sintaxis.append(sintaxis)

    def add_parametros(self,parametro):
        self.parametros.add(parametro)

    def add_excepciones(self,excepcion):
        self.excepciones.add(excepcion)


class Enumerado:

    nombre = ""
    sintaxis = []

    def __init__(self):
        self.nombre = ""
        self.sintaxis = []

    def nombre(self,nombre):
        self.nombre = nombre

    def add_sintaxis(self,sintaxis):
        self.sintaxis.append(sintaxis)


class Campo:

    nombre = ""
    sintaxis = []

    def __init__(self):
        self.nombre = ""
        self.sintaxis = []

    def nombre(self,nombre):
        self.nombre = nombre

    def add_sintaxis(self,sintaxis):
        self.sintaxis.append(sintaxis)

class Elemento:

    nombre = ""
    sintaxis = []

    def __init__(self):
        self.nombre = ""
        self.sintaxis = []

    def nombre(self,nombre):
        self.nombre = nombre

    def add_sintaxis(self,sintaxis):
        self.sintaxis.append(sintaxis)


class ObjetoJS:

    nombre = ""
    sintaxis = []
    tipo = ""  # ¿?
    constructores = []
    metodos = []  #static method e instance_method
    propiedades = [] # static properties e instance_properties


    def __init__(self):
        self.nombre = ""
        self.sintaxis = []
        self.tipo = ""
        self.constructores = []
        self.metodos = []
        self.propiedades = []

    def nombre(self,nombre):
        self.nombre = nombre

    def add_constructor(self,constructor):
        self.constructores.append(constructor)

    def add_metodo(self,metodo):
        self.metodos.append(metodo)

    def add_propiedad(self,propiedad):
        self.propiedades.append(propiedad)

    def add_sintaxis(self,sintaxis):
        self.sintaxis.append(sintaxis)