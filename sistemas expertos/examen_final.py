import tkinter as tk
from tkinter import messagebox
import pymysql
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder


class RedMusica:
    def __init__(self, modelo_tipo="Bayesiana"):
        self.modelo_tipo = modelo_tipo
        self.conn = None
        self.cursor = None
        self.conectar_bd()

        if self.modelo_tipo == "Bayesiana":
            self.red_bayesiana = RedBayesianaMusica(self.cursor)
        elif self.modelo_tipo == "ML":
            self.modelo_ml = DecisionTreeClassifier()
            self.entrenar_modelo_ml()

    def conectar_bd(self):
        try:
            self.conn = pymysql.connect(
                host="localhost",
                user="root",
                password="elrubiusomg12",
                database="musica",
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.conn.cursor()
        except pymysql.MySQLError as e:
            raise ValueError(f"Error al conectar con la base de datos: {e}")

    def entrenar_modelo_ml(self):
        # Extraer datos de entrenamiento
        self.cursor.execute("SELECT genero, tipo, valor, probabilidad FROM atributos")
        datos = self.cursor.fetchall()

        X = []
        y = []

        for row in datos:
            X.append([row['tipo'], row['valor'], row['probabilidad']])
            y.append(row['genero'])

        self.le_tipo = LabelEncoder()
        self.le_valor = LabelEncoder()

        # Codificar las características categóricas
        tipos = [x[0] for x in X]
        valores = [x[1] for x in X]
        probabilidades = [x[2] for x in X]

        tipos_codificados = self.le_tipo.fit_transform(tipos)
        valores_codificados = self.le_valor.fit_transform(valores)

        X_codificado = list(zip(tipos_codificados, valores_codificados, probabilidades))

        # Entrenar el modelo
        self.modelo_ml.fit(X_codificado, y)

    def diagnostico(self, duracion, estilo):
        if self.modelo_tipo == "Bayesiana":
            return self.red_bayesiana.diagnostico(duracion, estilo)
        elif self.modelo_tipo == "ML":
            return self.diagnostico_ml(duracion, estilo)

    def diagnostico_ml(self, duracion, estilo):
        # Preparar la entrada para el modelo ML
        duracion_cod = self.le_tipo.transform(["Duracion"])[0]
        estilo_cod = self.le_tipo.transform(["Estilo"])[0]
        duracion_val_cod = self.le_valor.transform([duracion])[0]
        estilo_val_cod = self.le_valor.transform([estilo])[0]

        X_test = [
            [duracion_cod, duracion_val_cod, 1],
            [estilo_cod, estilo_val_cod, 1]
        ]

        # Predicciones
        predicciones = self.modelo_ml.predict(X_test)
        probabilidades = {genero: 0 for genero in set(predicciones)}
        for pred in predicciones:
            probabilidades[pred] += 1

        total = sum(probabilidades.values())
        for genero in probabilidades:
            probabilidades[genero] /= total

        genero_recomendado = max(probabilidades, key=probabilidades.get)
        return genero_recomendado, probabilidades


class RedBayesianaMusica:
    def __init__(self, cursor):
        self.cursor = cursor

    def diagnostico(self, duracion, estilo):
        self.cursor.execute("SELECT nombre FROM generos")
        generos = self.cursor.fetchall()
        probabilidades = {}

        for genero in generos:
            nombre_genero = genero['nombre']
            prob = self.inferir_probabilidad_genero(nombre_genero, duracion, estilo)
            probabilidades[nombre_genero] = prob

        total_prob = sum(probabilidades.values())
        if total_prob == 0:
            return "Sin datos suficientes para recomendar", None

        for genero in probabilidades:
            probabilidades[genero] /= total_prob

        genero_recomendado = max(probabilidades, key=probabilidades.get)
        return genero_recomendado, probabilidades

    def inferir_probabilidad_genero(self, genero, duracion, estilo):
        self.cursor.execute("SELECT probabilidad FROM generos WHERE nombre=%s", (genero,))
        prob_genero = self.cursor.fetchone()['probabilidad']

        self.cursor.execute("SELECT probabilidad FROM atributos WHERE genero=%s AND tipo='Duracion' AND valor=%s",
                            (genero, duracion))
        prob_duracion = self.cursor.fetchone()['probabilidad']

        self.cursor.execute("SELECT probabilidad FROM atributos WHERE genero=%s AND tipo='Estilo' AND valor=%s",
                            (genero, estilo))
        prob_estilo = self.cursor.fetchone()['probabilidad']

        return prob_genero * prob_duracion * prob_estilo


class AplicacionMusica(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Recomendador de Música")
        self.geometry("400x300")

        self.modelo_tipo = "Bayesiana"
        self.red = RedMusica(self.modelo_tipo)

        self.label_duracion = tk.Label(self, text="Duración de la canción:")
        self.label_duracion.pack()

        self.duracion_var = tk.StringVar()
        self.duracion_var.set("Corta")
        self.opciones_duracion = ["Corta", "Media", "Larga"]
        self.menu_duracion = tk.OptionMenu(self, self.duracion_var, *self.opciones_duracion)
        self.menu_duracion.pack()

        self.label_estilo = tk.Label(self, text="Estilo de la canción:")
        self.label_estilo.pack()

        self.estilo_var = tk.StringVar()
        self.estilo_var.set("Moderno")
        self.opciones_estilo = ["Moderno", "Retro"]
        self.menu_estilo = tk.OptionMenu(self, self.estilo_var, *self.opciones_estilo)
        self.menu_estilo.pack()

        self.boton_recomendar = tk.Button(self, text="Recomendar Género", command=self.recomendar)
        self.boton_recomendar.pack()

        self.boton_cambiar_modelo = tk.Button(self, text="Cambiar a ML", command=self.cambiar_modelo)
        self.boton_cambiar_modelo.pack()

    def recomendar(self):
        duracion = self.duracion_var.get()
        estilo = self.estilo_var.get()

        genero_recomendado, probabilidades = self.red.diagnostico(duracion, estilo)

        if probabilidades:
            messagebox.showinfo("Recomendación",
                                f"Género recomendado: {genero_recomendado}\nProbabilidades: {probabilidades}")
        else:
            messagebox.showinfo("Recomendación", f"Género recomendado: {genero_recomendado}")

    def cambiar_modelo(self):
        if self.modelo_tipo == "Bayesiana":
            self.modelo_tipo = "ML"
            self.red = RedMusica(self.modelo_tipo)
            self.boton_cambiar_modelo.config(text="Cambiar a Bayesiana")
        else:
            self.modelo_tipo = "Bayesiana"
            self.red = RedMusica(self.modelo_tipo)
            self.boton_cambiar_modelo.config(text="Cambiar a ML")


if __name__ == "__main__":
    app = AplicacionMusica()
    app.mainloop()
