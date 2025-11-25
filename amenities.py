import streamlit as st

def load_amenities(filepath="Faltantes.txt"):
    """Carga la lista de amenities desde un archivo de texto."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            amenities = [line.strip() for line in f if line.strip()]
        return amenities if amenities else ["Lista de faltantes vacía o no encontrada"]
    except FileNotFoundError:
        return ["Archivo 'Faltantes.txt' no encontrado"]

def render_amenities_selector(amenities_list, is_expanded=True):
    """Dibuja el selector para los amenities faltantes dentro de un expansor."""
    with st.expander("🧺 Seleccionar Amenities Faltantes", expanded=is_expanded):
        st.info("Elige los artículos que faltan de la lista.")
        
        selected_amenities = st.multiselect(
            "Artículos faltantes:",
            options=amenities_list,
            default=st.session_state.get('missing_amenities', []),
            key="amenities_selector",
            help="Esta lista se carga desde el archivo `Faltantes.txt`."
        )
        return selected_amenities
