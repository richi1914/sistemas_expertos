class RedBayesianaMusica:
    def __init__(self):

        self.probabilidad_genero = {
            "Pop": 0.3,
            "Rock": 0.25,
            "Jazz": 0.15,
            "Electronica": 0.2,
            "Clasica": 0.1
        }


        self.probabilidad_atributos_dado_genero = {
            "Duracion": {
                "Pop": {"Corta": 0.5, "Media": 0.4, "Larga": 0.1},
                "Rock": {"Corta": 0.2, "Media": 0.5, "Larga": 0.3},
                "Jazz": {"Corta": 0.1, "Media": 0.4, "Larga": 0.5},
                "Electronica": {"Corta": 0.6, "Media": 0.3, "Larga": 0.1},
                "Clasica": {"Corta": 0.1, "Media": 0.3, "Larga": 0.6}
            },
            "Estilo": {
                "Pop": {"Moderno": 0.8, "Retro": 0.2},
                "Rock": {"Moderno": 0.3, "Retro": 0.7},
                "Jazz": {"Moderno": 0.4, "Retro": 0.6},
                "Electronica": {"Moderno": 0.9, "Retro": 0.1},
                "Clasica": {"Moderno": 0.1, "Retro": 0.9}
            }
        }

    def inferir_probabilidad_genero(self, genero, duracion, estilo):

        prob_genero = self.probabilidad_genero[genero]


        prob_duracion = self.probabilidad_atributos_dado_genero["Duracion"][genero][duracion]


        prob_estilo = self.probabilidad_atributos_dado_genero["Estilo"][genero][estilo]


        prob_conjunta = prob_genero * prob_duracion * prob_estilo

        return prob_conjunta

    def diagnostico(self, duracion, estilo):
        # Inferimos la probabilidad para cada género
        probabilidades = {}
        for genero in self.probabilidad_genero.keys():
            probabilidades[genero] = self.inferir_probabilidad_genero(genero, duracion, estilo)


        total_prob = sum(probabilidades.values())
        for genero in probabilidades:
            probabilidades[genero] /= total_prob


        genero_recomendado = max(probabilidades, key=probabilidades.get)
        return genero_recomendado, probabilidades

if __name__ == "__main__":
    red = RedBayesianaMusica()

    print("¡Bienvenido al sistema experto de recomendación de música!")

    duracion = input("¿Prefieres una canción corta, media o larga?: ")
    estilo = input("¿Qué estilo prefieres? (Moderno, Retro): ")

    genero_recomendado, probabilidades = red.diagnostico(duracion.capitalize(), estilo.capitalize())

    print(f"Te recomendamos escuchar música del género: {genero_recomendado}")
    print("Probabilidades por género:")
    for genero, prob in probabilidades.items():
        print(f"{genero}: {prob * 100:.2f}%")