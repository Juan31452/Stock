import streamlit as st
from lenceria import render_lenceria_inputs

def render_lenceria_interface(stock_data):
    """Dibuja la interfaz para la gestión de lencería."""
    st.header("Gestión de Lencería")

    with st.form("lenceria_form"):
        new_stock_data = render_lenceria_inputs(stock_data, is_expanded=False)
        submitted = st.form_submit_button("Guardar Stock de Lencería")

        if submitted:
            st.session_state['stock_data'] = new_stock_data
            st.success("¡Stock de lencería guardado con éxito!")
