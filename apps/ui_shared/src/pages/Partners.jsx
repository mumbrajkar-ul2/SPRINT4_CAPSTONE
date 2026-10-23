import { useState } from "react";
import { DataTable, go, PageHead, Quiet, useFetch } from "./kit.jsx";

const TABS = [
  ["partner_feeds", "Feeds"],
  ["batch_runs", "Batch runs"],
  ["reference_versions", "Reference versions"],
  ["upstream_outages", "Upstream outages"],
  ["policy_exceptions", "Policy exceptions"],
];

export function Partners({ t, route, onUnauth }) {
  const table = TABS.some(([id]) => id === route.parts[1]) ? route.parts[1] : "partner_feeds";
  const [q, setQ] = useState(route.params.get("q") || "");
  const [offset, setOffset] = useState(Number(route.params.get("offset") || 0));
  const status = route.params.get("status") || "";
  const query = new URLSearchParams();
  if (route.params.get("q")) {
    query.set("q", route.params.get("q"));
  }
  if (status) {
    query.set("status", status);
  }
  query.set("limit", "50");
  query.set("offset", String(offset));
  const data = useFetch(`/api/partners/${table}?${query.toString()}`, onUnauth);

  function open(nextTable, extra = {}) {
    const params = new URLSearchParams();
    if (extra.q) {
      params.set("q", extra.q);
    }
    if (extra.status) {
      params.set("status", extra.status);
    }
    go(`/partners/${nextTable}?${params.toString()}`);
    setOffset(0);
  }

  const body = data.data || {};
  const rejection = body.rejection_rate?.measured ? `${Math.round(body.rejection_rate.value * 1000) / 10}%` : "Unknown";
  return (
    <div>
      <PageHead kicker="Force Fab" title={t("page.partners.title")} sentence={t("page.partners.sentence")} />
      <div className="ff-counts">
        <Quiet onClick={() => open("batch_runs")}>Rejection rate {rejection}</Quiet>
        <Quiet onClick={() => open("partner_feeds")}>Retry rate {body.retry_rate?.note || "Unknown"}</Quiet>
        <Quiet onClick={() => open("reference_versions")}>Reference keys {body.reference_version_drift?.value ?? ""}</Quiet>
      </div>
      <div className="scenario-bar" role="tablist">
        {TABS.map(([id, label]) => (
          <button type="button" role="tab" key={id} className={id === table ? "scenario-current" : undefined} aria-selected={id === table} onClick={() => open(id, { q: route.params.get("q") || "", status: id === "partner_feeds" ? status : "" })}>{label}</button>
        ))}
      </div>
      <form className="ff-filters" onSubmit={(event) => { event.preventDefault(); open(table, { q, status }); }}>
        <label>Search<input value={q} onChange={(event) => setQ(event.target.value)} /></label>
        <button type="submit" className="primary">{t("btn.search")}</button>
        {table === "partner_feeds" ? (
          <Quiet pressed={status === "REPLAY"} onClick={() => open(table, { q: route.params.get("q") || "", status: status === "REPLAY" ? "" : "REPLAY" })}>Replay only</Quiet>
        ) : null}
      </form>
      <p>The replay demo is the Replay tab. <Quiet onClick={() => go("/scenarios/Replay")}>Replay</Quiet></p>
      {data.loading ? <p role="status">Loading the partner feeds.</p> : null}
      {data.error ? <p role="status">{data.error}</p> : null}
      {body.items && body.items.length === 0 ? <p>{route.params.get("q") || status ? "No row matches this search." : "This table has no rows."}</p> : null}
      {(body.items || []).some((row) => row.processing_status === "REPLAY") ? <p>Replay marks the rows whose processing status is REPLAY.</p> : null}
      {(body.items || []).map((row) => {
        const blob = JSON.stringify(row);
        const match = blob.match(/C\d+/);
        return match ? <Quiet key={match[0] + (row.feed_id || "")} onClick={() => go(`/cases/${encodeURIComponent(match[0])}`)}>Open case {match[0]}</Quiet> : null;
      })}
      <details>
        <summary>All columns</summary>
        <DataTable rows={body.items || []} total={body.total || 0} offset={body.offset || 0} limit={body.limit || 50} onPage={setOffset} />
      </details>
    </div>
  );
}
