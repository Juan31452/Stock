import streamlit as st
from amenities import render_amenities_selector

def render_amenities_interface(amenities_list, _, is_expanded=True): # El segundo argumento no se usa
    """Dibuja la interfaz para la gestión de amenities."""
    st.divider()
    st.header("Gestión de Amenities")
    selected_amenities = render_amenities_selector(amenities_list, is_expanded=is_expanded)
    return selected_amenities
