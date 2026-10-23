import { useState } from "react";
import { callRaw } from "../api.js";
import { go, PageHead, Quiet, useFetch } from "./kit.jsx";

const LEAD = ["occurred_at", "actor_id", "event_type", "case_id"];

export function Audit({ t, route, onUnauth }) {
  const [draft, setDraft] = useState({
    actor: route.params.get("actor") || "",
    case: route.params.get("case") || "",
    from: route.params.get("from") || "",
    to: route.params.get("to") || "",
  });
  const [offset, setOffset] = useState(0);
  const [open, setOpen] = useState("");
  const query = new URLSearchParams();
  ["actor", "case", "from", "to"].forEach((key) => {
    if (route.params.get(key)) {
      query.set(key, route.params.get(key));
    }
  });
  query.set("limit", "50");
  query.set("offset", String(offset));
  const data = useFetch(`/api/audit/search?${query.toString()}`, onUnauth);

  function apply(event) {
    event.preventDefault();
    const params = new URLSearchParams();
    Object.entries(draft).forEach(([key, value]) => {
      if (value) {
        params.set(key, value);
      }
    });
    go(`/audit?${params.toString()}`);
    setOffset(0);
  }

  async function download() {
    const params = new URLSearchParams(query);
    params.set("format", "csv");
    const response = await callRaw(`/api/audit/search?${params.toString()}`);
    if (response.status === 401) {
      onUnauth();
      return;
    }
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "audit.csv";
    link.click();
    URL.revokeObjectURL(url);
  }

  const rows = data.data?.items || [];
  return (
    <div>
      <PageHead kicker="Force Fab" title={t("page.audit.title")} sentence={t("page.audit.sentence")} />
      <form onSubmit={apply} className="ff-filters">
        <label>Actor<input value={draft.actor} onChange={(event) => setDraft({ ...draft, actor: event.target.value })} placeholder="actor" /></label>
        <label>Case<input value={draft.case} onChange={(event) => setDraft({ ...draft, case: event.target.value })} placeholder="case" /></label>
        <label>From<input value={draft.from} onChange={(event) => setDraft({ ...draft, from: event.target.value })} placeholder="from" /></label>
        <label>To<input value={draft.to} onChange={(event) => setDraft({ ...draft, to: event.target.value })} placeholder="to" /></label>
        <button type="submit" className="primary">{t("btn.apply")}</button>
        <Quiet onClick={download}>Download CSV</Quiet>
      </form>
      {data.loading ? <p role="status">Loading the audit.</p> : null}
      {data.error ? <p role="status">{data.error}</p> : null}
      {data.data && rows.length === 0 ? <p>No audit row matches these filters.</p> : null}
      {rows.map((row, index) => {
        const key = `${row.seq}-${index}`;
        const rest = Object.keys(row).filter((name) => !LEAD.includes(name));
        return (
          <article key={key} className="ff-card">
            <button type="button" className="quiet" onClick={() => setOpen(open === key ? "" : key)}>
              {row.occurred_at} {row.actor_id} {row.event_type}
            </button>
            {row.case_id ? <Quiet onClick={() => go(`/cases/${encodeURIComponent(row.case_id)}`)}>{row.case_id}</Quiet> : null}
            {open === key ? <p>{rest.map((name) => `${name}: ${row[name] ?? ""}`).join(". ")}</p> : null}
          </article>
        );
      })}
      {data.data ? (
        <p>
          <Quiet disabled={offset <= 0} onClick={() => setOffset(Math.max(0, offset - 50))}>Previous</Quiet>
          <Quiet disabled={offset + 50 >= data.data.total} onClick={() => setOffset(offset + 50)}>Next</Quiet>
        </p>
      ) : null}
    </div>
  );
}
