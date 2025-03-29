from fastapi import FastAPI, HTTPException, Depends, Request,status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid
import inspect

from app.services.registry import FunctionRegistry
from app.services.code_generator import CodeGenerator
from app.services.context import SessionContext

# Initialize FastAPI app
app = FastAPI(
    title="Function Execution API",
    description="API for executing automation functions using LLM+RAG",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
registry = FunctionRegistry()
code_generator = CodeGenerator()

# Session storage
sessions = {}

# Define request and response models
class ExecuteRequest(BaseModel):
    prompt: str
    session_id: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

class ExecuteResponse(BaseModel):
    function: str
    code: str
    execution_result: Optional[Dict[str, Any]] = None
    context: Optional[str] = None

# Dependency to get session context
async def get_session(request: Request):
    session_id = request.query_params.get('session_id')
    
    if not session_id:
        # Generate new session ID
        session_id = f"session_{str(uuid.uuid4())}"
        
    # Get or create session
    if session_id not in sessions:
        sessions[session_id] = SessionContext(session_id)
    
    return sessions[session_id]

@app.post("/execute", response_model=ExecuteResponse)
async def execute_function(
    request: ExecuteRequest,
    session: SessionContext = Depends(get_session)
):
    """
    Execute a function based on the natural language prompt
    """
    try:
        # Get context from previous interactions
        context_summary = session.get_context_summary()
        
        # Enhance the prompt with context if available
        enhanced_prompt = request.prompt
        if context_summary and "No previous interactions" not in context_summary:
            enhanced_prompt = f"{request.prompt}\nContext from previous interactions:\n{context_summary}"
        
        # Search for the most relevant function
        search_results = registry.search(enhanced_prompt)
        
        if not search_results or not search_results['metadatas'] or not search_results['metadatas'][0]:
            raise HTTPException(status_code=404, detail="No matching function found")
        
        # Get the best match
        function_metadata = search_results['metadatas'][0][0]
        function_id = f"{function_metadata['module']}.{function_metadata['name']}"
        
        # Generate code for the function
        code = code_generator.generate_function_code(function_metadata, request.prompt)
        
        # Execute the function if parameters are provided
        execution_result = None
        if request.parameters:
            kwargs = request.parameters
            execution_result = registry.execute_function(function_id, kwargs=kwargs)
        
        # Store the interaction in session context
        session.add_interaction(
            request.prompt,
            {
                'function': function_id,
                'execution_result': execution_result
            }
        )
        
        # Return response
        return ExecuteResponse(
            function=function_id,
            code=code,
            execution_result=execution_result,
            context=context_summary
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/functions")
async def list_functions():
    """
    List all available functions in the registry
    """
    functions = []
    for function_id, func in registry.functions.items():
        module, name = function_id.split('.')
        signature = str(inspect.signature(func))
        doc = func.__doc__ or ""
        description = doc.strip().split('\n')[0] if doc else f"Function to {name.replace('_', ' ')}"
        
        functions.append({
            "id": function_id,
            "name": name,
            "module": module,
            "signature": signature,
            "description": description
        })
    
    return {"functions": functions}

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)