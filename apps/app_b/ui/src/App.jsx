import { useEffect, useState } from "react";
import { ROLES, callApi } from "./api.js";

const SCENARIOS = ["Replay", "Recipe", "Clocks", "Policy", "Outage", "Rule trace", "Compare"];

export function DemoApp({ appName, port, otherPort, lineage }) {
  const [scenario, setScenario] = useState("Replay");
  const [actor, setActor] = useState({
    apiKey: "local-demo-only",
    actorId: "demo-actor",
    role: "RT-01",
  });
  const [state, setState] = useState(null);
  const [result, setResult] = useState("");
  const [auditId, setAuditId] = useState("");
  const [details, setDetails] = useState("");
  const [other, setOther] = useState(null);
  const [agent, setAgent] = useState(null);

  async function refresh() {
    const response = await callApi("/api/demo/state", actor);
    setState(response.data);
    setAuditId(response.data.correlation_id || "");
    setDetails(JSON.stringify(response.data, null, 2));
  }

  useEffect(() => {
    refresh().catch((error) => setResult(String(error)));
  }, [actor.role, actor.actorId]);

  async function run(path, options) {
    const response = await callApi(path, actor, options);
    setState(response.data);
    setAuditId(response.data.correlation_id || auditId);
    setDetails(JSON.stringify(response.data, null, 2));
    setResult(response.data.message || response.data.last_probe?.sentence || "Done.");
    return response.data;
  }

  async function investigate() {
    const response = await callApi("/api/agent/run", actor, {
      method: "POST",
      body: { case_id: "PS000000016", proposed_action: "review recipe mismatch" },
    });
    setAgent(response.data);
    const verdict = response.data.opa_verdict || response.data.verdict || "";
    setResult(verdict || response.data.error_class || "Agent returned.");
    setAuditId(response.data.correlation_id || "");
    setDetails(JSON.stringify(response.data, null, 2));
  }

  async function compare() {
    const mine = await callApi("/api/demo/state", actor);
    setState(mine.data);
    let theirs = null;
    try {
      const response = await fetch(`http://127.0.0.1:${otherPort}/api/demo/state`, {
        headers: {
          "X-Api-Key": actor.apiKey,
          "X-Actor-Id": actor.actorId,
          "X-Actor-Role": actor.role,
        },
      });
      theirs = await response.json();
    } catch (error) {
      theirs = { ok: false, message: String(error) };
    }
    setOther(theirs);
    setResult("The browser called both ports. The servers did not call each other.");
  }

  const holdDisabled =
    actor.role !== "RT-03" || actor.actorId === (state?.proposed_by || "model_draft");
  const verdict = agent?.opa_verdict || "";
  let sentence = result || "Ready.";
  if (scenario === "Replay" && state) {
    sentence = `${result ? `${result} ` : ""}Work-queue count ${state.queue_count}.`;
  } else if (scenario === "Recipe") {
    sentence = `Verdict ${verdict || "not run"}.`;
  } else if (scenario === "Policy" && state?.policy?.verdict) {
    sentence = `${state.policy.verdict}. ${state.policy.sentence || ""}`.trim();
  } else if (scenario === "Outage" && state?.last_probe) {
    sentence = `Attempt count ${state.last_probe.attempt_count}. ${state.last_probe.sentence || ""}`.trim();
  }

  return (
    <main className="console">
      <header className="console-header">
        <div>
          <h1>{appName}</h1>
          <p>Port {port}</p>
        </div>
        <label>
          Role picker
          <select
            value={actor.role}
            onChange={(event) => setActor({ ...actor, role: event.target.value })}
          >
            {ROLES.map((role) => (
              <option key={role.id} value={role.id}>{role.label}</option>
            ))}
          </select>
        </label>
        <label>
          Actor id
          <input
            value={actor.actorId}
            onChange={(event) => setActor({ ...actor, actorId: event.target.value })}
          />
        </label>
      </header>
      <nav className="scenario-bar">
        {SCENARIOS.map((name) => (
          <button
            key={name}
            type="button"
            className={scenario === name ? "scenario-current" : undefined}
            aria-current={scenario === name ? "page" : undefined}
            onClick={() => setScenario(name)}
          >
            {name}
          </button>
        ))}
        <button type="button" onClick={() => run("/api/demo/reset", { method: "POST" })}>
          Start the demo again
        </button>
      </nav>
      <section className="panel">
        <h2>Situation</h2>
        <p>{appName} on port {port}. {scenario} is open.</p>
      </section>
      <section className="panel">
        <h2>Evidence table</h2>
        <Evidence scenario={scenario} state={state} lineage={lineage} other={other} />
      </section>
      <section className="panel">
        <h2>One action</h2>
        <Action
          scenario={scenario}
          lineage={lineage}
          holdDisabled={holdDisabled}
          onRun={run}
          onInvestigate={investigate}
          onCompare={compare}
        />
      </section>
      <section className="panel">
        <h2>Result</h2>
        <p className="result-sentence">{sentence}</p>
      </section>
      <section className="panel">
        <h2>Audit rows</h2>
        <p>Correlation id {auditId || "none yet"}.</p>
        {scenario === "Recipe" && lineage ? <p>Phase 10 chain {state?.phase10_correlation_id}.</p> : null}
      </section>
      <section className="panel later-checks">
        <h2>Later checks</h2>
        <button
          type="button"
          onClick={async () => {
            const response = await fetch("/api/cases/PS000000016");
            const data = await response.json();
            setResult(data.message || "The case read failed.");
            setDetails(JSON.stringify(data, null, 2));
          }}
        >
          Read a case with no key
        </button>
        <button
          type="button"
          onClick={async () => {
            const response = await callApi("/api/agent/run", actor, {
              method: "POST",
              body: {
                case_id: "REPLAY-000000000",
                scenario: "IC-01",
                proposed_action: "approve",
              },
            });
            setResult(response.data.opa_verdict || response.data.error_class || "Injection returned.");
            setDetails(JSON.stringify(response.data, null, 2));
          }}
        >
          Injection
        </button>
        <button type="button" onClick={() => run("/api/demo/gateway/pull", { method: "POST" })}>
          Receive one gateway message
        </button>
      </section>
      <details>
        <summary>Details</summary>
        <pre>{details}</pre>
      </details>
    </main>
  );
}

