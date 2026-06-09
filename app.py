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
            <p style="font-size: 0.8rem; color: #555; margin-bottom: 10px;">Configura el contexto base de la empresa para orientar a la IA.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    brand_name = st.text_input("Nombre de la Marca:", value="Digital Content Marketing S.L.")
    brand_industry = st.text_input("Sector de la Empresa:", value="Marketing Digital y Crecimiento en Redes")
    brand_tone = st.text_area(
        "Tono de Voz:",
        value="Profesional, atractivo, autoritario pero accesible y enfocado en aportar valor técnico."
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section 2: Advanced Technical Model Hyperparameters
    st.markdown(
        """
        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #10B981; margin-bottom: 20px;">
            <h4 style="margin-top:0; color: #065F46; font-size: 1.1rem;">⚙️ Configuración Avanzada</h4>
            <p style="font-size: 0.8rem; color: #555; margin-bottom: 10px;">Ajusta el comportamiento del modelo de lenguaje.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    temperature = st.slider("Temperatura (Creatividad):", min_value=0.0, max_value=1.0, value=0.7, step=0.05)

# Main Workspace Layout for post context ingestion
st.markdown("### 📝 Área de Trabajo")
st.info("Define los parámetros específicos del post que deseas generar a continuación.")

# Structural arrangement using dual columns for the main form factors
col_input1, col_input2 = st.columns(2)

with col_input1:
    topic = st.text_area(
        "¿Cuál es el tema de tu publicación?",
        placeholder="Ej. La importancia de las tuberías de datos automatizadas en empresas emergentes"
    )
    platform = st.selectbox("Plataforma de Destino:", ["LinkedIn", "Twitter/X", "Instagram", "Facebook"])

with col_input2:
    language = st.selectbox("Idioma de Destino:", ["Español", "English", "Français"])
    length = st.selectbox("Longitud del Post:", ["Corto (~50 palabras)", "Mediano (~150 palabras)", "Largo (~300 palabras)"])
    audience = st.text_input("Público Objetivo:", value="Fundadores Tecnológicos y Directores de Tecnología (CTOs)")

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
            
            # Apply Python tuple unpacking to capture both individual data streams from the backend execution
            post_text, image_url = generate_social_media_content(
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
            
        # UI visualization block for the final generated multi-modal content layout
        st.markdown("### 📋 Copiar Contenido Generado")
        with st.container(border=True):
            # Instantiate a balanced two-column structural layout wrapper (50% / 50%)
            col1, col2 = st.columns([1, 1])
            
            # Left Column: Defensive multi-modal rendering for the automated stock photo asset
            with col1:
                if image_url:
                    # Render the dynamic media asset URL securely to block red syntax faults
                    st.image(image_url, use_container_width=True, caption=f"Visual asset fetched for: {topic}")
                else:
                    # Fallback visual state if the Pexels search loop yielded no matching resources
                    st.info("ℹ️ No se encontró una imagen de stock idónea para este tema de publicación.")
            
            # Right Column: Presenting the high-converting copy output and strategic hashtags
            with col2:
                st.markdown(post_text)