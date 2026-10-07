<div align="center">

# AI Engineering Design Patterns · Season 01

**The structural decisions real production agents are built on, one pattern at a time, in the order they matter.**

A [Gensoku Devs](https://www.youtube.com/channel/UC9gPwESzUv7cvtC3qQdhmPQ) YouTube series

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Season](https://img.shields.io/badge/Season-01-ec2c34?style=flat-square)
![Patterns](https://img.shields.io/badge/Patterns-140-ededed?style=flat-square)
![Umbrellas](https://img.shields.io/badge/Umbrellas-14-ededed?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

[▶ Watch the series](https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID) · [Repo layout](#-repository-layout) · [Getting started](#-getting-started)

</div>

---

## Why this series exists

Getting hired in AI engineering now takes more than a toy RAG app and a LangChain demo. Real agents fail in specific, predictable ways. The fixes are design patterns that most tutorials never mention.

This series goes **depth-first**, not breadth-first. For every pattern it covers how it works, why it exists, and the edge cases a tutorial would normally skip.

---

## 📚 Pattern index

The umbrellas are ranked by how load-bearing they are in production agents today. Ticked patterns have code in this repo.

| # | Umbrella | Patterns |
|:---:|---|:---:|
| 01 | Tool Use & Tool Interface Design | 15 |
| 02 | Context Engineering & Memory | 17 |
| 03 | Control Flow & the Agent Loop | 19 |
| 04 | Guardrails, Permissions & Human Control | 17 |
| 05 | Reliability & Failure Recovery | 11 |
| 06 | Retrieval & Grounding | 10 |
| 07 | Verification, Evaluation & Self-Correction | 14 |
| 08 | Observability, Durability & Operations | 9 |
| 09 | Multi-Agent Orchestration & Delegation | 10 |
| 10 | Cost, Latency & Model Routing | 3 |
| 11 | Prompt-Injection-Resistant Architecture | 4 |
| 12 | Reasoning & Inference-Time Compute | 4 |
| 13 | Computer, Browser & GUI Control | 2 |
| 14 | Streaming & Interaction UX | 5 |

<details>
<summary><b>01 · Tool Use & Tool Interface Design</b>: nothing is an agent without it</summary>

- [ ] 01. Tool Use
- [ ] 02. Structured Output
- [ ] 03. Parallel Tool Calls
- [ ] 04. Sandbox Isolation
- [ ] 05. Model Context Protocol (MCP)
- [ ] 06. Agent-Computer Interface (ACI) Design
- [ ] 07. Tool Loadout
- [ ] 08. Code Execution as Action (CodeAct)
- [ ] 09. Agent Skills
- [ ] 10. Composite Service Tool
- [ ] 11. Direct API Wrapper
- [ ] 12. Tool Result Caching
- [ ] 13. Async Tool Handle
- [ ] 14. Tool Discovery & Registry
- [ ] 15. Translation Layer (Anti-Corruption)

</details>

<details>
<summary><b>02 · Context Engineering & Memory</b>: the dominant failure surface today</summary>

- [ ] 01. Context Window Packing
- [ ] 02. Context Compaction
- [ ] 03. Short-Term Thread Memory
- [ ] 04. Scratchpad
- [ ] 05. Prompt Caching (Stable Prefix)
- [ ] 06. Session Isolation
- [ ] 07. Filesystem as Context
- [ ] 08. Just-in-Time Context Retrieval
- [ ] 09. Tool-Result Eviction
- [ ] 10. Layered Configuration Context
- [ ] 11. Cross-Session Memory
- [ ] 12. Semantic Memory
- [ ] 13. Episodic Memory
- [ ] 14. Vector Memory
- [ ] 15. Progressive Disclosure for Large Files
- [ ] 16. Reasoning Trace Carry-Forward
- [ ] 17. Context Window Utilisation Cap

</details>

<details>
<summary><b>03 · Control Flow & the Agent Loop</b>: the shape of the loop is the architecture</summary>

- [ ] 01. ReAct
- [ ] 02. Prompt Chaining
- [ ] 03. Routing
- [ ] 04. Step Budget
- [ ] 05. Stop Hook / Termination Predicate
- [ ] 06. Parallelization (Sectioning & Voting)
- [ ] 07. Deterministic Control Flow, Not Prompt
- [ ] 08. Plan-and-Execute
- [ ] 09. Goal Decomposition
- [ ] 10. Replan on Failure
- [ ] 11. Todo-List-Driven Agent
- [ ] 12. Iterative Refinement Loop
- [ ] 13. MapReduce for Agents
- [ ] 14. Event-Driven Agent
- [ ] 15. Scheduled Agent
- [ ] 16. Disambiguation
- [ ] 17. Stateless Reducer Agent
- [ ] 18. Spec-Driven Loop
- [ ] 19. Outer-Inner Agent Loop

</details>

<details>
<summary><b>04 · Guardrails, Permissions & Human Control</b>: required once an agent has side effects</summary>

- [ ] 01. Human-in-the-Loop Approval Gate
- [ ] 02. Input/Output Guardrails
- [ ] 03. Secrets Handling
- [ ] 04. Rate Limiting
- [ ] 05. Refusal
- [ ] 06. Conversation Handoff to Human
- [ ] 07. Risk-Tiered Action Approval
- [ ] 08. Kill Switch
- [ ] 09. Approval Queue
- [ ] 10. Cost Gating
- [ ] 11. Dry-Run / Simulate Before Actuate
- [ ] 12. Compensating Action
- [ ] 13. Interruptible Execution
- [ ] 14. Delegated Agent Authorization
- [ ] 15. Policy-as-Code Gate
- [ ] 16. Execution-Plan Confirmation
- [ ] 17. PII Redaction

</details>

<details>
<summary><b>05 · Reliability & Failure Recovery</b>: distributed-systems discipline, re-learned</summary>

- [ ] 01. Exception Handling & Recovery
- [ ] 02. Bounded Retry with Backoff
- [ ] 03. Schema Validation Retry
- [ ] 04. Fallback Chain
- [ ] 05. Idempotent Tool Design
- [ ] 06. Circuit Breaker
- [ ] 07. Provider Fallback
- [ ] 08. Graceful Degradation
- [ ] 09. Agent Resumption / Durable Execution
- [ ] 10. Durable Workflow Snapshot
- [ ] 11. Degenerate-Output Detection

</details>

<details>
<summary><b>06 · Retrieval & Grounding</b>: the main antidote to stale and invented facts</summary>

- [ ] 01. Retrieval-Augmented Generation
- [ ] 02. Agentic Search over the Workspace
- [ ] 03. Hybrid Search
- [ ] 04. Cross-Encoder Reranking
- [ ] 05. Contextual Retrieval
- [ ] 06. Query Rewriting / Multi-Query
- [ ] 07. Agentic RAG
- [ ] 08. Citation Attribution
- [ ] 09. Hierarchical Retrieval
- [ ] 10. Repo Map

</details>

<details>
<summary><b>07 · Verification, Evaluation & Self-Correction</b>: essential, and rarely done</summary>

- [ ] 01. Eval Harness
- [ ] 02. LLM-as-Judge
- [ ] 03. Reflection / Self-Critique
- [ ] 04. Deterministic-LLM Sandwich
- [ ] 05. Evaluator-Optimizer
- [ ] 06. Generator-Critic Separation
- [ ] 07. Self-Consistency
- [ ] 08. Best-of-N Sampling
- [ ] 09. Eval as Contract
- [ ] 10. Dual Evaluation (Offline + Online)
- [ ] 11. Cross-Reflection
- [ ] 12. Human Reflection
- [ ] 13. Workflow Evals with Mocked Tools
- [ ] 14. Self-Refine

</details>

<details>
<summary><b>08 · Observability, Durability & Operations</b>: you can't debug what you didn't trace</summary>

- [ ] 01. Trajectory / Decision Logging
- [ ] 02. Cost & Token Observability
- [ ] 03. Prompt Versioning
- [ ] 04. Own Your Prompts
- [ ] 05. Replay / Time-Travel
- [ ] 06. Lineage Tracking
- [ ] 07. Provenance / Audit Ledger
- [ ] 08. Canary Rollout & Automatic Rollback
- [ ] 09. Agent Middleware Chain

</details>

<details>
<summary><b>09 · Multi-Agent Orchestration & Delegation</b>: popular online, much rarer in production</summary>

- [ ] 01. Orchestrator-Workers
- [ ] 02. Subagent Isolation
- [ ] 03. Agent-as-Tool
- [ ] 04. Handoff
- [ ] 05. Supervisor
- [ ] 06. Parallel Fan-Out / Gather
- [ ] 07. Role Assignment
- [ ] 08. Lead Researcher
- [ ] 09. Hierarchical Agents
- [ ] 10. Planner-Worker Separation

</details>

<details>
<summary><b>10 · Cost, Latency & Model Routing</b>: small category, large bills</summary>

- [ ] 01. Multi-Model Routing / Cascade
- [ ] 02. Complexity-Based Routing
- [ ] 03. Budget-Aware Routing with Hard Caps

</details>

<details>
<summary><b>11 · Prompt-Injection-Resistant Architecture</b>: widely acknowledged, rarely architected for</summary>

- [ ] 01. Lethal Trifecta Threat Model
- [ ] 02. Prompt Injection Defence
- [ ] 03. Tool Output Poisoning Defence
- [ ] 04. Egress Lockdown

</details>

<details>
<summary><b>12 · Reasoning & Inference-Time Compute</b>: the budget decisions are still yours</summary>

- [ ] 01. Chain of Thought
- [ ] 02. Extended Thinking / Reasoning Budget
- [ ] 03. Test-Time Compute Scaling
- [ ] 04. Adaptive Compute Allocation

</details>

<details>
<summary><b>13 · Computer, Browser & GUI Control</b>: shipping, but still narrow</summary>

- [ ] 01. Browser Agent
- [ ] 02. Shadow Workspace

</details>

<details>
<summary><b>14 · Streaming & Interaction UX</b>: non-negotiable for interactive and voice products</summary>

- [ ] 01. Stop / Cancel
- [ ] 02. Streaming Typed Events
- [ ] 03. Verbose Reasoning Transparency
- [ ] 04. Citation Streaming
- [ ] 05. Semantic Turn Endpointing

</details>

---

## 🤝 Contributing

Found a bug, an edge case the production version misses, or a clearer way to explain something?

- **Questions about an episode:** open a [Discussion](../../discussions)
- **Bugs in the code:** open an [Issue](../../issues) and include the pattern folder name
- **Fixes:** pull requests are welcome. Please keep the naive/production split intact.

---

## 📬 Contact

**Collaborations & business:** [gensokudevs@gmail.com](mailto:gensokudevs@gmail.com)

## 📄 License

Released under the [MIT License](LICENSE).

<div align="center">

<sub>Fundamentals → Development → Engineering → Repeat</sub>

**If it isn't deep, it isn't Gensoku.**

</div>
