import tkinter as tk
from tkinter import messagebox
import sqlite3


class RedBayesianaMusica:
    def __init__(self):
        self.conectar_bd()

    def conectar_bd(self):
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

    def inferir_probabilidad_genero(self, genero, duracion, estilo):
        self.cursor.execute("SELECT probabilidad FROM generos WHERE nombre=?", (genero,))
        prob_genero = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT probabilidad FROM atributos WHERE genero=? AND tipo='Duracion' AND valor=?",
                            (genero, duracion))
        prob_duracion = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT probabilidad FROM atributos WHERE genero=? AND tipo='Estilo' AND valor=?",
                            (genero, estilo))
        prob_estilo = self.cursor.fetchone()[0]

        prob_conjunta = prob_genero * prob_duracion * prob_estilo
        return prob_conjunta

    def diagnostico(self, duracion, estilo):
        probabilidades = {}
        for genero in self.cursor.execute("SELECT nombre FROM generos").fetchall():
            genero = genero[0]
            probabilidades[genero] = self.inferir_probabilidad_genero(genero, duracion, estilo)

        total_prob = sum(probabilidades.values())
        for genero in probabilidades:
            probabilidades[genero] /= total_prob

        genero_recomendado = max(probabilidades, key=probabilidades.get)
        return genero_recomendado, probabilidades

    def agregar_genero(self, genero, probabilidad, atributos):
        self.cursor.execute("INSERT OR REPLACE INTO generos VALUES (?, ?)", (genero, probabilidad))
        for tipo, valor, prob in atributos:
            self.cursor.execute("INSERT OR REPLACE INTO atributos VALUES (?, ?, ?, ?)", (genero, tipo, valor, prob))
        self.conn.commit()

    def cerrar_bd(self):
        self.conn.close()


class AplicacionMusica(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Recomendador de Música")
        self.geometry("400x300")

        self.red = RedBayesianaMusica()

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

        self.boton_agregar = tk.Button(self, text="Agregar Género", command=self.agregar_genero)
        self.boton_agregar.pack()

    def recomendar(self):
        duracion = self.duracion_var.get()
        estilo = self.estilo_var.get()
        genero_recomendado, probabilidades = self.red.diagnostico(duracion, estilo)

        messagebox.showinfo("Recomendación",
                            f"Género recomendado: {genero_recomendado}\nProbabilidades: {probabilidades}")

    def agregar_genero(self):
        def guardar():
            nuevo_genero = entry_genero.get()
            probabilidad = float(entry_prob.get())
            atributos = [
                ("Duracion", "Corta", float(entry_duracion_corta.get())),
                ("Duracion", "Media", float(entry_duracion_media.get())),
                ("Duracion", "Larga", float(entry_duracion_larga.get())),
                ("Estilo", "Moderno", float(entry_estilo_moderno.get())),
                ("Estilo", "Retro", float(entry_estilo_retro.get()))
            ]
            self.red.agregar_genero(nuevo_genero, probabilidad, atributos)
            ventana_agregar.destroy()

        ventana_agregar = tk.Toplevel(self)
        ventana_agregar.title("Agregar Género")

        tk.Label(ventana_agregar, text="Nombre del género:").pack()
        entry_genero = tk.Entry(ventana_agregar)
        entry_genero.pack()

        tk.Label(ventana_agregar, text="Probabilidad:").pack()
        entry_prob = tk.Entry(ventana_agregar)
        entry_prob.pack()

        tk.Label(ventana_agregar, text="Probabilidad Duración Corta:").pack()
        entry_duracion_corta = tk.Entry(ventana_agregar)
        entry_duracion_corta.pack()

        tk.Label(ventana_agregar, text="Probabilidad Duración Media:").pack()
        entry_duracion_media = tk.Entry(ventana_agregar)
        entry_duracion_media.pack()

        tk.Label(ventana_agregar, text="Probabilidad Duración Larga:").pack()
        entry_duracion_larga = tk.Entry(ventana_agregar)
        entry_duracion_larga.pack()

        tk.Label(ventana_agregar, text="Probabilidad Estilo Moderno:").pack()
        entry_estilo_moderno = tk.Entry(ventana_agregar)
        entry_estilo_moderno.pack()

        tk.Label(ventana_agregar, text="Probabilidad Estilo Retro:").pack()
        entry_estilo_retro = tk.Entry(ventana_agregar)
        entry_estilo_retro.pack()

        tk.Button(ventana_agregar, text="Guardar", command=guardar).pack()

    def cerrar(self):
        self.red.cerrar_bd()
        self.destroy()


if __name__ == "__main__":
    app = AplicacionMusica()
    app.protocol("WM_DELETE_WINDOW", app.cerrar)
    app.mainloop()