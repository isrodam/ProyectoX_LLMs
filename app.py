# Import packages for environment variables
from dotenv import load_dotenv

# Load environment variables from the local secure .env file
load_dotenv()

# Import the Streamlit library for building the web user interface
import streamlit as st

# SET PAGE CONFIGURATION FIRST: Optimize layout for full-screen readability
st.set_page_config(
    page_title="Digital Content AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import the core content generation function from our internal modular pipeline
from main import generate_social_media_content

# Render the main application title on the web interface with a custom icon
st.title("🚀 Generador de Contenido con Inteligencia Artificial")
st.caption("⚡ Entorno corporativo de alto rendimiento para optimización de copy multicanal")

# CORRECCIÓN: Usamos el nombre de parámetro correcto para la línea divisoria
st.markdown("<hr style='border:1px solid #4A90E2; margin-top: 0px; margin-bottom: 20px;'>", unsafe_allow_html=True)

# Create a professional sidebar for corporate brand identity configuration
with st.sidebar:
    st.markdown("### ⚙️ Panel de Control")
    
    # Advanced styling with the corrected parameter
    st.markdown(
        """
        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #4A90E2; margin-bottom: 20px;">
            <h4 style="margin-top:0; color: #1E3A8A; font-size: 1.1rem;">🏢 Identidad de Marca</h4>
            <p style="font-size: 0.8rem; color: #555; margin-bottom:0;">Configura el contexto base de la empresa para orientar a la IA.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Inputs placed cleanly inside the sidebar hierarchy
    brand_name = st.text_input("📋 Nombre de la Marca", value="Digital Content Marketing S.L.")
    brand_industry = st.text_input("🏭 Sector de la Empresa", value="Marketing Digital y Crecimiento en Redes Sociales")
    brand_tone = st.text_input("🗣️ Tono de Voz", value="Profesional, atractivo, autoritario pero accesible")

# Create the main content area with a professional info container
st.info("📝 **Área de Trabajo:** Define los parámetros específicos del post que deseas generar a continuación.")

# Main text input area for the topic
topic = st.text_area("✍️ ¿Cuál es el tema de tu publicación?", placeholder="Ej. La importancia de las tuberías de datos automatizadas en empresas emergentes")

# Split the layout into two columns for platform and audience selectors
col1, col2 = st.columns(2)

with col1:
    platform = st.selectbox(
        "📱 Plataforma de Destino",
        ["LinkedIn", "Twitter/X", "Instagram", "Artículo de Blog"]
    )

with col2:
    audience = st.text_input("🎯 Público Objetivo", value="Fundadores Tecnológicos y Directores de Tecnología (CTOs)")

st.write("") # Spatial padding

# Create a trigger button to execute the content generation process
if st.button("✨ Generar Publicación de Alto Impacto", use_container_width=True):
    
    # Modern status container that gives an ultra-professional look while processing
    with st.status("🤖 El motor de IA está procesando los prompts paramétricos...", expanded=True) as status:
        st.write("🔗 Conectando con el pipeline modular...")
        st.write("🧠 Inyectando variables de marca y público objetivo...")
        
        # Execute the modular core function with arguments collected from the web form
        generated_post = generate_social_media_content(
            brand_name=brand_name,
            brand_industry=brand_industry,
            brand_tone=brand_tone,
            topic=topic,
            platform=platform,
            audience=audience
        )
        status.update(label="🎉 ¡Contenido optimizado por Llama 3.1 con éxito!", state="complete", expanded=False)
        
    # Visual container designed like a real canvas card for reading copy comfortably
    st.markdown("### 📋 Copiar Contenido Generado")
    with st.container(border=True):
        st.markdown(generated_post)