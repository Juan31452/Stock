import streamlit as st
from lenceria import render_lenceria_inputs

def render_lenceria_interface(stock_data, is_expanded=False):
    """Dibuja la interfaz para la gestión de lencería."""
    st.header("Gestión de Lencería")
    new_stock_data = render_lenceria_inputs(stock_data, is_expanded=is_expanded)
    return new_stock_data
