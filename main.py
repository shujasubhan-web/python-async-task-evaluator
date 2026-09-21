import asyncio
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Async Task & Code Evaluator",
    description="A high-performance asynchronous service for evaluating task execution time.",
    version="1.0.0"
)

class EvaluationRequest(BaseModel):
    task_name: str = Field(..., example="Sorting Algorithm Test")
    execution_time: float = Field(..., gt=0, example=1.25)
    memory_mb: float = Field(..., gt=0, example=256.0)

class EvaluationResponse(BaseModel):
    task_name: str
    status: str
    performance_score: float

async def calculate_score(execution_time: float, memory_mb: float) -> float:
    """Asynchronously calculates performance score based on time and memory usage."""
    await asyncio.sleep(0.1)  # Simulating async I/O operation
    score = max(0.0, 100.0 - (execution_time * 10 + memory_mb * 0.05))
    return round(score, 2)

@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_task(request: EvaluationRequest) -> Dict[str, Any]:
    """Endpoint to process and evaluate Python code metrics."""
    if request.execution_time > 10.0:
        raise HTTPException(status_code=400, detail="Execution time exceeds acceptable limit.")
    
    score = await calculate_score(request.execution_time, request.memory_mb)
    status = "Passed" if score >= 60.0 else "Needs Optimization"
    
    return {
        "task_name": request.task_name,
        "status": status,
        "performance_score": score
    }

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for automated monitoring."""
    return {"status": "healthy", "service": "Python Async Evaluator"}
