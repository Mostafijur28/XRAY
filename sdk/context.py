import uuid
from contextlib import contextmanager


class RunContext:
    def __init__(self, client, input_summary):
        self.client = client
        self.run_id = str(uuid.uuid4())
        self.input_summary = input_summary

    def __enter__(self):
        self.client.emit_run(self.run_id, self.input_summary)
        return self.run_id

    def __exit__(self, exc_type, exc, tb):
        pass


class StepContext:
    def __init__(self, client, run_id, name, step_type, input_count, output_count, metadata):
        self.client = client
        self.step_id = str(uuid.uuid4())
        self.run_id = run_id
        self.name = name
        self.step_type = step_type
        self.input_count = input_count
        self.output_count = output_count
        self.metadata = metadata or {}

    def __enter__(self):
        self.client.emit_step(
            step_id=self.step_id,
            run_id=self.run_id,
            name=self.name,
            step_type=self.step_type,
            input_count=self.input_count,
            output_count=self.output_count,
            metadata=self.metadata,
        )
        return self.step_id

    def __exit__(self, exc_type, exc, tb):
        pass
