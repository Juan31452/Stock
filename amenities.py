import streamlit as st
import os

def load_amenities(filepath="Faltantes.txt"):
    """Carga la lista de amenities desde un archivo de texto."""
    try:
        # Usar os.path.join para construir la ruta es más seguro
        with open(filepath, 'r', encoding='utf-8') as f:
            amenities = [line.strip() for line in f if line.strip()]
        return amenities if amenities else ["Lista de faltantes vacía o no encontrada"]
    except FileNotFoundError:
        return ["Archivo 'Faltantes.txt' no encontrado"]

def render_amenities_selector(amenities_list, is_expanded=True):
    """Dibuja el selector para los amenities faltantes dentro de un expansor."""
    with st.expander("🧺 Seleccionar Amenities Faltantes", expanded=is_expanded):
        st.info("Marca los artículos que faltan de la lista.")
        
        selected_amenities = []
        # Obtenemos los amenities que ya estaban seleccionados para mantener el estado
        previously_selected = st.session_state.get('missing_amenities', [])

        # Creamos un checkbox para cada amenity en la lista
        for amenity in amenities_list:
            # El valor por defecto del checkbox es True si el amenity ya estaba seleccionado
            if st.checkbox(amenity, value=(amenity in previously_selected)):
                selected_amenities.append(amenity)

        return selected_amenities
