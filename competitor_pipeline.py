from sdk.client import XRayClient

xray = XRayClient(
    service_url="http://127.0.0.1:8005",
    pipeline="competitor_selection",
    version="v1"
)

candidates = [{"id": f"A{i}", "price": i} for i in range(100)]

with xray.run({"asin": "PHONE_CASE_123"}) as run_id:
    with xray.step(
        run_id,
        name="filter_candidates",
        step_type="filter",
        input_count=len(candidates),
        output_count=10,
        metadata={"price_range": "cheap"}
    ) as step_id:
        for c in candidates:
            if c["price"] > 10:
                xray.record_decision(
                    step_id,
                    candidate_id=c["id"],
                    decision="rejected",
                    reason="price_out_of_range"
                )
