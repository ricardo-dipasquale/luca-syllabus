import getpass
import os
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_chroma import Chroma

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

llm_model="gpt-4o-mini"
embedding_model="text-embedding-3-large"
model_provider="openai"

class CustomChatModel:
    
    llm = init_chat_model(llm_model, model_provider=model_provider)
    embeddings = OpenAIEmbeddings(model=embedding_model)
    #vector_store = InMemoryVectorStore(embeddings)
    vector_store = Chroma(
        collection_name="TrackDigital",
        embedding_function=embeddings,
        persist_directory="./db",  
    )

    def get_model(self):
        return self.llm
    
    def get_embeddings(self):
        return self.embeddings

    def get_vector_store(self): 
        return self.vector_store
      
    
