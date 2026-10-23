import { useState } from "react";
import { AskPanel, go, PageHead, Quiet, useFetch } from "./kit.jsx";

const LOT = /L\d+/g;

function lotIds(detail) {
  const found = new Set();
  const blob = JSON.stringify(detail?.case || {}) + JSON.stringify(detail?.timeline || []);
  for (const match of blob.match(LOT) || []) {
    found.add(match);
  }
  return [...found];
}

export function Cases({ t, fab, lineage, route, onUnauth, onStepUp }) {
  const params = route.params;
  const caseId = route.parts[1] && route.parts[1] !== "" ? decodeURIComponent(route.parts[1]) : "";
  const [draft, setDraft] = useState({
    status: params.get("status") || "",
    severity: params.get("severity") || "",
    segment: params.get("segment") || "",
    q: params.get("q") || "",
  });
  const site = params.get("site") || "";
  const query = new URLSearchParams();
  ["status", "severity", "segment", "q"].forEach((key) => {
    if (params.get(key)) {
      query.set(key, params.get(key));
    }
  });
  if (site) {
    query.set("site", site);
  }
  if (fab && !site) {
    query.set("fab", fab);
  }
  const list = useFetch(`/api/cases?${query.toString()}`, onUnauth);
  const detail = useFetch(caseId ? `/api/cases/${encodeURIComponent(caseId)}/detail` : "", onUnauth);
  function apply(event) {
    event?.preventDefault();
    const next = new URLSearchParams();
    Object.entries(draft).forEach(([key, value]) => {
      if (value) {
        next.set(key, value);
      }
    });
    if (site) {
      next.set("site", site);
    }
    go(`/cases?${next.toString()}`);
  }
  const narrow = typeof window !== "undefined" && window.innerWidth < 800 && caseId;
  return (
    <div>
      <PageHead kicker="Force Fab" title={t("page.cases.title")} sentence={t("page.cases.sentence")} />
      <form onSubmit={apply} className="ff-filters">
        <label>Status<input value={draft.status} onChange={(event) => setDraft({ ...draft, status: event.target.value })} placeholder="status" /></label>
        <label>Severity<input value={draft.severity} onChange={(event) => setDraft({ ...draft, severity: event.target.value })} placeholder="severity" /></label>
        <label>Segment<input value={draft.segment} onChange={(event) => setDraft({ ...draft, segment: event.target.value })} placeholder="segment" /></label>
        <label>Search<input value={draft.q} onChange={(event) => setDraft({ ...draft, q: event.target.value })} placeholder="search" /></label>
        <button type="submit" className="primary">{t("btn.apply")}</button>
        <Quiet onClick={() => go("/cases")}>{t("btn.clear")}</Quiet>
      </form>
      {site ? <p>Site {site}. <Quiet onClick={() => go("/cases")}>Clear</Quiet></p> : null}
      {list.loading ? <p role="status">Loading the cases.</p> : null}
      {list.error ? <p role="status">{list.error}</p> : null}
      <div className={narrow ? "" : "ff-split"}>
        {narrow ? null : (
          <div>
            <p>{list.data ? `${list.data.total} cases. Showing ${list.data.offset + 1}–${Math.min(list.data.offset + (list.data.items || []).length, list.data.total)}.` : ""}</p>
            {(list.data?.items || []).map((row) => (
              <p key={row.id}><Quiet pressed={row.id === caseId} onClick={() => go(`/cases/${encodeURIComponent(row.id)}?${query.toString()}`)}>{row.id}</Quiet> {row.status} {row.severity} {row.site}</p>
            ))}
          </div>
        )}
        <div>
          {caseId && narrow ? <Quiet onClick={() => go(`/cases?${query.toString()}`)}>{t("btn.back")}</Quiet> : null}
          {!caseId ? <p>Choose a case.</p> : null}
          {caseId && detail.loading ? <p role="status">Loading the case.</p> : null}
          {caseId && detail.error ? <p role="status">{detail.error}</p> : null}
          {detail.data?.case ? (
            <article>
              <h2>{detail.data.case.id} {detail.data.case.status}</h2>
              <p>{detail.data.case.status}. {detail.data.case.severity}. {detail.data.case.site}. {detail.data.case.sales_region}. {detail.data.case.segment}</p>
              <h3>Timeline</h3>
              {(detail.data.timeline || []).map((row, index) => (
                <p key={index}>{row.recorded_at || row.occurred_at} {row.event_type || row.kind || row.note}</p>
              ))}
              <h3>Policies</h3>
              {(() => {
                const named = (detail.data.policies || []).filter((row) => JSON.stringify(row).includes(caseId));
                return named.length ? named.map((row, index) => <p key={index}>{JSON.stringify(row)}</p>) : <p>No policy exception names this case.</p>;
              })()}
              <p>{detail.data.link_note}</p>
              {lotIds(detail.data).map((lot) => (
                <Quiet key={lot} onClick={() => go(`/lots/${encodeURIComponent(lot)}`)}>Open lot {lot}</Quiet>
              ))}
              <details>
                <summary>All columns</summary>
                <pre>{JSON.stringify(detail.data.case, null, 2)}</pre>
              </details>
              <AskPanel lineage={lineage} subject="case" id={caseId} onUnauth={onUnauth} onStepUp={onStepUp} />
            </article>
          ) : null}
        </div>
      </div>
    </div>
  );
}
