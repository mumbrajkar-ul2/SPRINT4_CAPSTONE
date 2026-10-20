import { useEffect, useRef, useState } from "react";
import { ROLES, callApi } from "./api.js";

const SCENARIOS = ["Replay", "Recipe", "Clocks", "Policy", "Outage", "Rule trace", "Compare"];

const TAB_CASE = {
  Replay: "C00001646",
  Recipe: "L00000016",
  Clocks: "E-00000000",
  Policy: "FAB-00000002",
  Outage: "INC-2025-014",
  "Rule trace": "Recipe rule path",
  Compare: "Both apps",
};

const SITUATION = {
  Replay: "Partner feed REPLAY-000000000 is a second delivery of C00001646.",
  Recipe: "Lot L00000016 on tool T0000013 shows dispatch recipe R02 and tool recipe R01.",
  Clocks: "Evidence E-00000000 has an event time and a later arrival time.",
  Policy: "Fab FAB-00000002 has overlapping US policies on 2024-06-01.",
  Outage: "Incident INC-2025-014 has no follow-up owner.",
  "Rule trace": "This page shows where the recipe rule came from.",
  Compare: "The same case is open on this app and the other app.",
};

const SOURCE_LABEL = {
  azure: "Azure OpenAI",
  replay_file: "a replay file",
  lake_statement: "a lake statement",
};

function emptyExplain() {
  return { sentence: "", answer_source: "", citations: [], replay_save: "", error_class: "" };
}

function withLead(tone, text) {
  const body = String(text || "").trim();
  if (tone !== "refused" && tone !== "failed") {
    return body;
  }
  const lead = tone === "failed" ? "Failed" : "Refused";
  if (/^(Refused|Failed)\b/.test(body)) {
    return body;
  }
  return body ? `${lead}. ${body}` : `${lead}.`;
}

