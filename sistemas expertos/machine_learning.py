import tkinter as tk
from tkinter import messagebox
import sqlite3
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
import numpy as np


class RedBayesianaMusicaML:
    def __init__(self):
        self.conectar_bd()
        self.entrenar_modelo()

    def conectar_bd(self):
        # Conexión con la base de datos
        self.conn = sqlite3.connect('musica.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS generos (
                nombre TEXT PRIMARY KEY,
                probabilidad REAL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS atributos (
                genero TEXT,
                tipo TEXT,
                valor TEXT,
                probabilidad REAL,
                FOREIGN KEY (genero) REFERENCES generos (nombre)
            )
        ''')
        self.cargar_datos_iniciales()

    def cargar_datos_iniciales(self):
        # Insertamos datos iniciales
        generos_iniciales = [
            ("Pop", 0.3), ("Rock", 0.25), ("Jazz", 0.15),
            ("Electronica", 0.2), ("Clasica", 0.1)
        ]
        atributos_iniciales = [
            ("Pop", "Duracion", "Corta", 0.5), ("Pop", "Duracion", "Media", 0.4),
            ("Pop", "Duracion", "Larga", 0.1), ("Rock", "Duracion", "Corta", 0.2),
            ("Rock", "Duracion", "Media", 0.5), ("Rock", "Duracion", "Larga", 0.3),
            ("Jazz", "Duracion", "Corta", 0.1), ("Jazz", "Duracion", "Media", 0.4),
            ("Jazz", "Duracion", "Larga", 0.5), ("Electronica", "Duracion", "Corta", 0.6),
            ("Electronica", "Duracion", "Media", 0.3), ("Electronica", "Duracion", "Larga", 0.1),
            ("Clasica", "Duracion", "Corta", 0.1), ("Clasica", "Duracion", "Media", 0.3),
            ("Clasica", "Duracion", "Larga", 0.6),
            ("Pop", "Estilo", "Moderno", 0.8), ("Pop", "Estilo", "Retro", 0.2),
            ("Rock", "Estilo", "Moderno", 0.3), ("Rock", "Estilo", "Retro", 0.7),
            ("Jazz", "Estilo", "Moderno", 0.4), ("Jazz", "Estilo", "Retro", 0.6),
            ("Electronica", "Estilo", "Moderno", 0.9), ("Electronica", "Estilo", "Retro", 0.1),
            ("Clasica", "Estilo", "Moderno", 0.1), ("Clasica", "Estilo", "Retro", 0.9)
        ]

        for genero in generos_iniciales:
            self.cursor.execute("INSERT OR IGNORE INTO generos VALUES (?, ?)", genero)

        for atributo in atributos_iniciales:
            self.cursor.execute("INSERT OR IGNORE INTO atributos VALUES (?, ?, ?, ?)", atributo)

        self.conn.commit()

    def entrenar_modelo(self):
        # Recopilamos los datos para entrenar el modelo
        self.cursor.execute("SELECT genero, tipo, valor FROM atributos")
        datos = self.cursor.fetchall()

        generos = [fila[0] for fila in datos]
        duraciones = [fila[1] for fila in datos]
        estilos = [fila[2] for fila in datos]

        # Codificación de datos
        self.encoder_genero = LabelEncoder()
        self.encoder_duracion = LabelEncoder()
        self.encoder_estilo = LabelEncoder()

        y = self.encoder_genero.fit_transform(generos)
        X_duracion = self.encoder_duracion.fit_transform(duraciones)
        X_estilo = self.encoder_estilo.fit_transform(estilos)
        X = np.column_stack((X_duracion, X_estilo))

        # Entrenamos el modelo
        self.modelo = MultinomialNB()
        self.modelo.fit(X, y)

    def diagnostico(self, duracion, estilo):
        duracion_encoded = self.encoder_duracion.transform([duracion])[0]
        estilo_encoded = self.encoder_estilo.transform([estilo])[0]
        X_test = np.array([[duracion_encoded, estilo_encoded]])
        prediccion = self.modelo.predict(X_test)
        genero_recomendado = self.encoder_genero.inverse_transform(prediccion)[0]
        return genero_recomendado


class AplicacionMusica(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Recomendador de Música ML")
        self.geometry("400x300")

        self.red = RedBayesianaMusicaML()

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

    def recomendar(self):
        duracion = self.duracion_var.get()
        estilo = self.estilo_var.get()
        genero_recomendado = self.red.diagnostico(duracion, estilo)

        messagebox.showinfo("Recomendación", f"Género recomendado: {genero_recomendado}")

    def cerrar(self):
        self.red.cerrar_bd()
        self.destroy()


if __name__ == "__main__":
    app = AplicacionMusica()
    app.protocol("WM_DELETE_WINDOW", app.cerrar)
    app.mainloop()