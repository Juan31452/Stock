import streamlit as st

def render_lenceria_inputs(is_expanded=True):
    """Dibuja los campos para lencería dentro de un expansor plegable."""
    with st.expander("📝 Actualizar Cantidades de Lencería", expanded=is_expanded):
        st.info("Introduce las cantidades de lencería que has recogido.")
        
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
