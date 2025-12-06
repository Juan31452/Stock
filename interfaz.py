import streamlit as st

from interfaz_amenities import render_amenities_interface
from interfaz_lenceria import render_lenceria_interface
from boton_copiar import copy_button

def render_main_interface(stock_data, amenities_list, apartment_list, generate_whatsapp_message_func):
    """Dibuja la interfaz principal de la aplicación."""
    st.title("Inventario de Lencería y Amenities")
    st.markdown("Utiliza esta interfaz para registrar las cantidades y generar tu mensaje de **STOCK DIARIO** para WhatsApp.")

    # Inicializar el apartamento seleccionado si no existe en el estado de sesión
    if 'selected_apartment' not in st.session_state:
        st.session_state['selected_apartment'] = apartment_list[0] if apartment_list else None

    # Usamos st.selectbox, que es ideal para listas largas y permite buscar.
    selected_apartment = st.selectbox(
        "🏠 Selecciona el Apartamento",
        options=apartment_list,
        index=apartment_list.index(st.session_state.get('selected_apartment', apartment_list[0])) if st.session_state.get('selected_apartment') in apartment_list else 0,
        help="Puedes escribir para buscar en la lista. La selección se guarda automáticamente."
    )
    # Actualizamos el estado de la sesión con la nueva selección
    st.session_state['selected_apartment'] = selected_apartment

    with st.form("main_form"):
        st.subheader("📝 Registrar Cantidades")
        st.info("Introduce las cantidades de lencería y selecciona los amenities que faltan. Luego, haz clic en 'Guardar Cambios'.")

        # --- Renderizar la interfaz de lencería (ahora devuelve los datos) ---
        new_stock_data = render_lenceria_interface(stock_data)

        # --- Renderizar la interfaz de amenities (ahora devuelve la selección) ---
        selected_amenities = render_amenities_interface(amenities_list, generate_whatsapp_message_func)

        submitted = st.form_submit_button("💾 Guardar Cambios")
        if submitted:
            st.session_state['stock_data'] = new_stock_data
            st.session_state['missing_amenities'] = selected_amenities
            st.success("¡Stock y amenities guardados con éxito!")

    st.divider()
    st.header("Mensaje de WhatsApp Generado")

    final_message = generate_whatsapp_message_func(
        st.session_state.get('stock_data', {}),
        selected_apartment, # El apartamento seleccionado se mantiene
        st.session_state.get('missing_amenities', []) # Usamos los amenities guardados en la sesión
    )

    st.text_area(
        "Mensaje listo para enviar (Copia el contenido):",
        value=final_message,
        height=400
    )

    copy_button(final_message)
    st.info("💡 Consejo: Haz clic en el botón de 'Copiar Mensaje' y luego pégalo directamente en WhatsApp. ¡Ya no necesitas copiar manualmente!")
