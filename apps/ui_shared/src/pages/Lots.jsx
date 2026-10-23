import { useEffect, useState } from "react";
import { AskPanel, PageHead, Quiet, useFetch } from "./kit.jsx";

export function Lots({ t, lineage, route, onUnauth, onStepUp }) {
  const lotFromHash = route.parts[1] ? decodeURIComponent(route.parts[1]) : "";
  const paramFromHash = route.parts[2] === "spc" && route.parts[3] ? decodeURIComponent(route.parts[3]) : "";
  const [lot, setLot] = useState(lotFromHash);
  const active = lotFromHash;
  const [tool, setTool] = useState("");
  const [showAll, setShowAll] = useState(false);
  const [point, setPoint] = useState(null);
  const mismatches = route.params.get("mismatches") === "1";
  const genealogy = useFetch(active ? `/api/lots/${encodeURIComponent(active)}/genealogy` : "", onUnauth);
  const metro = useFetch(active ? `/api/domain/metrology?q=${encodeURIComponent(active)}&limit=200` : "", onUnauth);
  const chart = useFetch(paramFromHash ? `/api/spc/${encodeURIComponent(paramFromHash)}` : "", onUnauth);
  const steps = (genealogy.data?.steps || []).filter((step) => {
    if (mismatches && !step.recipe_mismatch && !step.ecn_conflict) {
      return false;
    }
    if (tool && step.tool_id !== tool) {
      return false;
    }
    return true;
  });
  const allSteps = genealogy.data?.steps || [];
  const mismatchCount = allSteps.filter((step) => step.recipe_mismatch).length;
  const parameters = [...new Set((metro.data?.items || []).filter((row) => row.lot_id === active).map((row) => row.parameter).filter(Boolean))];
  useEffect(() => {
    setLot(lotFromHash);
  }, [lotFromHash]);
  const series = chart.data?.items || [];
  const shown = showAll ? series : series.slice(-12);

  function showLot(event) {
    event?.preventDefault();
    const id = lot.trim();
    if (!id) {
      return;
    }
    const flag = mismatches ? "?mismatches=1" : "";
    window.location.hash = `#/lots/${encodeURIComponent(id)}${flag}`;
  }

  function chartPath(parameter) {
    const flag = mismatches ? "?mismatches=1" : "";
    window.location.hash = `#/lots/${encodeURIComponent(active)}/spc/${encodeURIComponent(parameter)}${flag}`;
  }

  return (
    <div>
      <PageHead kicker="Force Fab" title={t("page.lots.title")} sentence={t("page.lots.sentence")} />
      <p>This lot list is every lot in the file, not a fab slice.</p>
      <form className="ff-filters" onSubmit={showLot}>
        <label>Lot id<input placeholder="L00000016" value={lot} onChange={(event) => setLot(event.target.value)} /></label>
        <button type="submit" className="primary">{t("btn.show_lot")}</button>
      </form>
      {genealogy.loading && active ? <p role="status">Loading the lot.</p> : null}
      {genealogy.error ? <p role="status">{genealogy.error}</p> : null}
      {genealogy.data?.lot ? (
        <div>
          <p>
            Yield {genealogy.data.lot.measured_yield ?? "Unknown"}. Defects {genealogy.data.lot.defect_count}. {Number(genealogy.data.lot.engineering_hold) ? "On hold" : "Not on hold"}. {mismatchCount} of {allSteps.length} steps use a different recipe on the tool.
          </p>
          <Quiet pressed={mismatches} onClick={() => { window.location.hash = `#/lots/${encodeURIComponent(active)}${mismatches ? "" : "?mismatches=1"}`; }}>Mismatches only</Quiet>
          <ol>
            {steps.map((step) => (
              <li key={step.step_id}>
                {step.started_at} {step.step_name} <Quiet onClick={() => setTool(tool === step.tool_id ? "" : step.tool_id)}>{step.tool_id}</Quiet> {step.chamber} dispatch {step.recipe_version} tool {step.recipe_rev}
                {step.recipe_mismatch ? <span> Mismatch. {step.flag}</span> : null}
                {step.ecn_conflict ? <span> The effective change {step.effective_ecn?.ecn_id} names {step.effective_ecn?.to_rev}.</span> : null}
              </li>
            ))}
          </ol>
          <details>
            <summary>All step columns</summary>
            <pre>{JSON.stringify(allSteps, null, 2)}</pre>
          </details>
          <AskPanel lineage={lineage} subject="lot" id={active} onUnauth={onUnauth} onStepUp={onStepUp} />
        </div>
      ) : null}
      <h2>Control chart</h2>
      {parameters.map((parameter) => (
        <Quiet key={parameter} pressed={parameter === paramFromHash} onClick={() => chartPath(parameter)}>{parameter}</Quiet>
      ))}
      {chart.loading && paramFromHash ? <p role="status">Loading the chart.</p> : null}
      {chart.error ? <p role="status">{chart.error}</p> : null}
      {chart.data?.unit_warning ? <p>{chart.data.unit_warning}</p> : null}
      {series.length ? <Chart data={chart.data} onPoint={setPoint} /> : null}
      {point ? <p>{point.sample_id}: measured {point.measured}. Spec {point.spec_low} to {point.spec_high}.</p> : null}
      {chart.data ? <RuleList data={chart.data} /> : null}
      {shown.length ? (
        <div>
          <table>
            <tbody>
              {shown.map((row) => (
                <tr key={row.sample_id}><td>{row.sample_id}</td><td>{row.measured}</td><td>{row.unit}</td></tr>
              ))}
            </tbody>
          </table>
          {series.length > 12 ? <Quiet onClick={() => setShowAll(!showAll)}>{showAll ? "Show the last 12" : "Show all"}</Quiet> : null}
        </div>
      ) : null}
    </div>
  );
}

