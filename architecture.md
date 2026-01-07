# ARCHITECTURE.md

## Overview

**X-Ray** provides decision-level observability for multi-step, non-deterministic pipelines (e.g., LLM-driven retrieval, filtering, ranking).  
Unlike logs or tracing—which answer *what happened*—X-Ray answers **why a particular output was produced** by capturing structured decision context and exposing it via query APIs.

---

## System Architecture

### Concise Block Diagram

```text
┌──────────────────────────┐
│   Business Pipeline      │
│                          │
│  - generate keywords     │
│  - retrieve candidates   │
│  - filter / rank / select│
└────────────┬─────────────┘
             │
             │ decision context
             ▼
┌──────────────────────────┐
│        X-Ray SDK         │
│                          │
│  - run / step contexts   │
│  - optional decisions    │
│  - async, fail-open      │
└────────────┬─────────────┘
             │
             │ POST /ingest/*
             ▼
┌──────────────────────────┐
│      X-Ray Backend       │
│                          │
│  - runs / steps /        │
│    decisions store       │
│  - query & aggregation   │
└────────────┬─────────────┘
             │
             │ GET /runs /decisions
             ▼
┌──────────────────────────┐
│   Debugging & Analysis   │
│                          │
│  - why rejected?         │
│  - where logic failed?   │
└──────────────────────────┘


Key property: Execution and debugging are decoupled. The pipeline never blocks on observability.

Data Model
Entities

Run

One end-to-end execution of a pipeline.

Fields: run_id, pipeline, version, input_summary, timestamps.

Step

One logical decision boundary within a run.

Fields: step_id, run_id, name, step_type, input_count, output_count, metadata.

Decision (optional, sampled)

Per-candidate reasoning at a step.

Fields: step_id, candidate_id, decision, reason, optional scores.

Run (1)
 ├─ Step (N)
 │    └─ Decision (0..N)
 └─ Step (N)
      └─ Decision (0..N)

Data Model Rationale

Why this structure

Mirrors real decision flows: candidates move through steps.

Separates execution context (Run), decision logic (Step), and reasoning (Decision).

Supports partial observability: counts always; decisions optionally.

Alternatives considered

Flat JSON logs → brittle queries.

Tracing spans only → timing-focused, no decision semantics.

Per-pipeline schemas → breaks generality.

What would break otherwise

No Step entity → cannot localize failures.

No standardized counts → cross-pipeline analytics fail.

No Decision layer → must re-run pipelines to explain outcomes.

Debugging Walkthrough (Bad Match)

Symptom: Phone case matched to a laptop stand.

Find the run

GET /runs → select the run with the bad output.

Inspect steps

GET /runs/{run_id} → observe input/output counts.

Filtering reduced ~5,000 → ~30 (very aggressive).

Inspect decisions

GET /runs/{run_id}/decisions → aggregate rejection reasons.

Many category/price rejections; laptop stands survived due to keyword overlap.

Conclusion

Root cause is upstream keyword generation, not ranking.

Queryability (Across Pipelines)

Example question:
“Show all runs where the filtering step eliminated >90% of candidates.”

How it’s supported

Enforced conventions:

step_type from a shared enum (e.g., filter, rank, retrieve, llm_eval)

Mandatory input_count, output_count

Query computes output_count / input_count across all step_type="filter".

Developer constraints

Use standardized step_type.

Always provide counts.

Use stable reason codes for decisions.

Performance & Scale

Problem: Steps with thousands of candidates make full capture expensive.

Approach: Tiered capture

Always: step metadata + counts.

Optional: per-candidate decisions.

Sampled/Capped: decisions for large sets.

Who decides

System defaults to summaries.

Developers opt into full detail per step.

Developer Experience

Minimal instrumentation

with xray.run(input_summary):
    with xray.step(name="filter", step_type="filter",
                   input_count=5000, output_count=30):
        ...


Full instrumentation

xray.record_decision(step_id, candidate_id, decision, reason)


Backend unavailable

SDK is fail-open: async sends, short timeouts, swallowed exceptions.

Pipeline behavior is unchanged.

Brief API Spec

Ingest

POST /ingest/run

POST /ingest/step

POST /ingest/decision

Query

GET /runs

GET /runs/{run_id}

GET /runs/{run_id}/decisions

GET /steps/{step_id}/decisions

Aggregations via query params.

Real-World Application

In a Python DOCX editing engine with sequential transformations, formatting bugs required replaying the entire pipeline.
With X-Ray, each edit would be a Step with before/after counts and optional diffs, localizing the exact transformation that introduced corruption.