import streamlit as st
from streamlit.components.v1 import html

# --- Importar los módulos de la interfaz ---
from lenceria import render_lenceria_inputs
from amenities import render_amenities_selector

def copy_button(text_to_copy):
    """
    Genera un botón HTML que copia el texto proporcionado al portapapeles.
    """
    # Escapamos las comillas y saltos de línea para que no rompan el string de JavaScript
    escaped_text = text_to_copy.replace('`', '\\`').replace("'", "\\'").replace('\n', '\\n')

    # El código HTML y JavaScript para el botón
    button_html = f"""
    <button id="copyBtn" onclick="copyToClipboard()">
        📲 Copiar Mensaje al Portapapeles
    </button>
    <script>
    function copyToClipboard() {{
        navigator.clipboard.writeText(`{escaped_text}`).then(function() {{
            var btn = document.getElementById('copyBtn');
            btn.innerText = '✅ ¡Copiado!';
            setTimeout(function(){{ btn.innerText = '📲 Copiar Mensaje al Portapapeles'; }}, 2000);
        }}, function(err) {{
            console.error('Error al copiar: ', err);
        }});
    }}
    </script>
    """
    return html(button_html, height=50)

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
        new_stock_data = render_lenceria_inputs(stock_data, is_expanded=False)
        selected_amenities = render_amenities_selector(amenities_list)
        submitted = st.form_submit_button("Guardar y Generar Mensaje")

        if submitted:
            st.session_state['stock_data'] = new_stock_data
            st.session_state['missing_amenities'] = selected_amenities
            st.success("¡Stock guardado con éxito!")

    st.divider()
    st.header("Mensaje de WhatsApp Generado")

    final_message = generate_whatsapp_message_func(
        st.session_state['stock_data'],
        selected_apartment,
        st.session_state['missing_amenities']
    )

    st.text_area(
        "Mensaje listo para enviar (Copia el contenido):",
        value=final_message,
        height=400
    )

    copy_button(final_message)
    st.info("💡 Consejo: Haz clic en el botón de 'Copiar Mensaje' y luego pégalo directamente en WhatsApp. ¡Ya no necesitas copiar manualmente!")
