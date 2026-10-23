import { useEffect, useState } from "react";
import { callApi } from "../api.js";

export const ENGLISH = {
  "nav.home": "Home",
  "nav.dashboard": "Dashboard",
  "nav.cases": "Cases",
  "nav.approvals": "Approvals",
  "nav.scenarios": "Scenarios",
  "nav.lots": "Lot genealogy & SPC",
  "nav.partners": "Partner feeds",
  "nav.graph": "Knowledge graph",
  "nav.glossary": "Glossary",
  "nav.audit": "Audit",
  "nav.kpis": "A-vs-B KPIs",
  "nav.faults": "Fault scenarios",
  "header.sites": "All my sites",
  "header.language": "Language",
  "header.signout": "Logout",
  "btn.apply": "Apply",
  "btn.show_graph": "Show graph",
  "btn.show_lot": "Show lot",
  "btn.search": "Search",
  "btn.sign": "Sign",
  "btn.back": "Back",
  "btn.clear": "Clear",
  "page.home.title": "Home",
  "page.home.sentence": "See what is waiting on this shift, then open that page.",
  "page.dashboard.title": "Dashboard",
  "page.dashboard.sentence": "Open cases, holds, and yield for the sites on this sign-in.",
  "page.cases.title": "Cases",
  "page.cases.sentence": "Find a case on your sites and read its timeline.",
  "page.approvals.title": "Approvals",
  "page.approvals.sentence": "Read the waiting item, then sign it.",
  "page.scenarios.title": "Scenarios",
  "page.scenarios.sentence": "The seven demo cases: replay, recipe, clocks, policy, outage, rule trace, and compare.",
  "page.lots.title": "Lot genealogy and SPC",
  "page.lots.sentence": "Follow a lot through its steps, then read the control chart for one measurement.",
  "page.partners.title": "Partner feeds",
  "page.partners.sentence": "Partner deliveries, batch runs, reference versions, outages, and policy exceptions.",
  "page.graph.title": "Knowledge graph",
  "page.graph.sentence": "Item relationships derived from the legacy data.",
  "page.glossary.title": "Glossary",
  "page.glossary.sentence": "One name for each term, and the local words that map to it.",
  "page.audit.title": "Audit",
  "page.audit.sentence": "The recorded writes, in the order they were stored.",
  "page.kpis.title": "A-vs-B KPIs",
  "page.kpis.sentence": "Measured figures, and the cells this demo has not measured.",
  "page.faults.title": "Fault scenarios",
  "page.faults.sentence": "Four checks over lots, tools, wafers, and supplier parts.",
  "app.a": "This app drafts an answer with the model, then a person signs any change.",
  "app.b": "This app answers from the Context Lake and does not call the model.",
  "link.all": "All links",
  "link.maps_to": "maps to",
  "link.implements": "implements",
  "link.conflicts_with": "conflicts with",
  "link.supersedes": "supersedes",
  "link.governs": "governs",
  "link.evidenced_by": "evidenced by",
  "link.depends_on": "depends on",
  "link.tested_by": "tested by",
};

export const MENU = [
  ["home", "nav.home", "/home"],
  ["dashboard", "nav.dashboard", "/dashboard"],
  ["cases", "nav.cases", "/cases"],
  ["approvals", "nav.approvals", "/approvals"],
  ["scenarios", "nav.scenarios", "/scenarios"],
  ["lots", "nav.lots", "/lots"],
  ["partners", "nav.partners", "/partners"],
  ["graph", "nav.graph", "/graph"],
  ["glossary", "nav.glossary", "/glossary"],
  ["audit", "nav.audit", "/audit"],
  ["kpis", "nav.kpis", "/kpis"],
  ["faults", "nav.faults", "/faults"],
];

export const ROLE_PAGE = {
  "RT-01": "/cases",
  "RT-02": "/approvals",
  "RT-03": "/lots",
  "RT-04": "/approvals",
  "RT-05": "/partners",
  "RT-06": "/dashboard",
  "FF-AUDITOR": "/audit",
  "FF-ADMIN": "/dashboard",
};

export function landingPath(roles) {
  const list = roles || [];
  const rt = list.find((role) => String(role).startsWith("RT-"));
  if (rt && ROLE_PAGE[rt]) {
    return ROLE_PAGE[rt];
  }
  if (list.includes("FF-AUDITOR")) {
    return ROLE_PAGE["FF-AUDITOR"];
  }
  if (list.includes("FF-ADMIN")) {
    return ROLE_PAGE["FF-ADMIN"];
  }
  return "/home";
}

