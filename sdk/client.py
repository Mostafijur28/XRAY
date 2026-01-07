import requests
from .context import RunContext, StepContext
import logging

logger = logging.getLogger("xray")


class XRayClient:
    def __init__(self, service_url, pipeline, version):
        self.service_url = service_url.rstrip("/")
        self.pipeline = pipeline
        self.version = version

    def run(self, input_summary):
        return RunContext(self, input_summary)

    def step(self, run_id, name, step_type, input_count, output_count, metadata=None):
        return StepContext(
            self, run_id, name, step_type, input_count, output_count, metadata
        )

    def record_decision(self, step_id, candidate_id, decision, reason):
        payload = {
            "step_id": step_id,
            "candidate_id": candidate_id,
            "decision": decision,
            "reason": reason,
        }
        self._post("/ingest/decision", payload)

    def emit_run(self, run_id, input_summary):
        payload = {
            "run_id": run_id,
            "pipeline": self.pipeline,
            "version": self.version,
            "input_summary": input_summary,
        }
        self._post("/ingest/run", payload)

    def emit_step(self, **payload):
        self._post("/ingest/step", payload)

    def _post(self, path, payload):
        try:
            requests.post(f"{self.service_url}{path}", json=payload, timeout=0.1)
        except Exception as e:
            # fail-open: never break the pipeline
            logger.warning(f"X-Ray POST failed: {path} | error={e}")
            pass
