from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime

class FunctionMetadata(BaseModel):
    """Metadata about a function"""
    name: str
    module: str
    signature: str
    docstring: str
    source: str

class ExecutionRequest(BaseModel):
    """Request to execute a function"""
    function_id: str
    args: Optional[List[Any]] = Field(default_factory=list)
    kwargs: Optional[Dict[str, Any]] = Field(default_factory=dict)

class ExecutionResponse(BaseModel):
    """Response from function execution"""
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time: float

class InteractionRecord(BaseModel):
    """Record of a user interaction"""
    timestamp: datetime
    user_query: str
    function_id: Optional[str] = None
    execution_result: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class SessionData(BaseModel):
    """Session data model"""
    session_id: str
    created_at: datetime
    last_active: datetime
    interactions: List[InteractionRecord] = Field(default_factory=list)
    data: Dict[str, Any] = Field(default_factory=dict)

class SystemInfo(BaseModel):
    """System information schema"""
    api_version: str
    functions_loaded: int
    vector_db_status: str
    llm_model: str
    embedding_model: str