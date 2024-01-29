from abc import ABCMeta, abstractmethod

# clase Solar
class Solar:
    def __init__(self, nombre, perimetro, area, valor, edificio=None):
        self.__nombre = nombre
        self.__perimetro = perimetro
        self.__area = area
        self.__edificio = edificio
        self.__valor = valor

    def getnombre(self):
        return self.__nombre

    def getedificio(self):
        return self.__edificio

    def setedifiio(self, edificio):
        self.__edificio = edificio

    def getperimetro(self):
        return self.__perimetro

    def getarea(self):
        return self.__area

    def getvalor(self):
        return self.__valor

    # para calcular el valor por metro cuadrado se obtiene el valor total del solar + casas y se divide por el area del solar
    def getvalormetrocuadrado(self):
        valor = self.__valor
        if isinstance(self.__edificio, Edificio):
            for c in self.__edificio.getcasas():
                valor += c.getvalor()

        return valor/self.__area


class Edificio:
    def __init__(self):
        self.__casas = []

    def addcasa(self, casa):
        self.__casas.append(casa)

    def getcasas(self):
        return self.__casas

    # obtiene la varianza de las casas del edificio
    # si no tiene casas devuelve 0, aunque realmente no está definida la varianza, podría devolver None
    def getvarianza(self):
        if len(self.__casas) == 0:
            return 0 # realmente no tenemos definida la varianza
        suma = 0
        suma_2 = 0
        for c in self.__casas:
            valor = c.getvalor()
            suma += valor
            suma_2 += valor**2
        var = (1/len(self.__casas)) * suma_2 - (suma/len(self.__casas))**2
        return var


# clase Casa, abstracta, no se pueden crear objetos de esta clase
class Casa(metaclass=ABCMeta):
    def __init__(self, identificador, metros, valor):
        self.__identificador = identificador
        self.__metros = metros
        self.__valor = valor

    def getidentificador(self):
        return self.__identificador

    def getmetros(self):
        return self.__metros

    def getvalor(self):
        return self.__valor

    def setvalor(self, valor):
        self.__valor = valor


# clase Piso instanciable
class Piso(Casa):
    def __init__(self, identificador, metros, valor):
        super().__init__(identificador, metros, valor)


# Los Áticos son como los pisos, pero pueden tener o no terraza
class Atico(Piso):
    def __init__(self, identificador, metros, valor, terraza=False):
        super().__init__(identificador, metros, valor)
        self.__terraza = terraza

    def getterraza(self):
        return self.__terraza


# Los unifamiliares son casas que pueden tener o no piscina
class Unifamiliar(Casa):
    def __init__(self, identificador, metros, valor, piscina=False):
        super().__init__(identificador, metros, valor)
        self.__piscina = piscina

    def getpiscina(self):
        return self.__piscina


# Construir la ciudad
def construir_ciudad():
    ed1 = Edificio()
    ed1.addcasa(Piso("1A", 100, 25000))
    ed1.addcasa(Piso("1B", 90, 22000))
    ed1.addcasa(Piso("2A", 100, 27000))
    ed1.addcasa(Piso("2B", 90, 26000))
    ed1.addcasa(Atico("3A", 150, 35000, True))
    sol1 = Solar("Rafal", 500, 2000, 15000, ed1)

    sol2 = Solar("Son Puig", 500, 2100, 21000, None)

    ed3 = Edificio()
    ed3.addcasa(Piso("1A", 100, 25000))
    ed3.addcasa(Piso("1B", 110, 29000))
    ed3.addcasa(Piso("2A", 100, 27000))
    ed3.addcasa(Piso("2B", 110, 32000))
    ed3.addcasa(Atico("3A", 150, 35000, True))
    ed3.addcasa(Atico("3B", 170, 39000, False))
    sol3 = Solar("Serralta", 1500, 20000, 18000, ed3)

    ed4 = Edificio()
    ed4.addcasa(Piso("BJA", 70, 15000))
    ed4.addcasa(Piso("BJB", 70, 15000))
    ed4.addcasa(Piso("1A", 90, 20000))
    ed4.addcasa(Piso("2B", 90, 20000))
    ed4.addcasa(Atico("3A", 90, 23000, True))
    ed4.addcasa(Atico("3B", 90, 23000))
    sol4 = Solar("Son Gotleu", 300, 1500, 5000, ed4)

    ed45 = Edificio()
    ed45.addcasa(Unifamiliar("24", 240, 65000, True))
    sol5 = Solar("Mi casa", 120, 800, 47000, ed45)

    ciudad = []
    ciudad.append(sol1)
    ciudad.append(sol2)
    ciudad.append(sol3)
    ciudad.append(sol4)
    ciudad.append(sol5)

    return ciudad

#obtenemos la ciudad
ciudad = construir_ciudad()

# el valor por metro cuadrado de cada solar
for sol in ciudad:
    print(sol.getnombre(), sol.getvalormetrocuadrado())

# mostrar cuantas casas tienen piscina
count_conpiscina = 0
for sol in ciudad:
    if isinstance(sol.getedificio(), Edificio):
        for c in sol.getedificio().getcasas():
            if (isinstance(c, Unifamiliar)):
                if c.getpiscina():
                    count_conpiscina += 1
print("Hay", count_conpiscina, "casas con piscina")

# mostrar cuantas casas tiene terraza
count_conterraza = 0
for sol in ciudad:
    if isinstance(sol.getedificio(), Edificio):
        for c in sol.getedificio().getcasas():
            if (isinstance(c, Atico)):
                if c.getterraza():
                    count_conterraza += 1
print("Hay", count_conpiscina, "casas con terraza")

# mostrar los solares vacíos
for sol in ciudad:
    if not isinstance(sol.getedificio(), Edificio):
        print(sol.getnombre(), "esta vacio")

# mostrar el porcentaje áticos que hay respecto el número de pisos
count_pisos = 0
count_aticos = 0
for sol in ciudad:
    if isinstance(sol.getedificio(), Edificio):
        for c in sol.getedificio().getcasas():
            if (isinstance(c, Piso)):
                count_pisos += 1
                if (isinstance(c, Atico)):
                    count_aticos += 1
print("Porcentaje de aticos", count_aticos/count_pisos*100, "%")

# indicar cual es el edificio cuya varianza del precio por casa es mayor
max_varianza = 0
max_varianza_sol = []
for sol in ciudad:
    if isinstance(sol.getedificio(), Edificio):
        var = sol.getedificio().getvarianza()
        if var == max_varianza:
            max_varianza_sol.append(sol)
        elif var > max_varianza:
            max_varianza = var
            max_varianza_sol = [sol]
print("Maxima Varianza", max_varianza, "solares:")
for sol in max_varianza_sol:
    print(sol.getnombre())