function Evidence({ scenario, state, lineage, other }) {
  if (!state) {
    return <p>The session has not loaded.</p>;
  }
  if (scenario === "Replay") {
    return (
      <table>
        <tbody>
          <tr><td>Ref</td><td>{state.replay.ref}</td></tr>
          <tr><td>Feed ingest</td><td>{state.replay.feed_ingested}</td></tr>
          <tr><td>Replay ingest</td><td>{state.replay.replay_ingested}</td></tr>
          <tr><td>Packaged REPLAY rows</td><td>{state.packaged_replay_rows}</td></tr>
        </tbody>
      </table>
    );
  }
  if (scenario === "Recipe") {
    const row = state.recipe;
    return (
      <table>
        <tbody>
          <tr><td>Dispatch</td><td>{row.dispatch_recipe} at {row.started}</td></tr>
          <tr><td>Tool recipe</td><td>{row.tool_recipe} on {row.tool_id}. Effective date {row.tool_effective_date || "none"}.</td></tr>
          <tr><td>Change</td><td>{row.change_id} effective {row.change_effective} {row.change_status}</td></tr>
        </tbody>
      </table>
    );
  }
  if (scenario === "Clocks") {
    return (
      <table>
        <tbody>
          <tr><td>Event</td><td>{state.clock.event_id}</td></tr>
          <tr><td>Event time</td><td>{state.backfill_applied ? state.clock.event_time : "not applied"}</td></tr>
          <tr><td>Arrival time</td><td>{state.clock.arrival_time}</td></tr>
          <tr><td>Metrology</td><td>{state.clock.metrology_clock}</td></tr>
        </tbody>
      </table>
    );
  }
  if (scenario === "Policy") {
    return (
      <table>
        <tbody>
          {state.policy.in_force.map((row) => (
            <tr key={row.policy_id}>
              <td>{row.policy_id}</td>
              <td>{row.valid_from} to {row.valid_to || "open"}</td>
            </tr>
          ))}
          <tr><td>In force on {state.policy.on_date}</td><td>{state.policy.in_force_count}</td></tr>
          <tr><td>Recorded choice</td><td>{state.policy_choice || "none"}</td></tr>
        </tbody>
      </table>
    );
  }
  if (scenario === "Outage") {
    return (
      <table>
        <tbody>
          <tr><td>Owner of INC-2025-014</td><td>{state.owner_id || "empty"}</td></tr>
          {(state.parked_intakes || []).map((row) => (
            <tr key={row.message_id}><td>{row.message_id}</td><td>{row.status}</td></tr>
          ))}
        </tbody>
      </table>
    );
  }
  if (scenario === "Rule trace") {
    if (!lineage) {
      return <p>Application A has no lineage route.</p>;
    }
    return (
      <ol>
        {state.rule_trace.map((step) => (
          <li key={step.step}>{step.role}: {step.item_id}</li>
        ))}
      </ol>
    );
  }
  return (
    <table>
      <tbody>
        <tr><td>This app</td><td>{state.app_name} queue {state.queue_count}</td></tr>
        <tr><td>Other app</td><td>{other ? `${other.app_name || "other"} queue ${other.queue_count ?? "unavailable"}` : "not loaded"}</td></tr>
        {state.known_differences.map((row) => (
          <tr key={row}><td>Difference</td><td>{row}</td></tr>
        ))}
      </tbody>
    </table>
  );
}