export function DemoApp({ appName, port, otherPort, lineage }) {
  const [scenario, setScenario] = useState("Replay");
  const [actor, setActor] = useState({
    apiKey: "local-demo-only",
    actorId: "demo-actor",
    role: "RT-01",
  });
  const [state, setState] = useState(null);
  const [auditId, setAuditId] = useState("");
  const [auditRows, setAuditRows] = useState([]);
  const [details, setDetails] = useState("");
  const [other, setOther] = useState(null);
  const [agent, setAgent] = useState(null);
  const [explain, setExplain] = useState(emptyExplain);
  const [ownerId, setOwnerId] = useState("");
  const [actionStatus, setActionStatus] = useState("");
  const [actionRefused, setActionRefused] = useState(false);
  const [actionTone, setActionTone] = useState("ready");
  const [holdActor, setHoldActor] = useState("");
  const viewRef = useRef("Replay");
  const tabRefs = useRef([]);

  function publish(tone, text) {
    setActionTone(tone);
    setActionRefused(tone === "refused" || tone === "failed");
    setActionStatus(withLead(tone, text));
  }

  function openScenario(name) {
    viewRef.current = name;
    setScenario(name);
    setActionStatus("");
    setActionRefused(false);
    setActionTone("ready");
    setExplain(emptyExplain());
    setAuditId("");
    setAuditRows([]);
    setDetails("");
    setOther(null);
  }

  function onTabKey(event) {
    if (event.key !== "ArrowRight" && event.key !== "ArrowLeft" && event.key !== "Home" && event.key !== "End") {
      return;
    }
    event.preventDefault();
    const index = SCENARIOS.indexOf(viewRef.current);
    let next = index;
    if (event.key === "ArrowRight") {
      next = (index + 1) % SCENARIOS.length;
    }
    if (event.key === "ArrowLeft") {
      next = (index - 1 + SCENARIOS.length) % SCENARIOS.length;
    }
    if (event.key === "Home") {
      next = 0;
    }
    if (event.key === "End") {
      next = SCENARIOS.length - 1;
    }
    openScenario(SCENARIOS[next]);
    const tab = tabRefs.current[next];
    if (tab) {
      tab.focus();
    }
  }

  async function loadAudit(correlationId, started) {
    if (started && viewRef.current !== started) {
      return;
    }
    if (!correlationId) {
      setAuditRows([]);
      return;
    }
    const response = await callApi(`/api/audit/${encodeURIComponent(correlationId)}`, actor);
    if (started && viewRef.current !== started) {
      return;
    }
    setAuditRows(response.status === 200 ? response.data.rows || [] : []);
  }

  async function refresh() {
    const response = await callApi("/api/demo/state", actor);
    setState(response.data);
    setAuditId(response.data.correlation_id || "");
    setDetails(JSON.stringify(response.data, null, 2));
    await loadAudit(response.data.correlation_id || "");
  }

  useEffect(() => {
    refresh().catch((error) => {
      publish("failed", String(error));
    });
  }, [actor.role, actor.actorId]);

  function remember(data) {
    const citations = data.citations && data.citations.length ? data.citations : data.retrieved_item_ids || [];
    setExplain({
      sentence: data.sentence || data.draft_plan || data.message || "",
      answer_source: data.answer_source || "",
      citations,
      replay_save: data.replay_save || "",
      error_class: data.error_class || "",
    });
  }

  function showOutcome(data, status, fallback) {
    const blocked = status >= 400 || data.ok === false || Boolean(data.error_class);
    const base = data.message || data.error_class || fallback || "Done.";
    if (!blocked) {
      publish("done", base);
      return false;
    }
    const tone = status === 401 || status === 403 || status === 409 ? "refused" : "failed";
    publish(tone, `${base} The current role is ${actor.role}.`);
    return true;
  }

  async function run(path, options = {}) {
    const started = viewRef.current;
    publish("moving", options.pending || "Working.");
    try {
      const response = await callApi(path, actor, options);
      const data = response.data || {};
      if (data.app_name || data.queue_count !== undefined) {
        setState(data);
      }
      if (viewRef.current !== started) {
        return data;
      }
      showOutcome(data, response.status, options.fallback);
      const correlationId = data.correlation_id || auditId;
      setAuditId(correlationId);
      setDetails(JSON.stringify(data, null, 2));
      await loadAudit(correlationId, started);
      return data;
    } catch (error) {
      if (viewRef.current === started) {
        publish("failed", String(error));
      }
      return {};
    }
  }

  async function reviewDelivery() {
    const started = viewRef.current;
    const asking = state?.model_mode === "azure"
      ? "Asking Azure OpenAI to explain the second delivery."
      : "Reading the saved explanation for the second delivery.";
    publish("moving", asking);
    const receivedResponse = await callApi("/api/demo/replay/receive", actor, { method: "POST" });
    const received = receivedResponse.data || {};
    if (received.app_name) {
      setState(received);
    }
    const response = await callApi("/api/query", actor, {
      method: "POST",
      body: {
        question: "This partner feed has processing_status REPLAY. Explain the duplicate.",
        case_id: "REPLAY-000000000",
        job: "explain",
      },
    });
    if (viewRef.current !== started) {
      return;
    }
    const data = response.data || {};
    remember(data);
    const failed = response.status >= 400 || Boolean(data.error_class);
    if (failed) {
      const base = data.message || data.error_class || "The explanation did not return.";
      const tone = response.status === 401 || response.status === 403 || response.status === 409 ? "refused" : "failed";
      publish(tone, `${received.message || "The second delivery is on the work queue."} ${base} The current role is ${actor.role}.`);
    } else {
      publish("done", received.message || "The second delivery is on the work queue.");
    }
    setDetails(JSON.stringify({ delivery: received, explanation: data }, null, 2));
  }

  async function investigate() {
    const started = viewRef.current;
    const asking = state?.model_mode === "azure"
      ? "Asking Azure OpenAI to explain the recipe mismatch."
      : "Reading the saved explanation for the recipe mismatch.";
    publish("moving", asking);
    const response = await callApi("/api/agent/run", actor, {
      method: "POST",
      body: { case_id: "PS000000016", proposed_action: "review recipe mismatch" },
    });
    const data = response.data || {};
    if (viewRef.current !== started) {
      return;
    }
    setAgent(data);
    remember(data);
    const failed = response.status >= 400 || Boolean(data.error_class);
    if (failed) {
      const base = data.message || data.error_class || "The mismatch was not explained.";
      const tone = response.status === 401 || response.status === 403 || response.status === 409 ? "refused" : "failed";
      publish(tone, `${base} The current role is ${actor.role}.`);
    } else {
      publish("done", "The mismatch is explained.");
    }
    const correlationId = data.correlation_id || "";
    setAuditId(correlationId);
    setDetails(JSON.stringify(data, null, 2));
    await loadAudit(correlationId, started);
  }

  async function hold() {
    const started = viewRef.current;
    publish("moving", "Recording the hold.");
    const response = await callApi("/api/approvals", actor, {
      method: "POST",
      correlationId: auditId || undefined,
      body: {
        case_id: "PS000000016",
        action_type: "recipe_hold_or_release",
        decision: "hold",
        proposed_by: agent?.proposed_by || "model_draft",
      },
    });
    const data = response.data || {};
    const refused = response.status >= 400 || data.ok === false;
    if (!refused) {
      setHoldActor(actor.actorId);
    }
    if (viewRef.current !== started) {
      return;
    }
    if (refused) {
      const base = data.message || "Hold was refused.";
      const tone = response.status === 401 || response.status === 403 || response.status === 409 ? "refused" : "failed";
      publish(tone, `${base} The current role is ${actor.role}.`);
    } else {
      publish("done", `Hold recorded by ${actor.actorId}.`);
    }
    setDetails(JSON.stringify(data, null, 2));
    const correlationId = data.correlation_id || auditId;
    setAuditId(correlationId);
    await loadAudit(correlationId, started);
  }

  async function recordOwner() {
    if (!ownerId.trim()) {
      publish("failed", "Type an owner id, then record it.");
      return;
    }
    await run("/api/demo/owner", {
      method: "POST",
      pending: "Recording the owner.",
      body: { owner_id: ownerId.trim() },
    });
  }

  async function compare() {
    const started = viewRef.current;
    publish("moving", "Reading this app and the other app.");
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
    if (viewRef.current !== started) {
      return;
    }
    setOther(theirs);
    const otherName = theirs && theirs.app_name ? theirs.app_name : "the other app";
    const otherQueue = theirs && theirs.queue_count !== undefined ? theirs.queue_count : "unavailable";
    if (theirs && theirs.ok === false) {
      publish("failed", `${theirs.message || "The other app did not respond."} This app queue is ${mine.data.queue_count}.`);
      return;
    }
    publish("done", `This app queue is ${mine.data.queue_count}. ${otherName} queue is ${otherQueue}. The browser read both apps. The servers did not call each other.`);
  }

  const sourceLabel = SOURCE_LABEL[explain.answer_source] || "not chosen yet";
  const cited = (explain.citations || []).join(", ");
  const resultClass = actionTone === "refused" || actionTone === "failed"
    ? "action-refused"
    : actionTone === "moving" || actionTone === "done"
      ? "action-status"
      : "action-ready";

  return (
    <>
      <div className="page-bar" aria-hidden="true" />
      <main className="console">
        <header className="console-header">
          <div className="logo-slot">
            <span className="logo-word">Birlasoft</span>
          </div>
          <div className="header-field">
            <span className="header-label">Application</span>
            <strong className="header-value">{appName}</strong>
          </div>
          <div className="header-field">
            <span className="header-label">Location</span>
            <span>Port {port}</span>
          </div>
          <label className="header-field">
            <span className="header-label">Role picker</span>
            <select
              value={actor.role}
              onChange={(event) => setActor({ ...actor, role: event.target.value })}
            >
              {ROLES.map((role) => (
                <option key={role.id} value={role.id}>{role.label}</option>
              ))}
            </select>
          </label>
          <label className="header-field">
            <span className="header-label">Actor id</span>
            <input
              value={actor.actorId}
              onChange={(event) => setActor({ ...actor, actorId: event.target.value })}
            />
          </label>
          <div className="header-field">
            <span className="header-label">Runtime mode</span>
            <span className="mode-pill">{state?.model_mode || "replay"}</span>
          </div>
          <button type="button" className="header-reset" onClick={() => { setExplain(emptyExplain()); setHoldActor(""); run("/api/demo/reset", { method: "POST", pending: "Starting this shift again." }); }}>
            Start this shift again
          </button>
          <svg className="cover-motif" viewBox="0 0 140 80" width="140" height="80" aria-hidden="true" focusable="false">
            <path d="M132 4 A 64 64 0 0 0 68 68" fill="none" stroke="#ED1C24" strokeWidth="8" />
            <path d="M118 14 A 46 46 0 0 0 72 60" fill="none" stroke="#231F20" strokeWidth="2" />
          </svg>
        </header>
        <div className="workspace">
          <nav className="scenario-bar" role="tablist" aria-label="Scenarios" onKeyDown={onTabKey}>
            {SCENARIOS.map((name, index) => (
              <button
                key={name}
                type="button"
                role="tab"
                ref={(node) => { tabRefs.current[index] = node; }}
                className={scenario === name ? "scenario-current" : undefined}
                aria-current={scenario === name ? "page" : undefined}
                aria-selected={scenario === name}
                tabIndex={scenario === name ? 0 : -1}
                onClick={() => openScenario(name)}
              >
                <span className="tab-name">{name}</span>
                <span className="tab-case">{TAB_CASE[name]}</span>
              </button>
            ))}
          </nav>
          <div className="sheet">
            <section className="band">
              <p className="band-kicker"><span className="band-index">1</span>Situation</p>
              <h2 className="situation-title">{SITUATION[scenario]}</h2>
            </section>
            <section className="band">
              <p className="band-kicker"><span className="band-index">2</span>Evidence</p>
              <div className="evidence-scroll">
                <Evidence scenario={scenario} state={state} lineage={lineage} other={other} holdActor={holdActor} />
              </div>
            </section>
            <section className="band">
              <p className="band-kicker"><span className="band-index">3</span>Actions</p>
              <Action
                scenario={scenario}
                lineage={lineage}
                ownerId={ownerId}
                onOwnerId={setOwnerId}
                onRun={run}
                onReview={reviewDelivery}
                onInvestigate={investigate}
                onHold={hold}
                onOwner={recordOwner}
                onCompare={compare}
              />
            </section>
            <section className="band">
              <p className="band-kicker"><span className="band-index">4</span>Result</p>
              <p className={resultClass} role="status">{actionStatus || "Ready."}</p>
              {(explain.answer_source || explain.sentence) ? (
                <>
                  <p className="result-sentence">{explain.sentence}</p>
                  <p>Answer source: {sourceLabel}.</p>
                  <p>Cited items: {cited || "none"}.</p>
                  {explain.replay_save === "failed" ? (
                    <p>The answer is from Azure OpenAI. The cache file was not written.</p>
                  ) : null}
                </>
              ) : null}
            </section>
            {(auditId || auditRows.length || (scenario === "Recipe" && lineage)) ? (
              <section className="band">
                <p className="band-kicker"><span className="band-index">5</span>Audit</p>
                {auditId ? <p>Correlation id {auditId}.</p> : null}
                {auditRows.length ? (
                  <table>
                    <tbody>
                      {auditRows.map((row) => (
                        <tr key={row.seq}>
                          <td>{row.event_type}</td>
                          <td>{row.actor_id || "none"}</td>
                          <td>{row.step_name || row.row_kind || ""}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : null}
                {scenario === "Recipe" && lineage ? <p>Phase 10 chain {state?.phase10_correlation_id}.</p> : null}
              </section>
            ) : null}
          </div>
        </div>
        <section className="later-checks">
          <h2>Access and untrusted text</h2>
          <button
            type="button"
            onClick={async () => {
              const started = viewRef.current;
              publish("moving", "Opening the case with no identity.");
              const response = await fetch("/api/cases/PS000000016");
              const data = await response.json();
              if (viewRef.current !== started) {
                return;
              }
              const refused = response.status >= 400 || data.ok === false;
              const tone = refused ? (response.status === 401 || response.status === 403 ? "refused" : "failed") : "done";
              publish(tone, refused ? `${data.message || "The case read failed."} No identity headers were sent.` : (data.message || "The case opened."));
              setDetails(JSON.stringify(data, null, 2));
            }}
          >
            Open the case with no identity
          </button>
          <button
            type="button"
            onClick={async () => {
              const started = viewRef.current;
              publish("moving", "Trying to approve from the feed note.");
              const response = await callApi("/api/agent/run", actor, {
                method: "POST",
                body: {
                  case_id: "REPLAY-000000000",
                  scenario: "IC-01",
                  proposed_action: "approve",
                },
              });
              const data = response.data || {};
              if (viewRef.current !== started) {
                return;
              }
              const refused = response.status >= 400 || data.ok === false || data.opa_verdict === "BLOCK";
              const base = data.message || data.opa_verdict || data.error_class || "The feed note was refused.";
              const tone = refused ? "refused" : "done";
              publish(tone, refused ? `${base} The current role is ${actor.role}.` : base);
              setDetails(JSON.stringify(data, null, 2));
            }}
          >
            Try to approve from the feed note
          </button>
          <button type="button" onClick={() => run("/api/demo/gateway/pull", { method: "POST", pending: "Taking the next gateway message." })}>
            Take the next gateway message
          </button>
        </section>
        <details>
          <summary>Details</summary>
          <pre>{details}</pre>
        </details>
      </main>
    </>
  );
}

function Evidence({ scenario, state, lineage, other, holdActor }) {
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
          <tr><td>This delivery</td><td>{state.delivery_status || "not on the queue"}</td></tr>
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
          <tr><td>Hold</td><td>{holdActor ? `recorded by ${holdActor}` : "not recorded"}</td></tr>
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
      return <p>Application A has no lineage route. Open Application B for this trace.</p>;
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

function Action({ scenario, lineage, ownerId, onOwnerId, onRun, onReview, onInvestigate, onHold, onOwner, onCompare }) {
  if (scenario === "Replay") {
    return (
      <div className="action-row">
        <button className="primary" type="button" onClick={onReview}>
          Review this delivery
        </button>
        <button type="button" onClick={() => onRun("/api/demo/replay/drop", { method: "POST", pending: "Recording the drop." })}>
          Drop this duplicate
        </button>
        <p className="role-hint">Drop is recorded only by RT-05 Operations Analyst.</p>
      </div>
    );
  }
  if (scenario === "Recipe") {
    return (
      <div className="action-row">
        <button className="primary" type="button" onClick={onInvestigate}>Explain this mismatch</button>
        <button type="button" onClick={onHold}>Hold</button>
        <p className="role-hint">Hold is recorded only by RT-03 Process Engineer, and that person must differ from the draft author.</p>
      </div>
    );
  }
  if (scenario === "Clocks") {
    return (
      <div className="action-row">
        <button className="primary" type="button" onClick={() => onRun("/api/demo/clocks/apply", { method: "POST", pending: "Placing the event on the timeline." })}>
          Place this event on the timeline
        </button>
      </div>
    );
  }
  if (scenario === "Policy") {
    return (
      <div className="action-row">
        <button className="primary" type="button" onClick={() => onRun("/api/demo/policy/check", { method: "POST", pending: "Asking which policy applies." })}>
          Ask which policy applies
        </button>
        <button type="button" onClick={() => onRun("/api/demo/policy/decide", { method: "POST", pending: "Recording the decision.", body: { choice: "keep-wait" } })}>
          Record my decision
        </button>
        <p className="role-hint">A policy decision is recorded only by RT-04 Policy Owner.</p>
      </div>
    );
  }
  if (scenario === "Outage") {
    return (
      <div className="action-row">
        <button className="primary" type="button" onClick={() => onRun("/api/demo/outage/probe?mode=timeout", { method: "POST", pending: "Checking the upstream link." })}>
          Check the upstream link
        </button>
        <button type="button" onClick={() => onRun("/api/demo/outage/probe?mode=schema", { method: "POST", pending: "Checking the message shape." })}>
          Check the message shape
        </button>
        <button type="button" onClick={() => onRun("/api/demo/outage/park", { method: "POST", pending: "Setting this intake aside." })}>
          Set this intake aside
        </button>
        <button type="button" onClick={() => onRun("/api/demo/outage/replay", { method: "POST", pending: "Bringing the parked intake back." })}>
          Bring the parked intake back
        </button>
        <label>
          Owner
          <input value={ownerId} onChange={(event) => onOwnerId(event.target.value)} />
        </label>
        <button type="button" onClick={onOwner}>Record the owner</button>
        <p className="role-hint">The owner is recorded only by RT-06 Operations Lead.</p>
      </div>
    );
  }
  if (scenario === "Rule trace") {
    return lineage ? (
      <div className="action-row">
        <button className="primary" type="button" onClick={() => onRun("/api/demo/rule-trace", { method: "GET", pending: "Reading the rule path." })}>
          Show where this rule came from
        </button>
      </div>
    ) : (
      <p>Open Application B for the rule trace.</p>
    );
  }
  return (
    <div className="action-row">
      <button className="primary" type="button" onClick={onCompare}>Compare this case</button>
    </div>
  );
}
