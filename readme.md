Setup Instructions

Install dependencies

pip install -r requirements.txt

Start the X-Ray backend

uvicorn api.main:app

Run without --reload when using in-memory storage.

Run the example competitor pipeline

python example/competitor_pipeline.py

Inspect captured data

List runs: GET /runs

Inspect a run: GET /runs/{run_id}

View decisions: GET /runs/{run_id}/decisions

Brief Explanation of the Approach

X-Ray is designed as a decision observability layer that runs alongside existing pipelines without changing their behavior.
Developers instrument decision boundaries (such as filtering, ranking, or LLM evaluation) using a lightweight SDK.

The SDK captures structured context—inputs, outputs, filters applied, and optional per-candidate reasoning—and sends it asynchronously to a backend service.
The backend stores this data and exposes query APIs, enabling post-hoc debugging of why a specific output was produced.

Execution and debugging are intentionally decoupled to ensure safety, low overhead, and zero impact on production behavior.

Known Limitations / Future Improvements
Known Limitations

In-memory storage is volatile and limited to a single process (demo-only).

No UI; analysis is performed via API queries.

Per-candidate decision capture is manual and opt-in.

No authentication or access control.

Future Improvements

Persistent, analytics-optimized storage (e.g., PostgreSQL or ClickHouse).

Schema evolution and versioning for long-running pipelines.

Privacy and redaction controls for sensitive data.

Visualization tools (timelines, diffs, aggregates).

Prompt and model version tracking for LLM-based steps.

Adaptive sampling policies to balance cost and observability.