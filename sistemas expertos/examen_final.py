import tkinter as tk
from tkinter import messagebox
import pymysql
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder


class RedBayesianaMusica:
    def __init__(self, cursor):
        self.cursor = cursor

    def inferir_probabilidad_genero(self, genero, duracion, estilo):
        # Obtenemos la probabilidad del género
        self.cursor.execute("SELECT probabilidad FROM generos WHERE nombre=%s", (genero,))
        prob_genero = self.cursor.fetchone()
        if prob_genero is None:
            print(f"[DEBUG] No se encontró el género: {genero}")
            return 0  # Si no encontramos el género, retornamos 0
        prob_genero = prob_genero['probabilidad']

        # Obtenemos la probabilidad de duración
        self.cursor.execute("SELECT probabilidad FROM atributos WHERE genero=%s AND tipo='Duracion' AND valor=%s",
                            (genero, duracion))
        prob_duracion = self.cursor.fetchone()
        if prob_duracion is None:
            print(f"[DEBUG] No se encontró la duración '{duracion}' para el género: {genero}")
            prob_duracion = {'probabilidad': 0}  # Si no encontramos duración, asignamos probabilidad 0
        prob_duracion = prob_duracion['probabilidad']

        # Obtenemos la probabilidad de estilo
        self.cursor.execute("SELECT probabilidad FROM atributos WHERE genero=%s AND tipo='Estilo' AND valor=%s",
                            (genero, estilo))
        prob_estilo = self.cursor.fetchone()
        if prob_estilo is None:
            print(f"[DEBUG] No se encontró el estilo '{estilo}' para el género: {genero}")
            prob_estilo = {'probabilidad': 0}  # Si no encontramos estilo, asignamos probabilidad 0
        prob_estilo = prob_estilo['probabilidad']

        # Calculamos la probabilidad conjunta
        prob_conjunta = prob_genero * prob_duracion * prob_estilo
        print(f"[DEBUG] Probabilidad para el género '{genero}': {prob_conjunta}")
        return prob_conjunta


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
                database="musica_db",
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.conn.cursor()

            if not self.cursor:
                raise ValueError("No se pudo establecer el cursor para la base de datos.")
        except pymysql.MySQLError as e:
            raise ValueError(f"Error al conectar con la base de datos: {e}")

    class RedBayesianaMusica:
        def __init__(self, cursor):
            if cursor is None:
                raise ValueError("Se necesita un cursor de base de datos.")
            self.cursor = cursor

    def entrenar_modelo_ml(self):
        if not self.cursor:
            raise ValueError("El cursor de la base de datos no está disponible.")

        self.cursor.execute("SELECT genero, tipo, valor, probabilidad FROM atributos")
        datos = self.cursor.fetchall()

        X = []
        y = []

        for row in datos:
            X.append([row['tipo'], row['valor'], row['probabilidad']])
            y.append(row['genero'])

        if len(X) != len(y):
            raise ValueError(f"Discrepancia en los datos: {len(X)} muestras en X, {len(y)} etiquetas en y")

        self.le_tipo = LabelEncoder()
        self.le_valor = LabelEncoder()

        tipos = [x[0] for x in X]
        valores = [x[1] for x in X]
        probabilidades = [x[2] for x in X]

        tipos_codificados = self.le_tipo.fit_transform(tipos)
        valores_codificados = self.le_valor.fit_transform(valores)

        X = list(zip(tipos_codificados, valores_codificados, probabilidades))

        self.modelo_ml.fit(X, y)

    def diagnostico(self, duracion, estilo):
        if not self.cursor:
            raise ValueError("El cursor de la base de datos no está disponible.")

        self.cursor.execute("SELECT nombre FROM generos")
        generos = self.cursor.fetchall()
        probabilidades = {}

        for genero in generos:
            genero_nombre = genero['nombre']
            probabilidades[genero_nombre] = self.red_bayesiana.inferir_probabilidad_genero(genero_nombre, duracion,
                                                                                           estilo)

        total_prob = sum(probabilidades.values())
        if total_prob == 0:
            return "No hay suficientes datos para recomendar", None

        for genero in probabilidades:
            probabilidades[genero] /= total_prob

        genero_recomendado = max(probabilidades, key=probabilidades.get)
        return genero_recomendado, probabilidades


class AplicacionMusica(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Recomendador de Música")
        self.geometry("400x300")

        self.modelo_tipo = "Bayesiana"  # Predeterminado
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