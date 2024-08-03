def solicitar_hechos():
    hechos = {}
    while True:
        print("tiene plumas, puede volar, es pequeño , tiene pico , pone huevos")
        hecho = input("Ingrese un hecho (ej. 'tiene plumas' o 'no tiene plumas'): ")
        if hecho.startswith("no"):
            hechos[hecho[3:]] = False
        else:
            hechos[hecho] = True

        continuar = input("¿Desea ingresar otro hecho? (si/no): ").strip().lower()
        if continuar != 'si':
            break
    return hechos


def encadenamiento_hacia_adelante(hechos, reglas):
    conclusiones = []

    for regla in reglas:
        es_aplicable = True
        for condicion in regla["condiciones"]:
            if condicion.startswith("no"):
                hecho = condicion[3:]
                if hechos.get(hecho, False):
                    es_aplicable = False
                    break
            else:
                if not hechos.get(condicion, False):
                    es_aplicable = False
                    break
        if es_aplicable:
            conclusiones.append(regla["conclusion"])

    return conclusiones


reglas = [
    {
        "condiciones": ["tiene plumas", "puede volar", "es pequeño", "tiene pico", "pone huevos"],
        "conclusion": "es pajaro"
    },
    {
        "condiciones": ["tiene_plumas", "no puede volar", "es pequeño", "tiene pico", "pone huevos"],
        "conclusion": "es pinguino"
    },
    {
        "condiciones": ["no tiene_plumas", "puede volar", "es pequeño", "no tiene pico", "no pone huevos"],
        "conclusion": "es murcielago"
    },
    {
        "condiciones": ["no tiene plumas", "no puede volar", "es pequeño", "no tiene pico", "no pone huevos"],
        "conclusion": "es gato"
    },
    {
        "condiciones": ["tiene plumas", "puede volar", "es pequeño", "tiene pico", "pone huevos"],
        "conclusion": "es colibri"
    },
    {
        "condiciones": ["tiene plumas", "puede volar", "no es pequeño", "tiene pico", "pone huevos"],
        "conclusion": "es aguila"
    }
]

while True:
    hechos = solicitar_hechos()
    conclusiones = encadenamiento_hacia_adelante(hechos, reglas)

    if conclusiones:
        print("Conclusiones:")
        for conclusion in conclusiones:
            print(conclusion)
    else:
        print("No se encontraron conclusiones basadas en los hechos proporcionados.")

    continuar = input("¿Desea ingresar más hechos o salir? (ingresar/salir): ").strip().lower()
    if continuar == 'salir':
        break