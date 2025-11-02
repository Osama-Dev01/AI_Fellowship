from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid

app = FastAPI(
    title="Todo API",
    description="A simple Todo API built with FastAPI",
    version="1.0.0"
)

# In-memory storage for todos
todos: List[Dict[str, Any]] = []

# Pydantic models for request/response validation
class TodoCreate(BaseModel):
    task: str = Field(..., min_length=1, max_length=200, description="The task description")

class TodoResponse(BaseModel):
    id: int
    task: str
    completed: bool = False

class TodoUpdate(BaseModel):
    task: Optional[str] = Field(None, min_length=1, max_length=200)
    completed: Optional[bool] = None

# Utility functions
def get_next_id() -> int:
    """Generate the next ID for a new todo"""
    return len(todos) + 1

def find_todo_by_id(todo_id: int) -> Optional[Dict[str, Any]]:
    """Find a todo by its ID"""
    return next((todo for todo in todos if todo["id"] == todo_id), None)

@app.get("/", response_model=Dict[str, str])
async def root() -> Dict[str, str]:
    """Root endpoint with API information"""
    return {"message": "Welcome to Todo API", "docs": "/docs"}

@app.get("/todos", response_model=List[TodoResponse])
async def get_todos() -> List[Dict[str, Any]]:
    """
    Get all todo items
    
    Returns:
        List of all todo items with their details
    """
    return todos

@app.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate) -> Dict[str, Any]:
    """
    Create a new todo item
    
    Args:
        todo: TodoCreate model with task field
        
    Returns:
        The created todo item with generated ID
    """
    new_todo = {
        "id": get_next_id(),
        "task": todo.task,
        "completed": False
    }
    
    todos.append(new_todo)
    return new_todo

@app.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int) -> Dict[str, Any]:
    """
    Get a specific todo item by ID
    
    Args:
        todo_id: ID of the todo item to retrieve
        
    Returns:
        The requested todo item
        
    Raises:
        HTTPException: 404 if todo not found
    """
    todo = find_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found"
        )
    return todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, todo_update: TodoUpdate) -> Dict[str, Any]:
    """
    Update a todo item
    
    Args:
        todo_id: ID of the todo item to update
        todo_update: Fields to update (task and/or completed status)
        
    Returns:
        The updated todo item
        
    Raises:
        HTTPException: 404 if todo not found
    """
    todo = find_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found"
        )
    
    # Update provided fields
    if todo_update.task is not None:
        todo["task"] = todo_update.task
    if todo_update.completed is not None:
        todo["completed"] = todo_update.completed
    
    return todo

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int) -> None:
    """
    Delete a todo item
    
    Args:
        todo_id: ID of the todo item to delete
        
    Raises:
        HTTPException: 404 if todo not found
    """
    todo = find_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found"
        )
    
    todos.remove(todo)

@app.get("/health", response_model=Dict[str, Any])
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint
    
    Returns:
        API health status and todo count
    """
    return {
        "status": "healthy",
        "todo_count": len(todos),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)