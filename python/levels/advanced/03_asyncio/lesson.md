# Advanced 3: Async I/O and Cancellation

**Author: Codex (OpenAI)**

## Purpose

Manage task lifecycles, timeouts, cancellation, and structured concurrency.

## Learning objectives

- Explain the central abstraction and its tradeoffs.
- Run, trace, test, and modify the example.
- Separate domain logic from input, output, and infrastructure.
- Recognize failure modes and validate boundaries.

## Lesson

Begin with a precise contract: identify the input, result, side effects, and possible failures. Read the example before running it. Trace the state changes, predict the output, and then use execution as evidence. Prefer the simplest design that preserves clarity, testability, and explicit ownership of resources.

The feature in this module is useful only when it reduces complexity at the system boundary. Keep the core calculation small, isolate external effects, and make cleanup and error behavior visible. Add abstractions after repeated concrete cases demonstrate a need.

## Runnable example

```python
import asyncio

async def fetch(name, delay):
    await asyncio.sleep(delay); return name
async def main():
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(fetch(str(i), .01)) for i in range(3)]
    print([task.result() for task in tasks])
if __name__ == "__main__": asyncio.run(main())
```

Run `python3 example.py` from this module directory.

## Guided lab

1. Predict the output and identify every state transition.
2. Run the example and explain any difference from the prediction.
3. Add validation for one invalid or boundary input.
4. Extract one pure function and write a focused test for it.
5. Record one design tradeoff and one alternative implementation.

## Independent practice

1. Adapt the example to Reader study data.
2. Add structured error reporting without hiding the original cause.
3. Measure or test the property that matters most for this module.

## Hints

- Keep computation independent from display and file access.
- Prefer deterministic inputs in tests.
- Document why an abstraction exists, not merely how it is written.

## Solution guidance

A sound solution has a narrow public interface, validates data once at the boundary, and leaves the central transformation easy to test. Confirm ordinary, empty, boundary, and malformed cases. For extensions involving external services or optional packages, keep the standard-library example runnable and isolate the adapter.

## Completion check

You can complete this module when you can explain the design without reading the code, reproduce it in a smaller example, and justify where errors, cleanup, and tests belong.
