import streamlit as st

def render_lenceria_inputs():
    """Dibuja los campos para actualizar las cantidades de lencería."""
    st.header("Actualizar Cantidades de Lencería")
    
    new_stock_data = {}
    for item, current_count in st.session_state['stock_data'].items():
        new_stock_data[item] = st.number_input(
            f"{item}",
            min_value=0,
            value=current_count,
            key=f"input_{item}",
            step=1
        )
    return new_stock_data
