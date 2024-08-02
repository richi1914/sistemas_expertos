hechos = {
    "tiene_plumas": True,
    "puede_volar": True,
    "es_pequeño": True,
    "tiene_pico": True,
    "pone_huevos": True
}

reglas = [
    {
        "condiciones": ["tiene_plumas", "puede_volar", "es_pequeño", "tiene_pico", "pone_huevos"],
        "conclusion": "es pajaro"
    },
    {
        "condiciones": ["tiene_plumas", "no_puede_volar", "es_pequeño", "tiene_pico", "pone_huevos"],
        "conclusion": "es pinguino"
    },
    {
        "condiciones": ["no_tiene_plumas", "puede_volar", "es_pequeño", "no_tiene_pico", "no_pone_huevos"],
        "conclusion": "es murcielago"
    },
    {
        "condiciones": ["no_tiene_plumas", "no_puede_volar", "es_pequeño", "no_tiene_pico", "no_pone_huevos"],
        "conclusion": "es gato"
    },
    {
        "condiciones": ["tiene_plumas", "puede_volar", "es_pequeño", "tiene_pico", "pone_huevos"],
        "conclusion": "es colibri"
    }
]

def encadenamiento_hacia_adelante(hechos, reglas):
    conclusiones = []

    for regla in reglas:
        es_aplicable = True
        for condicion in regla["condiciones"]:
            if condicion.startswith("no_"):
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

conclusiones = encadenamiento_hacia_adelante(hechos, reglas)
for conclusion in conclusiones:
    print(conclusion)

    return conclusiones

conclusiones = encadenamiento_hacia_adelante(hechos, reglas)
for conclusion in conclusiones:
    print(conclusion)
