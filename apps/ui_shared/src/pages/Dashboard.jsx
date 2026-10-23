import { go, hoursBetween, PageHead, useFetch } from "./kit.jsx";

function Bars({ rows, labelKey, countKey, onOpen }) {
  const max = Math.max(1, ...rows.map((row) => Number(row[countKey] || 0)));
  return rows.map((row) => {
    const name = row[labelKey] || "none";
    const count = Number(row[countKey] || 0);
    return (
      <button type="button" className="ff-bar" key={String(name)} onClick={() => onOpen(row)}>
        <span>{name}</span>
        <span className="ff-bar-track"><span className="ff-bar-fill" style={{ width: `${(count / max) * 100}%` }} /></span>
        <span>{count}</span>
      </button>
    );
  });
}

export function Dashboard({ t, fab, onUnauth }) {
  const query = fab ? `?fab=${encodeURIComponent(fab)}` : "";
  const dash = useFetch(`/api/dashboard${query}`, onUnauth);
  if (dash.loading) {
    return <p role="status">Loading the dashboard.</p>;
  }
  if (dash.error) {
    return <p role="status">{dash.error}</p>;
  }
  const data = dash.data;
  const openCount = (data.open_cases?.by_status || []).reduce((sum, row) => sum + Number(row.n || 0), 0);
  const holds = [...(data.engineering_holds || [])];
  const timed = holds.every((row) => hoursBetween(row.latest_step, row.now) != null);
  if (timed) {
    holds.sort((a, b) => hoursBetween(b.latest_step, b.now) - hoursBetween(a.latest_step, a.now));
  }
  const past = holds.filter((row) => row.sla_breached).length;
  const yieldValue = data.yield?.value == null ? "Unknown" : Number(data.yield.value).toFixed(1);
  return (
    <div>
      <PageHead kicker="Force Fab" title={t("page.dashboard.title")} sentence={t("page.dashboard.sentence")}>
        <p>{data.clock_note}</p>
      </PageHead>
      <div className="ff-counts">
        <div className="ff-card"><strong>{openCount}</strong><span>Open cases</span></div>
        <div className="ff-card"><strong>{past}</strong><span>Holds past 24 hours</span></div>
        <div className="ff-card"><strong>{yieldValue}</strong><span>{data.yield?.value == null ? "Unknown" : "Yield, measured"}</span></div>
        <div className="ff-card"><strong>{data.scrap?.amount_usd}</strong><span>Scrap estimate, {data.scrap?.usd_per_defect} USD</span></div>
        <div className="ff-card"><strong>Unknown</strong><span>MTTA. {data.mtta?.note}</span></div>
        <div className="ff-card"><strong>Unknown</strong><span>MTTR. {data.mttr?.note}</span></div>
      </div>
      <h2>Status</h2>
      <Bars rows={data.open_cases?.by_status || []} labelKey="status" countKey="n" onOpen={(row) => go(`/cases?status=${encodeURIComponent(row.status || "")}`)} />
      <h2>Severity</h2>
      <Bars rows={data.open_cases?.by_severity || []} labelKey="severity" countKey="n" onOpen={(row) => go(`/cases?severity=${encodeURIComponent(row.severity || "")}`)} />
      <h2>Site</h2>
      <Bars rows={data.open_cases?.by_site || []} labelKey="site" countKey="n" onOpen={(row) => go(`/cases?site=${encodeURIComponent(row.site || "")}`)} />
      <h2>Holds</h2>
      <table>
        <tbody>
          {holds.map((row) => {
            const age = hoursBetween(row.latest_step, row.now);
            return (
              <tr key={row.lot_id}>
                <td><button type="button" className="quiet" onClick={() => go(`/lots/${encodeURIComponent(row.lot_id)}`)}>{row.lot_id}</button></td>
                <td>{row.tool_id}</td>
                <td>{row.defect_count}</td>
                <td>{age == null ? `${row.latest_step || ""} ${row.now || ""}` : `${age} hours`}</td>
                <td>{row.sla_breached ? "Past 24 hours" : "Inside 24 hours"}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
      <p>{data.link_note}</p>
      <h2>Every lot in the legacy file.</h2>
      {(data.scrap_by_chamber || []).map((row) => (
        <p key={row.chamber}>{row.chamber}: {row.defect_count} defects, {row.amount_usd} USD, {row.label}</p>
      ))}
    </div>
  );
}