export function parseHash() {
  const raw = (window.location.hash || "#/home").replace(/^#/, "");
  const [pathPart, query = ""] = raw.split("?");
  const parts = pathPart.split("/").filter(Boolean);
  return { parts, params: new URLSearchParams(query), page: parts[0] || "home" };
}

export function go(path) {
  const next = path.startsWith("#") ? path : `#${path}`;
  if (window.location.hash !== next) {
    window.location.hash = next;
  }
}

export function PageHead({ kicker, title, sentence, children }) {
  return (
    <header className="ff-page-head">
      <p className="band-kicker">{kicker}</p>
      <h1 className="ff-title">{title}</h1>
      <p>{sentence}</p>
      {children}
    </header>
  );
}

export function Quiet({ children, onClick, disabled, pressed }) {
  return (
    <button type="button" className="quiet" onClick={onClick} disabled={disabled} aria-pressed={pressed}>
      {children}
    </button>
  );
}

export function useFetch(path, onUnauth) {
  const [state, setState] = useState({ loading: true, error: "", data: null });
  useEffect(() => {
    let live = true;
    if (!path) {
      setState({ loading: false, error: "", data: null });
      return undefined;
    }
    setState({ loading: true, error: "", data: null });
    callApi(path, {}).then((response) => {
      if (!live) {
        return;
      }
      if (response.status === 401) {
        onUnauth();
        return;
      }
      if (response.status >= 400 || response.data?.ok === false) {
        setState({ loading: false, error: response.data?.message || "The request failed.", data: null });
        return;
      }
      setState({ loading: false, error: "", data: response.data });
    }).catch((error) => {
      if (live) {
        setState({ loading: false, error: String(error), data: null });
      }
    });
    return () => {
      live = false;
    };
  }, [path, onUnauth]);
  return state;
}

export function DataTable({ rows, total, offset, limit, onPage }) {
  if (!rows || !rows.length) {
    return null;
  }
  const keys = Object.keys(rows[0]);
  const idKey = keys.find((key) => key === "id" || key.endsWith("_id")) || keys[0];
  const ordered = [idKey, ...keys.filter((key) => key !== idKey)];
  const end = Math.min(offset + rows.length, total ?? rows.length);
  return (
    <div>
      <p>{total ?? rows.length} rows. Showing {offset + 1}–{end}.</p>
      <div className="evidence-scroll">
        <table>
          <thead>
            <tr>{ordered.map((key) => <th key={key}>{key}</th>)}</tr>
          </thead>
          <tbody>
            {rows.map((row, index) => (
              <tr key={index}>
                {ordered.map((key) => <td key={key}>{row[key] == null ? "" : String(row[key])}</td>)}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {onPage ? (
        <p>
          <Quiet disabled={offset <= 0} onClick={() => onPage(Math.max(0, offset - limit))}>Previous</Quiet>
          {" "}
          <Quiet disabled={offset + limit >= (total ?? rows.length)} onClick={() => onPage(offset + limit)}>Next</Quiet>
        </p>
      ) : null}
    </div>
  );
}

export function shortLabel(text) {
  const words = String(text || "").split(/\s+/).filter(Boolean);
  let out = "";
  for (const word of words) {
    const next = out ? `${out} ${word}` : word;
    if (next.length > 28) {
      break;
    }
    out = next;
  }
  return out || String(text || "").slice(0, 28);
}

export function hoursBetween(start, end) {
  const a = Date.parse(start || "");
  const b = Date.parse(end || "");
  if (Number.isNaN(a) || Number.isNaN(b)) {
    return null;
  }
  return Math.round((b - a) / 36e5);
}

export function AskPanel({ lineage, subject, id, onUnauth, onStepUp }) {
  const [mode, setMode] = useState("");
  const [waiting, setWaiting] = useState(false);
  const [error, setError] = useState("");
  const [answer, setAnswer] = useState(null);
  async function ask(nextMode) {
    setMode(nextMode);
    setWaiting(true);
    setError("");
    const response = await callApi("/api/ask", {}, { method: "POST", body: { subject, id, mode: nextMode } });
    setWaiting(false);
    if (response.status === 401) {
      if (response.data?.error_class === "step_up_required") {
        setError(response.data.message || "Sign in again with a one-time code.");
        if (onStepUp) {
          onStepUp();
        }
        return;
      }
      onUnauth();
      return;
    }
    if (response.status >= 400 || response.data?.ok === false) {
      setError(response.data?.message || "The request failed.");
      return;
    }
    setAnswer(response.data);
  }
  const title = lineage ? "Context Lake answer" : "Ask Force Fab AI";
  const verdict = answer?.verdict || "";
  return (
    <section className="ask-panel band">
      <h2>{title}</h2>
      <Quiet onClick={() => ask("explain")} disabled={waiting || !id}>Explain</Quiet>
      {" "}
      <Quiet onClick={() => ask("plan")} disabled={waiting || !id}>Draft a plan</Quiet>
      {waiting ? <p role="status">The model is reading the evidence, for up to 30 seconds.</p> : null}
      {error ? <p role="status">{error}</p> : null}
      {answer ? (
        <div>
          <p>{verdict === "ABSTAIN" ? "No grounded answer. No claim is made." : verdict}</p>
          <p>{answer.source_badge?.label || ""}</p>
          <p>{answer.latency_ms} ms</p>
          <p className="result-sentence">{answer.sentence}</p>
          {answer.draft_plan ? <p>{answer.draft_plan}</p> : null}
          <p>
            {(answer.citations || []).map((item) => (
              <Quiet key={item} onClick={() => go(`/graph/${encodeURIComponent(item)}`)}>{item}</Quiet>
            ))}
          </p>
          <p>{answer.next_step}</p>
          {lineage && answer.rule_trace ? (
            <div>
              <p>{answer.rule_trace_basis === "subject_definitions" ? "These rows define the subject." : "Rule trace"}</p>
              <table>
                <tbody>
                  {answer.rule_trace.map((row) => (
                    <tr key={row.id || row.item_id}>
                      <td>{row.kind}</td>
                      <td>{row.statement || row.id}</td>
                      <td>{row.trust}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : null}
          <p className="sr-only">{mode}</p>
        </div>
      ) : null}
    </section>
  );
}
