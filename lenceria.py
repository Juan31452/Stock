import streamlit as st

def render_lenceria_inputs(stock_data, is_expanded=True):
    """Dibuja los campos para lencería en dos columnas dentro de un expansor plegable."""
    with st.expander("📝 Actualizar Cantidades de Lencería", expanded=is_expanded):
        st.info("Introduce las cantidades de lencería que has recogido.")

        new_stock_data = {}
        section_icons = {
            "Cama 180": "🔵",
            "Cama 160": "🟢",
            "Camas individuales": "🟠",
        }

        for section, items in stock_data.items():
            title = (
                f"{section_icons[section]} {section}"
                if section in section_icons
                else section
            )
            st.markdown(f"**{title}**")
            section_data = {}
            columns = st.columns(2)
            for index, (item, current_count) in enumerate(items.items()):
                with columns[index % 2]:
                    section_data[item] = st.number_input(
                        item,
                        min_value=0,
                        value=current_count,
                        key=f"input_{section}_{item}",
                        step=1,
                    )
            new_stock_data[section] = section_data
        return new_stock_data
