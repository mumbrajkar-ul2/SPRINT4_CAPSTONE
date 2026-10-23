import { go, hoursBetween, landingPath, PageHead, Quiet, useFetch } from "./kit.jsx";

const PLACES = [
  ["nav.dashboard", "page.dashboard.sentence", "/dashboard"],
  ["nav.cases", "page.cases.sentence", "/cases"],
  ["nav.approvals", "page.approvals.sentence", "/approvals"],
  ["nav.scenarios", "page.scenarios.sentence", "/scenarios/Replay"],
  ["nav.lots", "page.lots.sentence", "/lots"],
  ["nav.partners", "page.partners.sentence", "/partners/partner_feeds"],
  ["nav.graph", "page.graph.sentence", "/graph"],
  ["nav.glossary", "page.glossary.sentence", "/glossary"],
  ["nav.audit", "page.audit.sentence", "/audit"],
  ["nav.kpis", "page.kpis.sentence", "/kpis"],
  ["nav.faults", "page.faults.sentence", "/faults"],
];

export function Home({ t, fab, me, lineage, onUnauth }) {
  const query = fab ? `?fab=${encodeURIComponent(fab)}` : "";
  const dash = useFetch(`/api/dashboard${query}`, onUnauth);
  const notes = useFetch("/api/notifications", onUnauth);
  const pending = useFetch("/api/approvals/pending?limit=1", onUnauth);
  const audit = useFetch("/api/audit/search?order=desc&limit=5", onUnauth);
  const path = landingPath(me?.roles);
  const waiting = pending.data?.total ?? 0;
  const nextSentence = path === "/approvals"
    ? (waiting === 1 ? "1 item is waiting for your role." : waiting ? `${waiting} items are waiting for your role.` : "Nothing is waiting for your role.")
    : t(path === "/cases" ? "page.cases.sentence" : path === "/lots" ? "page.lots.sentence" : path === "/partners" ? "page.partners.sentence" : path === "/audit" ? "page.audit.sentence" : "page.dashboard.sentence");
  const holds = (dash.data?.engineering_holds || []).filter((row) => row.sla_breached);
  const openCount = (dash.data?.open_cases?.by_status || []).reduce((sum, row) => sum + Number(row.n || 0), 0);
  if (dash.loading) {
    return <p role="status">Loading the home page.</p>;
  }
  if (dash.error) {
    return <p role="status">{dash.error}</p>;
  }
  const sites = fab ? fab : (me?.sites || []).join(" and ") || "the sites on this sign-in";
  return (
    <div>
      <PageHead kicker="Force Fab" title={t("page.home.title")} sentence={t("page.home.sentence")} />
      <p>{me?.name}. {(me?.roles || []).join(", ")}</p>
      <p>Showing {sites}.</p>
      <p>{lineage ? t("app.b") : t("app.a")}</p>
      <section className="ff-card">
        <h2>{path === "/approvals" ? t("page.approvals.title") : "Next page"}</h2>
        <p>{nextSentence}</p>
        <button type="button" className="primary" onClick={() => go(path)}>Open</button>
      </section>
      <div className="ff-counts">
        <button type="button" className="ff-card" onClick={() => go("/dashboard")}>
          <strong>{openCount}</strong>
          <span>Open cases</span>
        </button>
        <button type="button" className="ff-card" onClick={() => go("/dashboard")}>
          <strong>{holds.length}</strong>
          <span>Holds past 24 hours, against the latest step in this file.</span>
        </button>
        <button type="button" className="ff-card" onClick={() => go("/dashboard")}>
          <strong>{dash.data?.scrap?.amount_usd}</strong>
          <span>Scrap estimate</span>
        </button>
      </div>
      <h2>Holds past the timer</h2>
      <p>{dash.data?.clock_note}</p>
      {holds.length ? holds.map((row) => (
        <p key={row.lot_id}>
          Lot {row.lot_id} is past the 24 hour hold. {hoursBetween(row.latest_step, row.now) == null ? "" : `${hoursBetween(row.latest_step, row.now)} hours.`}
          {" "}
          <Quiet onClick={() => go(`/lots/${encodeURIComponent(row.lot_id)}`)}>Open lot</Quiet>
        </p>
      )) : <p>No hold is past the timer on these sites.</p>}
      <h2>Latest recorded writes</h2>
      {audit.data?.items?.length ? audit.data.items.map((row) => (
        <p key={`${row.seq}-${row.audit_id || row.correlation_id}`}>
          {row.occurred_at || row.event_type} {row.actor_id || ""} {row.case_id || ""}
          {row.case_id ? <Quiet onClick={() => go(`/audit?case=${encodeURIComponent(row.case_id)}`)}>Open audit</Quiet> : null}
        </p>
      )) : <p>The audit file has no rows yet.</p>}
      <h2>Places in Force Fab</h2>
      <div className="ff-places">
        {PLACES.map(([label, sentence, href]) => (
          <p key={href}><Quiet onClick={() => go(href)}>{t(label)}</Quiet> {t(sentence)}</p>
        ))}
      </div>
      {notes.error ? <p>{notes.error}</p> : null}
    </div>
  );
}
