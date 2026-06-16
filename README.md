# 🚀 Project X: Multichannel Digital Content Generator

Este proyecto consiste en una aplicación web corporativa de alto rendimiento diseñada para la optimización y generación automatizada de contenido publicitario multicanal. Mediante la integración de Modelos de Lenguaje de Gran Escala (LLMs) a través de **LangChain** y **Groq**, el sistema permite adaptar la identidad de marca, el tono corporativo y la audiencia objetivo para crear piezas de copia optimizadas con soporte multimedia dinámico.

Para garantizar la portabilidad, el aislamiento del entorno y la consistencia en entornos de producción, todo el ecosistema ha sido contenerizado utilizando **Docker** y el gestor de paquetes avanzado **uv**.

---

## 🏗️ Arquitectura del Sistema y Tecnologías
La aplicación se divide en una arquitectura desacoplada orientada a servicios:
* **Frontend (Capa de Presentación):** Desarrollado en **Streamlit**, implementando un panel lateral de control paramétrico, control de estados persistentes (`st.session_state`), segregación por pestañas de trabajo e interfaces reactivas equilibradas en dos columnas.
* **Backend (Motor de IA):** Implementado con **LangChain** (`ChatPromptTemplate`) y la API de **Groq** utilizando el modelo ágil de inferencia de velocidad ultra-alta **`llama-3.1-8b-instant`**.
* **Pipeline Multimedia & Extracción Semántica:** Un segundo flujo asíncronizado con el LLM (configurado a temperatura `0.0` para máxima precisión) extrae de 2 a 3 sustantivos concretos en inglés del texto generado. Estos términos se inyectan en la API de **Pexels** para recuperar un asset visual HD idóneo de forma automatizada.
* **Gestión de Entorno:** **uv** (gestor desarrollado en Rust), asegurando tiempos de resolución de dependencias deterministas.

---

## 🛠️ Requisitos Previos

Antes de proceder con la instalación y despliegue, asegúrate de contar con las siguientes herramientas en tu máquina local:
* **Docker Desktop** en ejecución.
* Una API Key válida de **Groq Cloud**.
* Una API Key válida de **Pexels** para la recuperación automática de imágenes de stock.

---

## 📦 Configuración del Entorno Virtual Local

Si deseas ejecutar o inspeccionar el proyecto de forma nativa (sin usar contenedores), la gestión se realiza mediante las herramientas de `uv`:

```bash
# Sincronizar el entorno e instalar dependencias declaradas en el pyproject.toml
uv sync

# Ejecutar el servidor de desarrollo local
uv run streamlit run app.py

🐳 Despliegue Automatizado con Docker

La infraestructura de contenerización utiliza una estrategia de construcción multietapa (multi-stage build) optimizando el almacenamiento y la seguridad de la imagen final.
1. Variables de Entorno (.env)

Crea un archivo llamado .env en la raíz del proyecto e introduce tus credenciales correspondientes. Nota: Este archivo se encuentra excluido del control de versiones (.gitignore) por motivos de ciberseguridad.
Fragmento de código

GROQ_API_KEY=tu_api_key_de_groq_aqui
PEXELS_API_KEY=tu_api_key_de_pixels_aqui

2. Construcción de la Imagen Docker

Para empaquetar toda la estructura del proyecto, los módulos de backend y los recursos visuales, ejecuta:
Bash

docker build -t project-x-llms .

3. Ejecución del Contenedor

Arranca el contenedor mapeando el puerto del servidor web (8501) e inyectando de forma segura las variables de entorno en la memoria en tiempo de ejecución:
Bash

docker run -p 8501:8501 --env-file .env project-x-llms

Una vez levantado el servicio, accede directamente desde cualquier navegador web a la dirección local del contenedor:
👉 http://localhost:8501
🔧 Características Técnicas Clave Solucionadas

    Compilación por Capas Optimizada: El Dockerfile extrae el binario nativo desde la imagen oficial de uv, acelerando el aprovisionamiento de librerías en la capa interna de Linux (python:3.12-slim), ignorando el conflicto de versiones superiores en compilación asíncrona.

    Persistencia Local del Historial: Flujo avanzado en la memoria de la sesión (st.session_state["history"]) que almacena, estructura e indexa las publicaciones generadas en orden inverso para mostrar lo más reciente al principio del muro.

    Robustez de Identificadores (UI Stability): Resolución de conflictos de duplicados en la vista del historial. Se implementó una inyección de claves dinámicas únicas basadas en texto indexado (key=f"pills_{'-'.join(h_keys)}") en el componente st.pills, permitiendo múltiples peticiones recurrentes sobre los mismos tópicos y sectores comerciales sin degradación de la interfaz de Streamlit.

🎓 Propósito Educativo

    ⚠️ Nota legal: Este proyecto ha sido desarrollado exclusivamente con fines educativos y de investigación técnica en el ámbito del despliegue de soluciones de Inteligencia Artificial y Data Engineering dentro del marco formativo del bootcamp. Las herramientas, arquitecturas y claves de acceso empleadas se configuran bajo entornos controlados de simulación de prácticas profesionales.

##