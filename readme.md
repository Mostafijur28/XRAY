## X-Ray – Decision Observability for Multi-Step Pipelines

### Overview
X-Ray provides decision-level observability for complex, multi-step systems such as LLM-driven retrieval, filtering, ranking, and selection pipelines.

Traditional logs and tracing answer what happened.
X-Ray answers why a particular output was produced.

### Why X-Ray?

Modern pipelines are:

Multi-stage

Non-deterministic (LLMs, heuristics)

Hard to debug after the fact

When the final output is wrong, it’s difficult to identify:

Which step failed

Whether filters were too aggressive

Whether ranking logic behaved incorrectly

X-Ray captures decision context at each step and makes it queryable after execution.

### High-Level Flow

Business pipeline runs normally.
X-Ray runs alongside it and never interferes.

Pipeline → X-Ray SDK → X-Ray Backend → Debugging & Analysis

Setup Instructions
1. Install dependencies

pip install -r requirements.txt

2. Start the X-Ray backend

uvicorn api.main:app

Run without --reload when using in-memory storage.

3. Run the example pipeline

python example/competitor_pipeline.py

The pipeline prints nothing by design.
All observability data is retrieved via API queries.

4. Inspect captured data

List runs
GET /runs

Inspect a run and its steps
GET /runs/{run_id}

View decisions for a run
GET /runs/{run_id}/decisions

### Brief Explanation of the Approach

X-Ray instruments decision boundaries, not function calls.

Developers wrap:

A pipeline execution as a Run

Each decision boundary as a Step

Optional per-candidate reasoning as Decisions

The SDK sends this structured context asynchronously to a backend service.
The backend stores and exposes it through query APIs for post-hoc debugging.

Execution and debugging are fully decoupled to ensure safety and low overhead.

### Known Limitations

In-memory storage is volatile and single-process (demo-only).

No UI; analysis is API-driven.

Per-candidate decision capture is manual and opt-in.

No authentication or access control.

### Future Improvements

Persistent, analytics-optimized storage (PostgreSQL / ClickHouse).

Schema evolution and versioning.

Privacy and redaction controls.

Visualization (timelines, diffs, aggregates).

Prompt and model version tracking for LLM steps.

Adaptive sampling policies.