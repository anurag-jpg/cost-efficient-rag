from dataclasses import dataclass


@dataclass
class LoadedDocument:
    source:str
    content:str
    content_hash:str
    
@dataclass
class DocumentChunk:
    id:str
    source:str
    content:str
    chunk_index:int
    content_hash:str    