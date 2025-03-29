import chromadb
from chromadb.config import Settings
import os
import json
import inspect
import importlib
from app.functions import application, system, utilities

class VectorDatabase:
    def __init__(self, persist_directory="chroma_db"):
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        self.collection = self.client.get_or_create_collection("function_registry")
        
    def add_function(self, function, description, module_name):
        """Add a function to the vector database"""
        # Get function signature details
        signature = str(inspect.signature(function))
        doc = function.__doc__ or ""
        source = inspect.getsource(function)
        
        # Metadata
        metadata = {
            "name": function.__name__,
            "module": module_name,
            "signature": signature,
            "docstring": doc.strip(),
            "source": source,
        }
        
        # Create documents for embedding
        document = f"{function.__name__}{signature}\n{doc}\n{description}"
        
        # Add to collection
        self.collection.add(
            documents=[document],
            metadatas=[metadata],
            ids=[f"{module_name}.{function.__name__}"]
        )
    
    def search_functions(self, query, n_results=3):
        """Search for functions matching the query"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return results