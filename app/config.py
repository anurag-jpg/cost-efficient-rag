from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    app_name:str="Cost-Efficient RAG"
    app_env:str="development"
    
    chroma_path:str="./storage/chroma"
    
    
    embedding_model:str=(
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    
    embedding_dimension:int=384
    
    chunk_size:int=800
    chunk_overlap:int=120
    default_top_k:int=5
    
    
    llm_provider:str="gemini"
    llm_model:str="suppprted-model"
    llm_api_key:str=""
    
    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
settings=Settings()