from langchain_core.documents import Document
from typing_extensions import List, TypedDict
from init import CustomChatModel
from langgraph.graph import START, StateGraph
from langchain import hub
from typing import Literal
from typing_extensions import Annotated
from langchain_core.prompts import PromptTemplate


class Search(TypedDict):
    """Search query."""

    query: Annotated[str, ..., "Search query to run."]
    section: Annotated[
        Literal["beginning", "middle", "end"],
        ...,
        "Section to query.",
    ]

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

state = State()
llm = CustomChatModel().get_model()
embeddings = CustomChatModel().get_embeddings()
vector_store = CustomChatModel().get_vector_store()
#prompt = hub.pull("rlm/rag-prompt")


template = """La tarea es ser el agente (chatbot) de la Facultad de Ingeniería y Ciencias Agrarias de la Universidad Católica Argentina.
Las preguntas de nuestros usuarios suelen hacerse en función de los programas de las carreras de Lic. en Ciencias de Datos e Ingeniería en Inteligencia Artificial.
Vamos a contestar siempre las preguntas en Español de Argentina.
Utiliza la información que te proporcionamos en el contexto para responder a la pregunta..
Si no sabes la respuesta, simplemente di que no sabes, no intentes inventar una respuesta..
Elaborá la respuesta de la manera más concisa posible, sin rodeos, evitando dar información innecesaria.
Siempre agradecé al final de la respuesta.

Contexto: {context}

Question: {question}

Helpful Answer:"""

prompt = PromptTemplate.from_template(template)
    
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}

graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()
