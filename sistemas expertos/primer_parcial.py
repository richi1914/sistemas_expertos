peliculas = [
    {"titulo": "Mad Max: Fury Road", "genero": "Accion", "duracion": "Larga", "estilo": "Post-apocaliptico"},
    {"titulo": "La La Land", "genero": "Romance", "duracion": "Larga", "estilo": "Musical"},
    {"titulo": "El Padrino", "genero": "Drama", "duracion": "Larga", "estilo": "Crimen"},
    {"titulo": "Spider-Man: Into the Spider-Verse", "genero": "Animacion", "duracion": "Media", "estilo": "Superheroes"},
    {"titulo": "Parasitos", "genero": "Drama", "duracion": "Larga", "estilo": "Thriller"},
    {"titulo": "Toy Story", "genero": "Animacion", "duracion": "Corta", "estilo": "Familiar"},
    {"titulo": "Pulp Fiction", "genero": "Crimen", "duracion": "Larga", "estilo": "Neo-noir"},
    {"titulo": "Dunkerque", "genero": "Belico", "duracion": "Corta", "estilo": "Historico"},
    {"titulo": "Whiplash", "genero": "Drama", "duracion": "Corta", "estilo": "Musical"},
    {"titulo": "Mad Max", "genero": "Acción", "duracion": "Media", "estilo": "Post-apocaliptico"}
]

def recomendar_pelicula(genero, duracion, estilo):
    for pelicula in peliculas:
        if (pelicula["genero"].lower() == genero.lower() and
            pelicula["duracion"].lower() == duracion.lower() and
            pelicula["estilo"].lower() == estilo.lower()):
            return f"Te recomendamos la película: {pelicula['titulo']}"
    return "Lo siento, no encontramos una película que coincida con tus preferencias."

print("¡Bienvenido al sistema experto de recomendación de películas!")

genero = input("¿Qué género de película prefieres? (Accion, Drama, Romance, Animacion, Crimen, Belico): ")
duracion = input("¿Prefieres una película corta, media o larga?: ")
estilo = input("¿Qué estilo prefieres? (Musical, Thriller, Crimen, Superheroes, Post-apocaliptico, Familiar, Historico, Neo-noir): ")

recomendacion = recomendar_pelicula(genero, duracion, estilo)
print(recomendacion)