function Chart({ data, onPoint }) {
  const rows = data.items || [];
  const values = rows.map((row) => Number(row.measured));
  const marks = [data.spec_low, data.spec_high, data.mean, ...values].map(Number).filter((value) => !Number.isNaN(value));
  const min = Math.min(...marks);
  const max = Math.max(...marks);
  const span = max - min || 1;
  const width = 560;
  const height = 220;
  const y = (value) => 20 + ((max - Number(value)) / span) * 180;
  const x = (index) => 30 + (index * (width - 50)) / Math.max(rows.length - 1, 1);
  const line = (value) => Number.isNaN(Number(value)) ? null : (
    <line x1="30" x2={width - 10} y1={y(value)} y2={y(value)} stroke="currentColor" />
  );
  return (
    <svg viewBox={`0 0 ${width} ${height}`} width="100%" role="img" aria-label={`${data.parameter} ${ (data.units || []).join(" ") }`}>
      <text x="30" y="16">{data.parameter} {(data.units || []).join(", ")}</text>
      {line(data.spec_low)}
      {line(data.spec_high)}
      {line(data.mean)}
      <text x="34" y={y(data.spec_low)}>Spec low</text>
      <text x="34" y={y(data.spec_high)}>Spec high</text>
      <text x="34" y={y(data.mean)}>Mean</text>
      <polyline fill="none" stroke="currentColor" points={rows.map((row, index) => `${x(index)},${y(row.measured)}`).join(" ")} />
      {rows.map((row, index) => {
        const outside = Number(row.measured) < Number(row.spec_low) || Number(row.measured) > Number(row.spec_high);
        return (
          <circle key={row.sample_id || index} cx={x(index)} cy={y(row.measured)} r="5" fill={outside ? "var(--accent)" : "var(--ink)"} role="button" tabIndex="0" onClick={() => onPoint(row)} onKeyDown={(event) => { if (event.key === "Enter") { onPoint(row); } }} />
        );
      })}
    </svg>
  );
}

function RuleList({ data }) {
  const rules = data.rules || {};
  const rows = data.items || [];
  return (
    <ul>
      {Object.entries(rules).map(([name, indexes]) => (indexes || []).map((index) => (
        <li key={`${name}-${index}`}>Rule {name.replace("rule_", "")} at point {index}, sample {rows[index]?.sample_id || index}.</li>
      )))}
    </ul>
  );
}
