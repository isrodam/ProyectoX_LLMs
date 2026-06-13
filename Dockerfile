# --- BASE INFRASTRUCTURE ---
# Use an official lightweight Python base image compatible with system requirements
FROM python:3.12-slim

# --- SYSTEM ENVIRONMENT VARIABLES ---
# Ensure Python outputs everything directly to the terminal without buffering
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:$PATH"

# --- WORK DIRECTORY COMPILATION ---
# Establish the isolated operational workspace inside the container
WORKDIR /app

# --- PACKAGE MANAGER OVERSIGHT ---
# Copy the official high-performance 'uv' binary directly from its verified image layer
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# --- CACHE-OPTIMIZED DEPENDENCY SYNC ---
# Copy only the dependency definition files to leverage Docker layer caching
COPY pyproject.toml /app/

# Synchronize project dependencies, automatically installing the required Python version
RUN uv pip install --system -r pyproject.toml

# --- SOURCE CODE INTEGRATION ---
# Copy the remaining codebase into the application layer context
COPY . /app/

# --- PORT NETWORK EXPOSURE ---
# Expose Streamlit's default network communication layer port
EXPOSE 8501

# --- RUNTIME EXECUTION GATEWAY ---
# Configure health checks and run the Streamlit frontend layer on container startup
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]