function Action({ scenario, lineage, holdDisabled, onRun, onInvestigate, onCompare }) {
  if (scenario === "Replay") {
    return (
      <>
        <button className="primary" type="button" onClick={() => onRun("/api/demo/replay/receive", { method: "POST" })}>
          Receive the replayed MESDispatch
        </button>
        <button type="button" onClick={() => onRun("/api/demo/replay/drop", { method: "POST" })}>
          Confirm drop
        </button>
      </>
    );
  }
  if (scenario === "Recipe") {
    return (
      <>
        <button className="primary" type="button" onClick={onInvestigate}>Investigate</button>
        <button type="button" disabled={holdDisabled}>Hold</button>
      </>
    );
  }
  if (scenario === "Clocks") {
    return (
      <button className="primary" type="button" onClick={() => onRun("/api/demo/clocks/apply", { method: "POST" })}>
        Apply the backfilled event
      </button>
    );
  }
  if (scenario === "Policy") {
    return (
      <>
        <button className="primary" type="button" onClick={() => onRun("/api/demo/policy/check", { method: "POST" })}>
          Check the overlap
        </button>
        <button type="button" onClick={() => onRun("/api/demo/policy/decide", { method: "POST", body: { choice: "keep-wait" } })}>
          Record policy decision
        </button>
      </>
    );
  }
  if (scenario === "Outage") {
    return (
      <>
        <button className="primary" type="button" onClick={() => onRun("/api/demo/outage/probe?mode=timeout", { method: "POST" })}>
          Probe timeout
        </button>
        <button type="button" onClick={() => onRun("/api/demo/outage/probe?mode=schema", { method: "POST" })}>
          Probe schema
        </button>
        <button type="button" onClick={() => onRun("/api/demo/outage/park", { method: "POST" })}>
          Park a bad intake
        </button>
        <button type="button" onClick={() => onRun("/api/demo/outage/replay", { method: "POST" })}>
          Replay the parked intake
        </button>
      </>
    );
  }
  if (scenario === "Rule trace") {
    return lineage ? (
      <button className="primary" type="button" onClick={() => onRun("/api/demo/rule-trace", { method: "GET" })}>
        Show the five steps
      </button>
    ) : (
      <p>Open Application B for the rule trace.</p>
    );
  }
  return (
    <button className="primary" type="button" onClick={onCompare}>Compare</button>
  );
}
