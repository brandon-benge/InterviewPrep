# Coding Interview Prep

This directory is organized around three distinct uses:

- `reference/`: short Python and interview cheat sheets
- practice categories: problem statements (`.md`) paired with implementations (`.py`)
- `archive/`: failed attempts, backups, and scratch files that should not clutter active practice

## Working Format

For active problems, keep the structure consistent:

- one prompt file: `<problem>.md`
- one implementation file: `<problem>.py`
- keep related files in the category folder where you would look for that interview pattern first

## Reference

- [Interview Must Haves](reference/interview_must_haves.md)
- [Data Structures Collections](reference/data_structures_collections.md)
- [Classes and OOP](reference/classes_oop.md)
- [Exception Handling](reference/exception_handling.md)

## Practice Categories

- `arrays/`: interval and array-style problems
- `caching_kv_store/`: caches, time-based lookup, transactional KV, ranking
- `concurrency/`: synchronization and thread-safety
- `consistent_hashing_ring/`: partitioning and hashing
- `data_structures/`: reusable DS implementations
- `job_queue/`: worker and queue coordination
- `rate_limiting_ttl/`: expiration, throttling, and sampling
- `stream/`: event processing and temporal aggregation
- `task_scheduler/`: scheduling and retry logic
- `token_bucket/`: bucket-based rate limiting

## Suggested Conventions

- Use category folders for active interview-ready material only.
- Move abandoned experiments and backups into [archive/README.md](archive/README.md).
- Keep the study-plan style index in [questions.md](questions.md) until you decide to merge or replace it.
