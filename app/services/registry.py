import inspect
from app.models.database import VectorDatabase
from app.functions import application, system, utilities

class FunctionRegistry:
    def __init__(self):
        self.db = VectorDatabase()
        self.modules = {
            "application": application,
            "system": system,
            "utilities": utilities
        }
        self.functions = {}
        self._populate_registry()
    
    def _populate_registry(self):
        """Populate the registry with all available functions"""
        # Clear existing collection
        try:
            self.db.client.delete_collection("function_registry")
            self.db.collection = self.db.client.create_collection("function_registry")
        except:
            pass

        # For each module
        for module_name, module in self.modules.items():
            # Get all functions in the module
            for name, obj in inspect.getmembers(module, inspect.isfunction):
                if not name.startswith('_'):  # Skip private functions
                    # Store function reference
                    self.functions[f"{module_name}.{name}"] = obj
                    
                    # Extract description from docstring
                    doc = obj.__doc__ or ""
                    description = doc.strip().split('\n')[0] if doc else f"Function to {name.replace('_', ' ')}"
                    
                    # Add to vector DB
                    self.db.add_function(obj, description, module_name)
    
    def get_function(self, function_id):
        """Get a function by its ID"""
        return self.functions.get(function_id)
    
    def search(self, query):
        """Search for functions matching the query"""
        results = self.db.search_functions(query)
        return results
    
    def execute_function(self, function_id, args=None, kwargs=None):
        """Execute a function by its ID with optional arguments"""
        args = args or []
        kwargs = kwargs or {}
        
        func = self.get_function(function_id)
        if func:
            try:
                return {"success": True, "result": func(*args, **kwargs)}
            except Exception as e:
                return {"success": False, "error": str(e)}
        return {"success": False, "error": "Function not found"}