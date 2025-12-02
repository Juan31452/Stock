from streamlit.components.v1 import html

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
