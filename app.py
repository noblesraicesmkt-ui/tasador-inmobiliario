import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="TasaBot Inmobiliario", page_icon="🏠")
st.title("🏠 TasaBot: Consultor de Tasaciones")

with st.sidebar:
    st.title("Configuración")
    api_key = st.text_input("Ingresa tu Gemini API Key:", type="password")

if api_key:
    try:
        # Quitamos la especificación de versión para que Google elija la correcta
        client = genai.Client(api_key=api_key)
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.messages.append({"role": "assistant", "content": "¡Hola! Soy TasaBot. Para empezar la tasación, ¿en qué ciudad y barrio se encuentra la propiedad?"})

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Responde aquí..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # Cambiamos a 1.5-pro que tiene mayor disponibilidad
                response = client.models.generate_content(
                    model="gemini-1.5-pro", 
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction="Eres TasaBot, tasador experto. Entrevista al broker una pregunta a la vez."
                    )
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Ajustando conexión... por favor intenta de nuevo en 5 segundos. (Error: {e})")
else:
    st.warning("⚠️ Ingresa tu API Key en la barra lateral para comenzar.")
