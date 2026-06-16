import os
import json
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Initialize the native Groq client using the API key from the environment
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Updated to the currently supported Groq model to avoid decommission errors
MODEL_NAME = "llama-3.3-70b-versatile"

# 1. Define the Python functions (Tools)
def simular_consulta_base_datos(cliente: str) -> str:
    """Simulates a database lookup to retrieve a customer's status and current plan."""
    clientes_db = {
        "isrodam": {"plan": "Premium", "servidores": 5, "estado": "Activo"},
        "alberto": {"plan": "Básico", "servidores": 1, "estado": "Suspendido"}
    }
    datos = clientes_db.get(cliente.lower(), "Cliente no encontrado")
    return json.dumps(datos)

def calcular_coste_ampliacion(servidores_nuevos: int) -> str:
    """Calculates the monthly infrastructure cost for adding new servers."""
    precio_por_servidor = 25  # USD per server
    total = servidores_nuevos * precio_por_servidor
    return json.dumps({"coste_total_usd": total})

# Map string names to the actual executable Python functions
tools_map = {
    "simular_consulta_base_datos": simular_consulta_base_datos,
    "calcular_coste_ampliacion": calcular_coste_ampliacion
}

# 2. Specify schemas so the LLM understands when and how to call each tool
tools_spec = [
    {
        "type": "function",
        "function": {
            "name": "simular_consulta_base_datos",
            "description": "Consulta el plan actual y estado de un cliente en el sistema.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cliente": {"type": "string", "description": "Nombre del cliente a buscar."}
                },
                "required": ["cliente"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calcular_coste_ampliacion",
            "description": "Calcula el coste mensual de añadir nuevos servidores al entorno.",
            "parameters": {
                "type": "object",
                "properties": {
                    "servidores_nuevos": {"type": "integer", "description": "Número de servidores a añadir."}
                },
                "required": ["servidores_nuevos"],
            },
        },
    }
]

def run_agent():
    print("\n--- INICIO DE LA TAREA (Groq Native Agent) ---")
    
    # Establish conversational history and initial system guidelines
    messages = [
        {
            "role": "system",
            "content": "Eres un asistente técnico amigable. Utiliza las herramientas proporcionadas secuencialmente si es necesario para responder la duda."
        },
        {
            "role": "user",
            "content": "Revisa el estado del cliente 'isrodam' en la base de datos. Si está activo, calcula cuánto le costaría añadir 3 servidores más a su infraestructura."
        }
    ]
    
    # --- STEP 1: First LLM call to determine if a tool is needed ---
    print("🤖 El agente está pensando...")
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=tools_spec,
        tool_choice="auto",
        temperature=0
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    
    # --- STEP 2: Handle tool execution if requested by the model ---
    if tool_calls:
        messages.append(response_message)
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"🔧 Acción: El agente decidió ejecutar la herramienta '{function_name}' con los argumentos {function_args}")
            
            # Execute the corresponding local function
            function_to_call = tools_map[function_name]
            tool_output = function_to_call(**function_args)
            
            print(f"📥 Observación: Resultado de la herramienta -> {tool_output}")
            
            # Send tool execution results back into the context safely
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": tool_output,
            })
        
        # --- STEP 3: Second LLM call to process tool output and determine the next step ---
        print("🤖 El agente está procesando la información recibida...")
        second_response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools_spec  # Re-provide tools in case it needs to chain the calculation
        )
        
        second_message = second_response.choices[0].message
        second_tool_calls = second_message.tool_calls
        
        # Check if the LLM chains the second tool (cost calculation) based on the first outcome
        if second_tool_calls:
            messages.append(second_message)
            for tool_call in second_tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"🔧 Acción: El agente decide ejecutar la siguiente herramienta '{function_name}' con los argumentos {function_args}")
                
                function_to_call = tools_map[function_name]
                tool_output = function_to_call(**function_args)
                
                print(f"📥 Observación: Resultado de la herramienta -> {tool_output}")
                
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": tool_output,
                })
            
            # Final LLM call to generate the human-readable narrative answer
            final_response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages
            )
            print("\n--- RESPUESTA FINAL DEL AGENTE ---")
            print(final_response.choices[0].message.content)
        else:
            print("\n--- RESPUESTA FINAL DEL AGENTE ---")
            print(second_message.content)

if __name__ == "__main__":
    run_agent()