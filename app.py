from dotenv import load_dotenv
import streamlit as st
from main import generate_social_media_content

# Load environment variables from the secure .env file
load_dotenv()

# Set professional layout configuration for the web platform
st.set_page_config(
    page_title="Digital Content AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Application titles and corporate headers
st.title("🚀 Generador de Contenido con Inteligencia Artificial")
st.caption("⚡ Entorno corporativo de alto rendimiento para optimización de copy multicanal")

st.markdown("<hr style='border:1px solid #4A90E2; margin-top: 0px; margin-bottom: 20px;'>", unsafe_allow_html=True)

# Sidebar layout: Configuration panel for brand context and hyperparameters
with st.sidebar:
    st.markdown("### ⚙️ Panel de Control")
    
    # Section 1: Brand Identity parameters
    st.markdown(
        """
        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #4A90E2; margin-bottom: 20px;">
            <h4 style="margin-top:0; color: #1E3A8A; font-size: 1.1rem;">🏢 Identidad de Marca</h4>
            <p style="font-size: 0.8rem; color: #555; margin-bottom:0;">Configura el contexto base de la empresa para orientar a la IA.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    brand_name = st.text_input("📋 Nombre de la Marca", value="Digital Content Marketing S.L.")
    brand_industry = st.text_input("🏭 Sector de la Empresa", value="Marketing Digital y Crecimiento en Redes Sociales")
    brand_tone = st.text_input("🗣️ Tono de Voz", value="Profesional, atractivo, autoritario pero accesible")
    
    # Section 2: Model advanced configuration inputs
    st.markdown(
        """
        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #FF9F43; margin-top: 20px; margin-bottom: 20px;">
            <h4 style="margin-top:0; color: #A04000; font-size: 1.1rem;">⚙️ Configuración Avanzada</h4>
            <p style="font-size: 0.8rem; color: #555; margin-bottom:0;">Ajusta el comportamiento del modelo de lenguaje.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    temperature = st.slider("🌡️ Temperatura (Creatividad)", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    language = st.selectbox("🌐 Idioma de Destino", ["Español", "Inglés", "Portugués", "Francés", "Alemán"])
    length = st.selectbox("📏 Longitud del Post", ["Corto (~50 palabras)", "Mediano (~150 palabras)", "Largo (~300 palabras)"])

# Main interface layout: Post specifications and workspace setup
st.info("📝 **Área de Trabajo:** Define los parámetros específicos del post que deseas generar a continuación.")

topic = st.text_area("✍️ ¿Cuál es el tema de tu publicación?", placeholder="Ej. La importancia de las tuberías de datos automatizadas en empresas emergentes")

col1, col2 = st.columns(2)

with col1:
    platform = st.selectbox(
        "📱 Plataforma de Destino",
        ["LinkedIn", "Twitter/X", "Instagram", "Artículo de Blog"]
    )

with col2:
    audience = st.text_input("🎯 Público Objetivo", value="Fundadores Tecnológicos y Directores de Tecnología (CTOs)")

st.write("") 

# Execution block: Form validation and modular generation trigger
if st.button("✨ Generar Publicación de Alto Impacto", use_container_width=True):
    # Field validation to guarantee programmatic safety before API connection
    if not topic.strip():
        st.error("⚠️ Por favor, introduce un tema para la publicación antes de generar.")
    else:
        # Contextual loader container for rendering API processing workflows
        with st.status("🤖 El motor de IA está procesando los prompts paramétricos...", expanded=True) as status:
            st.write("🔗 Conectando con el pipeline modular...")
            st.write("🧠 Inyectando variables avanzadas y de marca...")
            
            generated_post = generate_social_media_content(
                brand_name=brand_name,
                brand_industry=brand_industry,
                brand_tone=brand_tone,
                topic=topic,
                platform=platform,
                audience=audience,
                temperature=temperature,
                language=language,
                length=length
            )
            status.update(label="🎉 ¡Contenido optimizado por Llama 3.1 con éxito!", state="complete", expanded=False)
            
        # UI visualization block for the final generated output string
        st.markdown("### 📋 Copiar Contenido Generado")
        with st.container(border=True):
            st.markdown(generated_post)