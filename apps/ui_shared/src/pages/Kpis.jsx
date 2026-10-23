import { go, PageHead, Quiet, useFetch } from "./kit.jsx";

function amount(row) {
  for (const key of ["amount", "cost", "usd"]) {
    if (row[key] != null && row[key] !== "" && !Number.isNaN(Number(row[key]))) {
      return Number(row[key]);
    }
  }
  return null;
}

export function Kpis({ t, onUnauth }) {
  const compare = useFetch("/api/kpi/compare", onUnauth);
  const costs = useFetch("/api/costs", onUnauth);
  if (compare.loading) {
    return <p role="status">Loading the KPIs.</p>;
  }
  if (compare.error) {
    return <p role="status">{compare.error}</p>;
  }
  const periods = costs.data?.periods || [];
  const amounts = periods.map(amount);
  const highest = amounts.some((value) => value != null) ? Math.max(...amounts.filter((value) => value != null)) : null;
  return (
    <div>
      <PageHead kicker="Force Fab" title={t("page.kpis.title")} sentence={t("page.kpis.sentence")} />
      {(compare.data?.cells || []).map((cell) => (
        <p key={cell.name}>
          {cell.name}
          {cell.value == null ? ` Unknown. ${cell.note || ""} ${cell.source || ""}` : ` ${cell.value}`}
          {cell.value == null ? null : <span className="ff-bar-track"><span className="ff-bar-fill" style={{ width: "40%" }} /></span>}
          {cell.value != null && cell.source ? <span> {cell.source}</span> : null}
        </p>
      ))}
      <section className="ff-card">
        <h2>Scrap rate</h2>
        <p>{compare.data?.scrap_rate?.usd_per_defect} USD. estimate. (est.)</p>
        <svg width="180" height="16" aria-hidden="true"><pattern id="est" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0 6 L6 0" stroke="var(--accent)" /></pattern><rect width="180" height="16" fill="url(#est)" /></svg>
        <Quiet onClick={() => go("/dashboard")}>Chamber list</Quiet>
      </section>
      <h2>Costs</h2>
      {periods.map((row, index) => (
        <p key={index}>{row.period || index} {amount(row) ?? ""} {highest != null && amount(row) === highest ? "Highest" : ""} {row.label || ""}</p>
      ))}
      <p>{costs.data?.scrap?.label} {costs.data?.scrap?.note}</p>
      <Quiet onClick={() => go("/scenarios/Compare")}>Open the Compare tab</Quiet>
    </div>
  );
}
