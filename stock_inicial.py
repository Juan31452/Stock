from collections import OrderedDict

# --- Datos de Inventario (Puedes expandir esto) ---
# Usamos un diccionario para guardar los datos. En una app real, usarías una base de datos (como Firestore).
# Inicializamos el stock con ceros.
# Usamos OrderedDict para garantizar que el orden se mantenga siempre.
STOCK_INICIAL = OrderedDict([
    ("Sábanas Matrimonio", 0),
    ("Sábana individual", 0),
    ("Sábanas extra", 0),
    ("F. Nórdica individual", 0),
    ("F. nórdicas Matrimonio", 0),
    ("F. nórdica Extra", 0),
    ("Fundas almohadas", 0),
    ("Protector Almohada", 0),
    ("Protector Colchón", 0),
    ("Toallas Grandes", 0),
    ("Toallas Chicas", 0),
    ("Pisa pies", 0),
    ("Trapo de cocina", 0),
    ("Bayeta amarilla", 0),
])
