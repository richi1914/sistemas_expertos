class Enfermedad:
    def __init__(self, nombre):
        self.nombre = nombre

class Sintoma:
    def __init__(self, nombre):
        self.nombre = nombre

class RelacionSintomaEnfermedad:
    def __init__(self):
        self.relaciones_sintoma_enfermedad = []

    def agregar_sintoma_enfermedad(self, sintoma, enfermedad):
        self.relaciones_sintoma_enfermedad.append((sintoma, enfermedad))

    def es_sintoma_de(self, sintoma, enfermedad):
        return (sintoma, enfermedad) in self.relaciones_sintoma_enfermedad

def main():
    gripe = Enfermedad("Gripe")
    covid = Enfermedad("COVID-19")

    fiebre = Sintoma("Fiebre")
    tos = Sintoma("Tos")
    dificultad_respirar = Sintoma("Dificultad para respirar")

    relaciones = RelacionSintomaEnfermedad()

    relaciones.agregar_sintoma_enfermedad(fiebre, gripe)
    relaciones.agregar_sintoma_enfermedad(tos, gripe)
    relaciones.agregar_sintoma_enfermedad(tos, covid)
    relaciones.agregar_sintoma_enfermedad(dificultad_respirar, covid)

    print(f"¿La fiebre es un síntoma de la gripe? {relaciones.es_sintoma_de(fiebre, gripe)}")
    print(f"¿La tos es un síntoma de la gripe? {relaciones.es_sintoma_de(tos, gripe)}")
    print(f"¿La dificultad para respirar es un síntoma de la gripe? {relaciones.es_sintoma_de(dificultad_respirar, gripe)}")
    print(f"¿La tos es un síntoma de COVID-19? {relaciones.es_sintoma_de(tos, covid)}")

if __name__ == "__main__":
    main()