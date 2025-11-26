import streamlit as st
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

# Inicializar o cargar el estado del stock
if 'stock_data' not in st.session_state:
    st.session_state['stock_data'] = STOCK_INICIAL.copy()
# Inicializar la lista de amenities faltantes
if 'missing_amenities' not in st.session_state:
    st.session_state['missing_amenities'] = []

# --- Funciones de Lógica ---

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
            message += f"- {amenity}\n"
            
    return message

# --- Carga de datos inicial ---
AMENITIES_LIST = load_amenities()
APARTMENT_LIST = load_apartments()

# --- Renderizar la Interfaz Principal ---
render_main_interface(st.session_state['stock_data'], AMENITIES_LIST, APARTMENT_LIST, generate_whatsapp_message)
