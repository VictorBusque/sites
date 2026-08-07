# Ideas — blog entry queue

Every idea maps to one note under `blog/`. **Status:** `Queued` = on my list to write, `Idea` = brainstormed, not yet committed. When a note ships, move it to the `ENTRIES` list in `index.html` and delete the row here.

## AI — Basics

| Concept | Title | Excerpt | Status |
| --- | --- | --- | --- |
| LLM | Token by token | What a language model actually is, one token at a time | Queued |
| Agent | When a tool acts on its own | What makes a system an agent, not a tool | Queued |
| Tokens | How text becomes numbers | The split that happens before the model ever sees your words | Idea |
| Embeddings | Meaning, mapped | Turning meaning into vectors, and why similar things land nearby | Idea |
| Sampling | Why the same prompt isn't deterministic | Temperature, top-p, and the randomness you can tune | Idea |
| Context window | What the model can see | The window of visibility, and what falls outside it | Idea |

## AI — Advanced

| Concept | Title | Excerpt | Status |
| --- | --- | --- | --- |
| Tools | Text that turns into action | Function calling as the primitive that turns text into action | Queued |
| MCP | One interface to the world | The protocol that gives models a stable interface to the world | Queued |
| RAG | Grounding answers in your data | Retrieval-augmented generation, from index to answer | Queued |
| Harness | The loop that drives the model | The loop that drives model + tools + context | Queued |
| pi.dev | A harness I live in | pi as a harness: skills, MCP, sandboxing, and the agent loop | Queued |
| Speculative decoding | Faster than one token at a time | Draft models and why inference can outpace single-token generation | Queued |
| KV-cache | What transformers remember | What transformers remember between tokens, and why memory grows with context | Queued |
| Claude Agents SDK | A harness you don't have to build | The SDK as a harness you don't have to build | Queued |
| Context engineering | Structure, not hacks | Prompt structure and context stuffing, not prompt hacks | Idea |
| Structured output | The contract agents need | JSON schemas and why agents need a contract | Idea |
| ReAct loop | Think, act, repeat | Reasoning-then-acting as the pattern behind tool use | Idea |
| Multi-agent | When one model isn't enough | Orchestrating several models, and when it pays off | Idea |
| Skills vs plugins vs MCP | Where each layer lives | Where each layer of the stack lives, and what belongs where | Idea |

## AI — Models

| Concept | Title | Excerpt | Status |
| --- | --- | --- | --- |
| Claude lineup | Sonnet vs Opus vs Haiku | How the lineup splits in my daily work, and where I reach for each | Idea |
| Model routing | The right model per task | Picking the right model per task, and the risks of getting it wrong | Queued |
| Cost per task | What answers really cost | Tokens in vs tokens out, and the real price of an answer | Idea |

## AI — Production

| Concept | Title | Excerpt | Status |
| --- | --- | --- | --- |
| Gateway | Routing model calls like traffic | Routing, throttling, and load-balancing model calls | Queued |
| Runtimes | Where agents actually execute | The execution layer of an agent, and what runs there | Queued |
| Memory | Persistence across turns | Persistence across sessions and turns | Queued |
| Guardrails | Steering before it goes off | Steering and constraining model output | Queued |
| Sandboxing | Isolating untrusted code | Isolating untrusted code and tool execution | Queued |
| Security | Prompt injection, exfiltration, least privilege | The threats, and the countermeasures | Queued |
| Evaluation | Measure before it ships | Measuring quality before it ships | Queued |
| Observability | What the model saw, did, and cost | Tracing agent runs end to end | Idea |
| Streaming | Token-by-token feel | Why streaming changes the feel of an answer | Idea |
| Retries and fallbacks | Degrade gracefully | Making flaky model calls degrade gracefully | Idea |
| Cost control | Before the bill surprises you | Caching, batching, and throttling | Idea |

## AI — Personal

| Concept | Title | Excerpt | Status |
| --- | --- | --- | --- |
| My setup | The machine I work from | The machine, the shell, the editor, the workflows | Queued |
| My infrastructure | How my stack is wired | What runs my personal stack and how it's wired | Queued |
| My projects | Shipped, and in progress | The ones I've shipped and the ones in motion | Queued |
| How I drive pi | My daily agent loop | Skills, sessions, habits — the loop I actually run | Idea |
| My prompt templates | The ones I keep | The reusable prompts I actually keep | Idea |
| CV work with agents | Agents on my CV | How I use agents to work on my CV | Queued |
| LinkedIn screening | Screening outreach with AI | How I use AI to screen LinkedIn outreaches I receive | Queued |

## Software Engineering — Python

| Concept | Title | Excerpt | Status |
| --- | --- | --- | --- |
| FastAPI | Where the concurrency happens | Async web frameworks, and where the concurrency actually happens | Queued |
| Concurrency | Threads, asyncio, and when each wins | Threads, asyncio, and when each one wins | Queued |
| Parallelism | Multiprocessing and the GIL | Multiprocessing and the GIL story | Queued |
| asyncio deep dive | The event loop, and what blocks it | The event loop, coroutines, and what blocks it | Idea |
| Streaming responses | Data as it arrives | Sending data as it arrives, not when it's done | Idea |
| FastAPI vs Litestar | Two frameworks, one hard problem | Two async frameworks, one hard problem | Idea |

## Software Engineering — Architecture

| Concept | Title | Excerpt | Status |
| --- | --- | --- | --- |
| Monolith first | When microservices are the wrong call | Why most projects shouldn't start distributed | Idea |
| Event-driven | Decoupling with queues | Decoupling with queues, and why it isn't free | Idea |
| Agent runtime as architecture | My agent stack | What my agent stack looks like as an architecture | Idea |

## Cloud — AWS

| Concept | Title | Excerpt | Status |
| --- | --- | --- | --- |
| Bedrock AgentCore | Agents as a managed service | Agents as a managed service on AWS | Queued |

More queued — Lambda, S3 and DynamoDB land here.
