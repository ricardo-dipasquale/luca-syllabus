import os
from init import CustomChatModel
import chromadb
from langchain_community.document_loaders import PyPDFLoader

config = CustomChatModel()
llm = config.get_model()
embeddings = config.get_embeddings()
vector_store = config.get_vector_store()

docs_folder = "./docs"
all_docs = []

for filename in os.listdir(docs_folder):
    if filename.endswith(".pdf"):
        file_path = os.path.join(docs_folder, filename)
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        all_docs.extend(docs)
        print(f"{filename}: {len(docs)} documentos cargados")

print(f"Total de documentos cargados: {len(all_docs)}")

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=5000, chunk_overlap=2000, add_start_index=True
)
all_splits = text_splitter.split_documents(all_docs)

print(f"Total de splits: {len(all_splits)}")

vector_1 = embeddings.embed_query(all_splits[0].page_content)
vector_2 = embeddings.embed_query(all_splits[1].page_content)

assert len(vector_1) == len(vector_2)
print(f"Generated vectors of length {len(vector_1)}\n")
print(vector_1[:10])

ids = vector_store.add_documents(documents=all_splits)

embedding = embeddings.embed_query("Qué materias hay en el primer año / primer cuatrimestre de la Licenciatura en Ciencias de Datos?")
results = vector_store.similarity_search_by_vector(embedding)
print(results[0])

print ("Finalizado")