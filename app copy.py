from chain import graph

import streamlit as st
import uuid

SUGGESTED_QUESTIONS = [
    "¿Qué carga horaria total tiene la Carrera de Ing. en IA?",
    "¿Cuáles son los objetivos de la Licenciatura en Ciencias de Datos?",
    "¿Qué materias del ciclo básico tiene Ingeniería Informática?",
    "¿Cuál es el perfil profesional de un egresado en IA?",
    "¿Qué diferencia hay entre Ciencia de Datos e Ingeniería en IA?",
    "¿Cómo es el cursado para quienes trabajan?",
]

st.set_page_config(page_title="Luca - Asistente UCA Track Digital", page_icon="🤖")

col1, col2 = st.columns([1, 8])
with col1:
    st.image("./assets/logo_uca.png", width=100)
with col2:
    st.markdown("# 🤖 Luca – Asistente Virtual UCA")

st.markdown("""
Bienvenido/a al chat de orientación de la **Facultad de Ingeniería y Ciencias Agrarias** de la Pontificia Universidad Católica Argentina.

Consultá sobre las carreras del *Track Digital*:
- Licenciatura en Ciencias de Datos
- Ingeniería en Inteligencia Artificial
- Ingeniería Informática

---
""")

if "thread_id" not in st.session_state or st.button("Nuevo chat 🚀"):
    st.session_state["thread_id"] = str(uuid.uuid4())
    st.session_state["messages"] = []
    st.session_state["suggested_message"] = None

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        with st.chat_message("Usuario", avatar="👤"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("Luca", avatar="🤖"):
            st.markdown(msg["content"])

st.markdown("#### ¿Querés inspiración? Probá con una de estas preguntas:")
cols = st.columns(len(SUGGESTED_QUESTIONS))
for i, q in enumerate(SUGGESTED_QUESTIONS):
    if cols[i].button(q, key=f"suggested_{i}"):
        st.session_state["suggested_message"] = q
        st.session_state["from_suggested"] = True
        st.rerun()

# Detecta input (prioridad a sugerida, si existe)
input_message = None
from_suggested = st.session_state.pop("from_suggested", False)
if st.session_state.get("suggested_message"):
    input_message = st.session_state.pop("suggested_message")
else:
    input_message = st.chat_input("Escribí tu pregunta...")

if input_message:
    st.session_state["messages"].append({"role": "user", "content": input_message})
    with st.chat_message("Usuario", avatar="👤"):
        st.markdown(input_message)

    config = {"configurable": {"thread_id": st.session_state["thread_id"]}}
    result = graph.invoke(
        {"messages": st.session_state["messages"]},
        config=config,
    )

    # Extraer la respuesta del AI (mismo parseo robusto)
    response_text = None
    if isinstance(result, dict) and "messages" in result and result["messages"]:
        for message in reversed(result["messages"]):
            if hasattr(message, "content"):
                if getattr(message, "type", None) == "ai" or getattr(message, "role", None) == "assistant" or "AIMessage" in type(message).__name__:
                    response_text = message.content
                    break
            elif isinstance(message, dict):
                if message.get("type") == "ai" or message.get("role") == "assistant":
                    response_text = message.get("content", "")
                    break
        if not response_text:
            last = result["messages"][-1]
            response_text = getattr(last, "content", None) or last.get("content", str(last))
    else:
        response_text = str(result)

    with st.chat_message("Luca", avatar="🤖"):
        st.markdown(response_text)
    st.session_state["messages"].append({"role": "assistant", "content": response_text})

    # SOLO si la pregunta fue sugerida, rerun para volver a mostrar el input
    if from_suggested:
        st.rerun()

st.markdown("""
---
👨‍🎓 **Luca** es un agente de IA de la Facultad de Ingeniería y Ciencias Agrarias (UCA).
""")
