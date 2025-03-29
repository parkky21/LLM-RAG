from sentence_transformers import SentenceTransformer
import torch

class EmbeddingService:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initialize the embedding service with a chosen model
        
        Args:
            model_name (str): Name of the sentence-transformers model to use
        """
        # Using a lightweight but effective model
        self.model = SentenceTransformer(model_name)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)
    
    def get_embedding(self, text):
        """
        Get embedding vector for a text
        
        Args:
            text (str): Text to embed
            
        Returns:
            list: Embedding vector
        """
        return self.model.encode(text).tolist()
    
    def get_embeddings(self, texts):
        """
        Get embedding vectors for multiple texts
        
        Args:
            texts (list): List of texts to embed
            
        Returns:
            list: List of embedding vectors
        """
        return self.model.encode(texts).tolist()