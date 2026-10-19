# ADR: ports and Compose

| Field | Value |
|---|---|
| Stage | Phase 4 / 10 Target architecture and ADRs |
| Date / version | 2026-10-18, v1.0 |
| Author / agent | Executor agent (Grok 4.6), correlation id corr-p4-doc-20261018-001 |
| Status | ACCEPTED. Documents FD-06. Does not change the lock. Application A and Application B host ports stay Unknown. |
| Evidence sources | `Execution_Plan.md` sections 4 and 10; `docs/00-preflight/discovery/high-level-architecture.md`; `docs/00-preflight/discovery/system-landscape.md`; inherited `compose.yaml`; `Decision_Tracker.md` FD-06 |
| Assumptions | The inherited default host binds remain 8080 and 8090 until Phase 8 extends Compose. |
| Unresolved issues | Application A and Application B host ports stay Unknown. Phase 8 compose work assigns them. Lake container names stay later. |
| Residual risks | Binding lake REST and lake MCP both to 8000 would clash. Moving the baseline off 8080 would hide the 0-to-8-minute current system. |

This ADR records the locked local port map. Compose starts the listeners. Port 8080 is the legacy API. Port 8090 is the source gateway. Port 8091 is the lake REST API. Port 8092 is the lake MCP server.

---

## Decision

**Verified Fact.** `Execution_Plan.md` sections 4 and 10.

| Port | Listener | Role in the demo |
|---|---|---|
| 8080 | Legacy API | Current-system baseline. Already in inherited `compose.yaml` |
| 8090 | Source gateway | Simulated upstream. Already in inherited `compose.yaml` |
| 8091 | Lake REST | Screens in Application A and Application B read the lake here |
| 8092 | Lake MCP | Agents and other tool clients read the lake here |

**Verified Fact.** `Execution_Plan.md` section 10. One `docker compose up` starts the legacy app on 8080, the source gateway on 8090, the lake REST API on 8091, the lake MCP server on 8092, and both app UIs. Seed the bundled tier.

Application A and Application B host ports are not in that four-port lock. They stay Unknown in this phase.

---

## Alternatives (rejected options)

| Option | What it would do | Why it is rejected |
|---|---|---|
| Lake REST and lake MCP both on 8000 | Framework defaults | The two lake listeners clash with each other. They also clash with common app defaults |
| Replace 8080 with Application A | One port, one app | The 0-to-8-minute slot needs the current API. Inherited Compose already publishes 8080 |
| Random or OS-assigned ports | A new number each boot | The demo script and the speaker notes would have to rediscover the URL every rehearsal |
| Cloud-only URLs with no local ports | Bind nothing on the laptop | Offline replay on this laptop would have no local listener. FD-02 keeps data local |
| Putting the lake on 8080 beside the legacy API | One port, two apps | Route clash. The current GET paths already live on 8080 |
| Skipping Compose | Start each process by hand | Section 10 requires one Compose command for the rehearsal path |

Worked example. FastAPI and the MCP SDK both default to 8000 in common samples. If both lake listeners used 8000, the second bind would fail. 8091 and 8092 sit next to the already-used 8080 and 8090.

---

## Why this wins for a laptop demo

The inherited file already uses 8080 and 8090. Adding 8091 and 8092 keeps one unused gap and two new lake ports. The speaker can say four numbers.

One Compose command matches the 40-minute rehearsal rule.

---

## Risks and mitigation

| Risk | Mitigation |
|---|---|
| Host port already taken on the laptop | Phase 8 can document a conflict. This ADR still locks the intended map |
| Forgetting to publish 8091 or 8092 | Section 10 Done path includes both lake listeners |
| Inventing Application A and Application B ports now | Leave them Unknown. FD-13 / Phase 8 |

---

## Cost and token or runtime impact

Ports have no token cost.

Four extra listeners (8091, 8092, plus two app UIs later) use local RAM. The amount is Unknown until Compose is extended. No cloud load balancer is required for this map.

Honesty: current 8080 and 8090 presence is REAL in inherited Compose. 8091 and 8092 are locked future listeners. They are not in the inherited file today. **Verified Fact.** `docs/00-preflight/discovery/high-level-architecture.md`.

---

## Portability lesson

Keep the current system on its existing port. Give each new listener the next unused number in the same range. Do not reuse 8000 for two lake servers.

---

## Finding

**Finding.** The locked port map is 8080 legacy, 8090 source gateway, 8091 lake REST, 8092 lake MCP, started by Compose.
**Evidence.** `Execution_Plan.md` sections 4 and 10. FD-06.
**Impact.** Phase 8 extends `compose.yaml`. Phase 5 serving binds 8091 and 8092.
**Risk.** Assigning Application A and Application B ports here would collide with Phase 8.
**Confidence.** High on the four locked ports. Unknown on the two app host ports.
**Open questions.** Application A host port. Application B host port. Container names.

---

## What this ADR does not do

This ADR does not edit `compose.yaml`. It does not assign Application A or Application B ports. It does not start Phase 8.
