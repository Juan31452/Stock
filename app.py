import streamlit as st
from copy import deepcopy
from datetime import date

# --- Importar módulos ---
from data_loader import load_amenities, load_apartments
from interfaz import render_main_interface

# --- Importar datos ---
from stock_inicial import STOCK_INICIAL

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Gestión de Stock de Lencería",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Función para Cargar CSS Local ---
def local_css(file_name):
    """Carga un archivo CSS local en la aplicación Streamlit."""
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css") # Llama a la función para cargar nuestro CSS

# Inicializar o actualizar el estado del stock sin perder cantidades guardadas.
stored_stock = st.session_state.get('stock_data')
if not isinstance(stored_stock, dict):
    st.session_state['stock_data'] = deepcopy(STOCK_INICIAL)
else:
    for section, initial_items in STOCK_INICIAL.items():
        section_stock = stored_stock.setdefault(section, {})
        for item, initial_count in initial_items.items():
            section_stock.setdefault(item, initial_count)
# Inicializar la lista de amenities faltantes
if 'missing_amenities' not in st.session_state:
    st.session_state['missing_amenities'] = []

# --- Funciones de Lógica ---

def generate_whatsapp_message(stock_data, apartment_name, missing_amenities):
    """Genera el pedido de stock con el formato preparado para WhatsApp."""
    today = date.today().strftime("%d/%m/%Y")
    lines = [
        "🏠 PEDIDO 🏠",
        "",
        f"Apartamento: {apartment_name}",
        f"📅 Fecha: {today}",
        "👤 Limpiador/a:",
        "",
        "🛏️ ROPA DE CAMA",
        "",
    ]

    section_icons = {
        "Cama 180": "🔵",
        "Cama 160": "🟢",
        "Camas individuales": "🟠",
    }
    for section in ("Cama 180", "Cama 160", "Camas individuales"):
        icon = section_icons[section]
        lines.append(f"{icon} {section}")
        for item, count in stock_data[section].items():
            lines.append(f"{icon} {item}: {count}")
        lines.append("")

    lines.append("▫️ Fundas de almohada")
    for item, count in stock_data["Fundas de almohada"].items():
        lines.append(f"{item}: {count}")
    lines.extend(["", "🛁 TOALLAS"])
    lines.extend(
        f"{item}: {count}" for item, count in stock_data["Toallas"].items()
    )
    lines.extend([
        "",
        "🧴 AMENITIES Y PRODUCTOS",
        "",
        "Paño de cocina",
        "Bayeta amarilla",
    ])
    if missing_amenities:
        lines.append("")
        lines.extend(f"- {amenity}" for amenity in missing_amenities)
    lines.extend(["", "📌 OBSERVACIONES", "Sin Observaciones"])
    return "\n".join(lines)

# --- Carga de datos inicial ---
AMENITIES_LIST = load_amenities()
APARTMENT_LIST = load_apartments()

# --- Renderizar la Interfaz Principal ---
render_main_interface(st.session_state['stock_data'], AMENITIES_LIST, APARTMENT_LIST, generate_whatsapp_message)
