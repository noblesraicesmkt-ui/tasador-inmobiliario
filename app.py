import streamlit as st
from google import genai
from google.genai import types

# 1. CONFIGURACIÓN DE LA WEB
st.set_page_config(page_title="TasaBot Inmobiliario", page_icon="🏠")

st.title("🏠 TasaBot: Consultor de Tasaciones")
st.markdown("Herramienta exclusiva para brokers inmobiliarios.")

# Barra lateral para la API Key
with st.sidebar:
    st.title("Configuración")
    api_key = st.text_input("Ingresa tu Gemini API Key:", type="password")
    st.info("Obtén tu clave en Google AI Studio")

# 2. LÓGICA DEL AGENTE
if api_key:
    client = genai.Client(api_key=api_key)

    # Inicializar el historial de la conversación
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Mensaje de bienvenida del bot
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "¡Hola! Soy TasaBot. Vamos a tasar esa propiedad. Para empezar, ¿en qué ciudad y barrio se encuentra?"
        })

    # Mostrar mensajes previos en la pantalla
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de texto del Broker
    if prompt := st.chat_input("Escribe tu respuesta aquí..."):
        # Guardar y mostrar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Consultar a Gemini
        with st.chat_message("assistant"):
            # Configuramos el "Cerebro" y las Herramientas (Búsqueda de Google)
            config = types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                system_instruction="""Rol: Eres TasaBot, experto tasador. 
                Entrevista al broker paso a paso (UNA pregunta a la vez). 
                Pregunta: Ubicación, Tipo, Metros, Ambientes, Estado y Amenidades. 
                Al final, usa Google Search para buscar 3 testigos reales en la zona y entrega un 'Informe de Salida' con Precio de Publicación y Precio de Cierre estimado."""
            )
            
            # Formatear historial para la IA
            history = [types.Content(role=m["role"], parts=[types.Part.from_text(text=m["content"])]) for m in st.session_state.messages]
            
            # Generar respuesta
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=history,
                config=config
            )
            
            # Mostrar respuesta y guardarla
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.warning("⚠️ Por favor, ingresa tu API Key en la barra lateral izquierda para comenzar.")
