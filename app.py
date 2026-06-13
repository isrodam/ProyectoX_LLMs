from dotenv import load_dotenv
import streamlit as st
from main import generate_social_media_content

# --- ENVIRONMENT CONFIGURATION ---
# Securely load operational infrastructure environment variables
load_dotenv()

# --- WEB PLATFORM VIEWPORT STANDARDS ---
# Enforce high-performance wide screen rendering parameters at 100% zoom
st.set_page_config(
    page_title="Digital Content AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INJECT CUSTOM CSS FOR TYPOGRAPHY AND LAYOUT BALANCE ---
# Explicitly force legible input text sizes and optimize layout constraints
st.markdown(
    """
    <style>
        /* Force highly visible typography size inside text input areas */
        .stTextArea textarea {
            font-size: 1.1rem !important;
            color: #1E293B !important;
        }
        /* Optimize block containers to minimize vertical white spaces */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 1rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- MULTIMODAL CONTENT SESSION HISTORY STORAGE ---
# Verify if the global history array key is missing from the active session context.
# If true, initialize an empty list to accumulate generated media structures safely.
if "history" not in st.session_state:
    st.session_state["history"] = []

# --- APPLICATION CORPORATE HEADERS ---
st.title("🚀 Generador de Contenido con IA")
st.caption("⚡ Entorno corporativo de alto rendimiento para optimización de copy multicanal")

st.markdown("<hr style='border:1px solid #4A90E2; margin-top: 5px; margin-bottom: 20px;'>", unsafe_allow_html=True)

# --- SIDEBAR CONFIGURATION PANEL ---
# Construct isolated vertical workflow lane for input capture and hyperparameter control
with st.sidebar:
    st.markdown("### ⚙️ Panel de Control")
    
    # Section 1: Brand Identity parameters
    st.markdown(
        """
        <div style="background-color: #f0f2f6; padding: 12px; border-radius: 8px; border-left: 5px solid #4A90E2; margin-bottom: 15px;">
            <h4 style="margin-top:0; color: #1E3A8A; font-size: 1rem; margin-bottom:4px;">🏢 Identidad de Marca</h4>
            <p style="font-size: 0.75rem; color: #555; margin-bottom: 0px;">Define los rasgos base de la empresa para alinear el LLM.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    brand_name = st.text_input("Nombre de la Marca:", value="Digital Content Marketing S.L.")
    brand_industry = st.text_input("Sector de la Empresa:", value="Digital Marketing and Social Media Growth")
    brand_tone = st.text_input("Tono de Voz Corporativo:", value="Professional, engaging, authoritative yet accessible")
    
    # Section 2: Distribution and Generation Hyperparameters
    st.markdown(
        """
        <div style="background-color: #f0f2f6; padding: 12px; border-radius: 8px; border-left: 5px solid #10B981; margin-top: 15px; margin-bottom: 15px;">
            <h4 style="margin-top:0; color: #065F46; font-size: 1rem; margin-bottom:4px;">🎛️ Parámetros de Distribución</h4>
            <p style="font-size: 0.75rem; color: #555; margin-bottom: 0px;">Ajusta los criterios del canal y aleatoriedad del modelo.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    platform = st.selectbox("Plataforma de Destino:", ["LinkedIn", "Twitter/X", "Instagram", "Facebook", "Blog Corporativo"])
    audience = st.text_input("Audiencia Objetivo (Target):", value="Tech Founders and Chief Technology Officers (CTOs)")
    language = st.selectbox("Idioma de Salida:", ["Español", "English", "Français"])
    length = st.selectbox("Extensión del Contenido:", ["Corto (~50 palabras)", "Mediano (~150 palabras)", "Largo (~300 palabras)"])
    temperature = st.slider("Temperatura (Creatividad):", min_value=0.0, max_value=1.0, value=0.7, step=0.05)


# --- CENTRAL WORKSPACE LAYOUT DEFINITION ---
# Instantiate professional navigation tabs to decouple the active generator from historical logs
tab_generator, tab_history = st.tabs(["🚀 Generador Activo", "🗂️ Historial de Sesión"])

# LOGIC AND UI FOR TAB 1: THE ACTIVE GENERATOR
with tab_generator:
    topic = st.text_area(
        "¿Sobre qué quieres hablar hoy?",
        placeholder="Escribe el tema central, ideas clave o un borrador del mensaje...",
        height=120
    )
    
    submit_button = st.button("🚀 Generar Publicación de Alto Impacto", use_container_width=True)
    
    if submit_button:
        if not topic.strip():
            st.warning("⚠️ Por favor, introduce un tema o descripción para poder inicializar el pipeline.")
        else:
            with st.status("🛸 Sincronizando componentes y orquestando modelos...", expanded=True) as status:
                # Orchestrate execution flow towards the backend controller logic in main.py
                generated_post, image_url, keywords, photographer = generate_social_media_content(
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
                
                # --- APPEND CURRENT PIPELINE OUTPUT TO STORAGE LAYER ---
                st.session_state["history"].append({
                    "topic": topic,
                    "post_text": generated_post,
                    "image_url": image_url,
                    "keywords": keywords,
                    "photographer": photographer
                })
            
            # --- ACTIVE OUTPUT VISUALIZATION LAYOUT ---
            st.markdown("### 📋 Copiar Contenido Generado")
            with st.container(border=True):
                # Balanced two-column structural layout wrapper (Texto Izquierda / Imagen Derecha)
                col1, col2 = st.columns([1, 1])
                
                # Left Column: Copywriting content display
                with col1:
                    st.markdown(generated_post)
                
                # Right Column: Visual stock asset rendering and keywords tracking
                with col2:
                    if image_url:
                        st.image(image_url, width=400)
                        st.caption(f"📷 Foto por **{photographer}** en Pexels")
                        
                        st.write("")
                        st.markdown("##### 🔍 Búsqueda Semántica de Imagen")
                        list_of_keys = [k.strip() for k in keywords.split(",") if k.strip()]
                        st.pills("Términos extraídos por la IA:", list_of_keys)
                    else:
                        st.info("ℹ️ No se encontró una imagen de stock idónea para este tema de publicación.")

# LOGIC AND UI FOR TAB 2: THE HISTORICAL LOGS VIEW
with tab_history:
    st.markdown("### 🗂️ Registro Stack de Publicaciones Guardadas")
    st.caption("Consulta y recupera el contenido generado durante la sesión de trabajo activa.")
    st.write("")
    
    # Evaluate persistent memory boundaries before structural compilation
    if not st.session_state["history"]:
        st.info("ℹ️ No se registran publicaciones almacenadas en la sesión actual. Genera contenido para activar el histórico.")
    else:
        # Loop over historical arrays in reverse sequence to showcase real-time outputs at the top
        for idx, item in enumerate(reversed(st.session_state["history"])):
            with st.container(border=True):
                # Setup a symmetric inner layout for the historical card component
                h_col1, h_col2 = st.columns([1, 1])
                
                with h_col1:
                    st.markdown(f"#### 📌 Tema: {item['topic']}")
                    st.markdown(item["post_text"])
                    
                with h_col2:
                    if item["image_url"]:
                        st.image(item["image_url"], width=350)
                        st.caption(f"📷 por **{item['photographer']}**")
                        
                        st.write("")
                        h_keys = [k.strip() for k in item["keywords"].split(",") if k.strip()]
                        st.pills(f"Keywords utilizadas:", h_keys, key=f"pills_{'-'.join(h_keys)}")
                
                st.markdown("<hr style='border:0.5px dashed #ccc; margin: 15px 0;'>", unsafe_allow_html=True)