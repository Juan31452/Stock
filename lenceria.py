import streamlit as st

def render_lenceria_inputs(is_expanded=True):
    """Dibuja los campos para lencería en dos columnas dentro de un expansor plegable."""
    with st.expander("📝 Actualizar Cantidades de Lencería", expanded=is_expanded):
        st.info("Introduce las cantidades de lencería que has recogido.")
        
        new_stock_data = {}
        
        # Crear dos columnas para el grid
        col1, col2 = st.columns(2)
        
        # Distribuir los campos de entrada entre las dos columnas
        items = list(st.session_state['stock_data'].items())
        for i, (item, current_count) in enumerate(items):
            # Los elementos pares van a la columna 1
            if i % 2 == 0:
                with col1:
                    new_stock_data[item] = st.number_input(
                        f"{item}",
                        min_value=0,
                        value=current_count,
                        key=f"input_{item}",
                        step=1
                    )
            # Los elementos impares van a la columna 2
            else:
                with col2:
                    new_stock_data[item] = st.number_input(f"{item}", min_value=0, value=current_count, key=f"input_{item}", step=1)

        return new_stock_data
