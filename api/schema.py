from pydantic import BaseModel
from typing import Dict, Any


class RunIn(BaseModel):
    run_id: str
    pipeline: str
    version: str
    input_summary: Dict[str, Any]


class StepIn(BaseModel):
    step_id: str
    run_id: str
    name: str
    step_type: str
    input_count: int
    output_count: int
    metadata: Dict[str, Any]


class DecisionIn(BaseModel):
    step_id: str
    candidate_id: str
    decision: str
    reason: str
