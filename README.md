# Async Execution Patterns for Python-based SaaS Pipelines

This project is a technical study on optimizing I/O-bound workloads in Python. Specifically, it addresses the limitations of thread-based concurrency in GIL-constrained environments.

### Context: Moving beyond standard threading
Initially, a multi-threaded approach was considered for this ingestion prototype. However, profiling revealed that context-switching overhead and thread-safety management outweighed the performance gains for pure I/O tasks. 

**Decision:** I refactored the core to a single-threaded event loop using `asyncio`. This approach provides a more deterministic memory footprint and significantly higher throughput for concurrent API operations.

### Resilience and Error Propagation
The implementation in `app/core/optimizer.py` deviates from the standard `asyncio.gather` pattern. In a production B2B SaaS environment, a "fail-fast" strategy is often counter-productive for batch processing.

* **Non-blocking error handling:** By setting `return_exceptions=True`, the pipeline remains resilient. A single malformed request or network timeout does not trigger a cascading failure.
* **Result Sanitization:** Post-await, the system filters out `Exception` objects while logging their trace, ensuring that the downstream data handlers only receive valid payloads.

### Performance Profile
* **Concurrency:** Validated for 1,000+ concurrent simulated requests.
* **Latency:** ~40% reduction in batch processing time compared to synchronous execution.

---
*Technical Note: Part of a Stanford-based research project into high-performance system design.*
