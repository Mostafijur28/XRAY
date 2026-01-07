from fastapi import FastAPI
from .schema import RunIn, StepIn, DecisionIn
from .storage import RUNS, STEPS, DECISIONS

app = FastAPI(title="X-Ray API")

@app.get("/runs")
def list_runs():
    return list(RUNS.values())

@app.get("/decisions")
def list_decisions():
    return list(DECISIONS)

@app.post("/ingest/run")
def ingest_run(run: RunIn):
    RUNS[run.run_id] = run.dict()
    return {"status": "ok"}


@app.post("/ingest/step")
def ingest_step(step: StepIn):
    STEPS.setdefault(step.run_id, []).append(step.dict())
    return {"status": "ok"}


@app.post("/ingest/decision")
def ingest_decision(decision: DecisionIn):
    DECISIONS.append(decision.dict())
    return {"status": "ok"}


@app.get("/runs/{run_id}")
def get_run(run_id: str):
    return {
        "run": RUNS.get(run_id),
        "steps": STEPS.get(run_id, []),
    }

@app.get("/query/filter_heavy")
def filter_heavy(threshold: float = 0.9):
    results = []
    for steps in STEPS.values():
        for s in steps:
            ratio = s["output_count"] / max(s["input_count"], 1)
            if s["step_type"] == "filter" and ratio <= (1 - threshold):
                results.append(s)
    return results
