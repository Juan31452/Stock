import streamlit as st
import pandas as pd
from collections import OrderedDict
from datetime import date
from streamlit.components.v1 import html

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Gestión de Stock de Lencería",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Datos de Inventario (Puedes expandir esto) ---
# Usamos un diccionario para guardar los datos. En una app real, usarías una base de datos (como Firestore).
# Inicializamos el stock con ceros.
# Usamos OrderedDict para garantizar que el orden se mantenga siempre.
STOCK_INICIAL = OrderedDict([
    ("Sábanas Matrimonio", 0),
    ("Sábana individual", 0),
    ("Sábanas extra", 0),
    ("F. Nórdica individual", 0),
    ("F. nórdicas Matrimonio", 0),
    ("F. nórdica Extra", 0),
    ("Fundas almohadas", 0),
    ("Protector Almohada", 0),
    ("Protector Colchón", 0),
    ("Toallas Grandes", 0),
    ("Toallas Chicas", 0),
    ("Pisa pies", 0),
    ("Trapo de cocina", 0),
    ("Bayeta amarilla", 0),
])

# Inicializar o cargar el estado del stock
if 'stock_data' not in st.session_state:
    st.session_state['stock_data'] = STOCK_INICIAL.copy()
# Inicializar la lista de amenities faltantes
if 'missing_amenities' not in st.session_state:
    st.session_state['missing_amenities'] = []

# --- Funciones de Lógica ---

def load_apartments(filepath="apartamentos.txt"):
    """Carga la lista de apartamentos desde un archivo de texto."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Leer cada línea, quitar espacios en blanco y filtrar las vacías
            apartments = [line.strip() for line in f if line.strip()]
        return apartments if apartments else ["Lista vacía o no encontrada"]
    except FileNotFoundError:
        # Si el archivo no se encuentra, devolver una lista con un valor por defecto
        return ["Archivo 'apartamentos.txt' no encontrado"]

def load_amenities(filepath="Faltantes.txt"):
    """Carga la lista de amenities desde un archivo de texto."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            amenities = [line.strip() for line in f if line.strip()]
        return amenities if amenities else ["Lista de faltantes vacía o no encontrada"]
    except FileNotFoundError:
        return ["Archivo 'Faltantes.txt' no encontrado"]


def generate_whatsapp_message(stock_data, apartment_name, missing_amenities):
    """Genera el mensaje completo de STOCK DIARIO en formato de texto."""
    
    # Obtener la fecha actual
    today = date.today().strftime("%d/%m/%y")
    
    # 1. Encabezado
    message = f"Plantilla *STOCK DIARIO*\n"
    message += f"🏠Apartamento:\n{apartment_name}\n"
    message += f"📆Fecha:{today}\n"
    message += f"👤Limpieza: MÓNICA \n"
    message += "----------------------\n----------------------\n"
    
    # 2. Sección Lencería/Stock
    message += "🛏️ *Lencería*\n"
    for item, count in stock_data.items():
        # Añadir cada ítem de stock con su cantidad actual
        message += f"- {item}: {count}\n"
        
    # 3. Sección Amenities
    if missing_amenities:
        message += "AMENITES FALTANTES\n"
        for amenity in missing_amenities:
            # Añadir los amenities faltantes seleccionados por el usuario
            message += f"- {amenity}\n"
            
    return message

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

# --- Interfaz de Streamlit ---

st.title("Inventario de Lencería y Amenities")
st.markdown("Utiliza esta interfaz para registrar las cantidades y generar tu mensaje de **STOCK DIARIO** para WhatsApp.")

# --- Cargar y seleccionar apartamento ---
AMENITIES_LIST = load_amenities()
APARTMENT_LIST = load_apartments()
selected_apartment = st.selectbox(
    "🏠 Selecciona el Apartamento",
    options=APARTMENT_LIST,
    help="La lista se carga desde el archivo `apartamentos.txt`."
)

# --- 1. Formulario de Entrada de Datos ---
with st.form("inventory_form"):
    st.header("Actualizar Cantidades de Lencería")
    
    # Generar campos numéricos para cada ítem en el stock
    new_stock_data = {}
    for i, (item, current_count) in enumerate(st.session_state['stock_data'].items()):
        # Usamos una sola columna para mantener el orden en PC y móvil
        new_stock_data[item] = st.number_input(
            f"{item}",
            min_value=0,
            value=current_count,
            key=f"input_{item}",
            step=1
        )

    st.divider()
    st.header("Seleccionar Amenities Faltantes")
    selected_amenities = st.multiselect(
        "Elige los artículos que faltan:",
        options=AMENITIES_LIST,
        default=st.session_state['missing_amenities'],
        help="Esta lista se carga desde el archivo `Faltantes.txt`."
    )
    
    # Botón para enviar el formulario y guardar los cambios
    submitted = st.form_submit_button("Guardar Stock y Generar Mensaje")
    
    if submitted:
        # Al guardar, actualizamos el estado de la sesión
        st.session_state['missing_amenities'] = selected_amenities
        st.session_state['stock_data'] = new_stock_data
        st.success("¡Stock guardado con éxito! El mensaje de WhatsApp está listo abajo.")

# --- 2. Generación del Mensaje de Salida ---

st.divider()
st.header("Mensaje de WhatsApp Generado")

# Generar el mensaje completo con los datos guardados en el estado de la sesión
final_message = generate_whatsapp_message(
    st.session_state['stock_data'],
    selected_apartment,
    st.session_state['missing_amenities']
)

st.text_area(
    "Mensaje listo para enviar (Copia el contenido):",
    value=final_message,
    height=400
)

# --- 3. Botón de Copiar al Portapapeles (Automatización) ---

# Usamos nuestra función personalizada para crear un botón de copiado real
copy_button(final_message)

st.info("💡 Consejo: Haz clic en el botón de 'Copiar Mensaje' y luego pégalo directamente en WhatsApp. ¡Ya no necesitas copiar manualmente!")
