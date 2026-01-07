from dataclasses import dataclass
from typing import Any, Dict
from uuid import uuid4


@dataclass
class RunEvent:
    run_id: str
    pipeline: str
    version: str
    input_summary: Dict[str, Any]


@dataclass
class StepEvent:
    step_id: str
    run_id: str
    name: str
    step_type: str
    input_count: int
    output_count: int
    metadata: Dict[str, Any]


@dataclass
class DecisionEvent:
    step_id: str
    candidate_id: str
    decision: str
    reason: str
