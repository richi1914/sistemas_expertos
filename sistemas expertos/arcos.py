class Nodo:
    def __init__(self, etiqueta):
        self.etiqueta = etiqueta
        self.arcos = []

    def agregar_arco(self, destino, etiqueta_arco):
        self.arcos.append(Arco(self, destino, etiqueta_arco))


class Arco:
    def __init__(self, origen, destino, etiqueta):
        self.origen = origen
        self.destino = destino
        self.etiqueta = etiqueta

    def __str__(self):
        return f"{self.origen.etiqueta} -- {self.etiqueta} --> {self.destino.etiqueta}"


class RedSemantica:
    def __init__(self):
        self.nodos = []

    def crear_nodo(self, etiqueta):
        nodo = Nodo(etiqueta)
        self.nodos.append(nodo)
        return nodo

    def mostrar_red(self):
        for nodo in self.nodos:
            for arco in nodo.arcos:
                print(arco)

if __name__ == "__main__":
    red = RedSemantica()

    # Creación de nodos según la imagen
    animal = red.crear_nodo("ANIMAL")
    vida = red.crear_nodo("vida")
    sentir = red.crear_nodo("sentir")
    moverse = red.crear_nodo("moverse")

    ave = red.crear_nodo("AVE")
    bien = red.crear_nodo("bien")
    plumas = red.crear_nodo("plumas")
    huevos = red.crear_nodo("huevos")

    avestruz = red.crear_nodo("AVESTRUZ")
    largas = red.crear_nodo("largas")
    no_puede = red.crear_nodo("no_puede")

    albatros = red.crear_nodo("ALBATROS")
    muy_bien = red.crear_nodo("muy_bien")

    mamifero = red.crear_nodo("MAMIFERO")
    leche = red.crear_nodo("leche")
    pelo = red.crear_nodo("pelo")

    ballena = red.crear_nodo("BALLENA")
    piel = red.crear_nodo("piel")
    mar = red.crear_nodo("mar")

    tigre = red.crear_nodo("TIGRE")
    carne = red.crear_nodo("carne")

    animal.agregar_arco(vida, "tiene")
    animal.agregar_arco(sentir, "puede")
    animal.agregar_arco(moverse, "puede")

    animal.agregar_arco(ave, "tipo_de")
    animal.agregar_arco(mamifero, "tipo_de")

    ave.agregar_arco(bien, "vuela")
    ave.agregar_arco(plumas, "tiene")
    ave.agregar_arco(huevos, "pone")

    ave.agregar_arco(avestruz, "tipo_de")
    ave.agregar_arco(albatros, "tipo_de")

    avestruz.agregar_arco(largas, "patas")
    avestruz.agregar_arco(no_puede, "vuela")

    albatros.agregar_arco(muy_bien, "vuela")

    mamifero.agregar_arco(leche, "da")
    mamifero.agregar_arco(pelo, "tiene")

    mamifero.agregar_arco(ballena, "tipo_de")
    mamifero.agregar_arco(tigre, "tipo_de")

    ballena.agregar_arco(piel, "tiene")
    ballena.agregar_arco(mar, "vive_en")

    tigre.agregar_arco(carne, "come")

    red.mostrar_red()