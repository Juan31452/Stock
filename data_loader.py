import os

def load_from_file(filepath):
    """
    Función genérica para cargar una lista de elementos desde un archivo de texto,
    eliminando líneas vacías.
    """
    if not os.path.exists(filepath):
        return [f"Archivo '{os.path.basename(filepath)}' no encontrado"]
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            items = [line.strip() for line in f if line.strip()]
        return items if items else ["Lista vacía o archivo no encontrado"]
    except Exception as e:
        return [f"Error al leer el archivo: {e}"]

def load_amenities(filepath="Faltantes.txt"):
    """Carga la lista de amenities desde un archivo de texto."""
    return load_from_file(filepath)

def load_apartments(filepath="apartamentos.txt"):
    """Carga la lista de apartamentos desde un archivo de texto."""
    return load_from_file(filepath)
