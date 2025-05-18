from chain import graph

import streamlit as st
import uuid


SUGGESTED_QUESTIONS = [
    "¿Qué carga horaria total tiene la Carrera de Ing. en IA?",
    "¿Cuáles son los objetivos de la Licenciatura en Ciencias de Datos?",
    "¿Cuál es el año con más carga horaria de la Lic. en Ciencias de Datos?",
    "¿Cuál es el perfil profesional de un egresado en IA?",
    "¿Qué diferencia hay entre Ciencia de Datos e Ingeniería en IA?",
    "¿Cómo es el cursado para quienes trabajan?",
]

st.set_page_config(page_title="Luca - Asistente UCA Track Digital", page_icon="🤖")

# --- Logo grande, centrado ---
col1, col2, col3 = st.columns([2, 4, 2])
with col2:
    st.image("./assets/logo_uca.png", width=500)

st.markdown(
    """
    <div style='text-align: center; font-size: 2.5em; font-weight: bold; color: #2357c6; 
                margin-top: 0.1em; display: flex; align-items: center; justify-content: center; gap: 0.25em;'>
        <span style='vertical-align: middle;'>Luca</span>
        <span style='font-size:1.1em; vertical-align: middle;'>🤖</span>
    </div>
    <div style='text-align: center; font-size: 1.25em; color: #f2f2f2; margin-bottom: 1.5em; 
                margin-top: 0.5em; background:rgba(35,87,198,0.08); border-radius: 10px; padding:0.3em 0;'>
        Asistente virtual de la <b>Facultad de Ingeniería y Ciencias Agrarias</b>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# --- Sidebar ---
with st.sidebar:
    st.markdown("### ¿Querés inspiración?")
    for i, q in enumerate(SUGGESTED_QUESTIONS):
        if st.button(q, key=f"suggested_{i}"):
            st.session_state["suggested_message"] = q
            st.session_state["from_suggested"] = True
            st.rerun()
    st.markdown("---")
    if st.button("Nuevo chat 🚀"):
        st.session_state["thread_id"] = str(uuid.uuid4())
        st.session_state["messages"] = []
        st.session_state["suggested_message"] = None
        st.session_state["from_suggested"] = False
        st.rerun()
    st.markdown(
        """
        <div style='font-size:0.9em; color:#2357c6; margin-top:2em;'>
            Facultad de Ingeniería y Ciencias Agrarias, Pontificia Universidad Católica Argentina (UCA)
        </div>
        """, unsafe_allow_html=True
    )

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "suggested_message" not in st.session_state:
    st.session_state["suggested_message"] = None

if not st.session_state["messages"]:
    st.markdown(
        """
        <div style='
            text-align:center; 
            color: #2357c6; 
            margin-bottom:2em; 
            font-size:1.2em; 
            background:rgba(35,87,198,0.08); 
            border-radius:10px;
            padding: 1em 0.5em; 
            box-shadow:0 1px 8px rgba(35,87,198,0.06);'>
            <b>¡Bienvenido/a!</b> Consultá sobre las carreras del Track Digital:
            Lic. en Ciencias de Datos, Ing. en Inteligencia Artificial e Ing. Informática
        </div>
        """,
        unsafe_allow_html=True
    )

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        with st.chat_message("Usuario", avatar="👤"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("Luca", avatar="🤖"):
            st.markdown(msg["content"])

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

    if from_suggested:
        st.rerun()

st.markdown(
    """
    ---
    <div style='text-align:center; font-size:0.95em; color:#2357c6; margin-top:1em;'>
    👨‍🎓 Luca es un agente de IA de la Facultad de Ingeniería y Ciencias Agrarias (Pontificia Universidad Católica Argentina).
    </div>
    """,
    unsafe_allow_html=True
)
