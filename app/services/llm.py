from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class LLMService:
    def __init__(self, model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        """
        Initialize the LLM service
        
        Args:
            model_name (str): Model to use for text generation
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            # low_cpu_mem_usage=True,
            device_map="auto"
        )
    
    def generate_response(self, prompt, max_length=1024):
        """
        Generate a response for a given prompt
        
        Args:
            prompt (str): Prompt for text generation
            max_length (int): Maximum length of generated text
            
        Returns:
            str: Generated response
        """
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_length=max_length,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    
    def generate_code(self, function_metadata, additional_context=None):
        """
        Generate executable Python code for a function
        
        Args:
            function_metadata (dict): Metadata of the function to execute
            additional_context (str, optional): Any additional context or parameters
            
        Returns:
            str: Generated Python code
        """
        # Construct a prompt that instructs the model to generate executable Python code
        prompt = f"""
        Generate Python code to call the following function:
        
        Function name: {function_metadata['name']}
        Module: {function_metadata['module']}
        Signature: {function_metadata['signature']}
        Description: {function_metadata['docstring']}
        
        {f'Additional context: {additional_context}' if additional_context else ''}
        
        The code should:
        1. Import the function from the correct module
        2. Include proper error handling
        3. Be executable as a standalone script
        4. Follow PEP 8 style guidelines
        
        Return only the Python code without any explanations.
        ```python
        """
        
        response = self.generate_response(prompt)
        
        # Extract code from response if needed
        code = response.split("```python")[-1].split("```")[0].strip()
        if not code:
            code = response.strip()
            
        return code