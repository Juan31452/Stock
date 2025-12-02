import streamlit as st
from amenities import render_amenities_selector

def render_amenities_interface(amenities_list, _): # El segundo argumento no se usa, pero se mantiene por consistencia
    """Dibuja la interfaz para la gestión de amenities."""
    st.divider()
    st.header("Gestión de Amenities")

    with st.form("amenities_form"):
        selected_amenities = render_amenities_selector(amenities_list)
        submitted = st.form_submit_button("Guardar Selección de Amenities")

        if submitted:
            st.session_state['missing_amenities'] = selected_amenities
            st.success("¡Selección de amenities guardada!")
