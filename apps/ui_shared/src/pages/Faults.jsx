import { useState } from "react";
import { AskPanel, go, PageHead, Quiet, useFetch } from "./kit.jsx";

const TITLES = {
  tool_drift: "Tool drift",
  outlier_wafer: "Outlier wafer",
  unqualified_supplier: "Unqualified supplier",
  lot_genealogy: "Lot genealogy",
};

export function Faults({ t, me, lineage, route, onUnauth, onStepUp }) {
  const data = useFetch("/api/scenarios/faults", onUnauth);
  const pending = useFetch("/api/approvals/pending?limit=1", onUnauth);
  const selected = route.parts[1] || "";
  const [more, setMore] = useState(false);
  if (data.loading) {
    return <p role="status">Loading the fault scenarios.</p>;
  }
  if (data.error) {
    return <p role="status">{data.error}</p>;
  }
  const detectors = data.data?.detectors || [];
  const open = detectors.find((row) => row.id === selected);
  const roles = me?.roles || [];
  return (
    <div>
      <PageHead kicker="Force Fab" title={t("page.faults.title")} sentence={t("page.faults.sentence")} />
      <p>
        {detectors.map((row) => (
          <Quiet key={row.id} onClick={() => go(`/faults/${row.id}`)}>{TITLES[row.id] || row.id} {(row.findings || []).length}</Quiet>
        ))}
      </p>
      <div className="ff-faults">
        {detectors.map((row) => (
          <article className="ff-card" key={row.id}>
            <h2>{TITLES[row.id] || row.id}</h2>
            <p>{(row.findings || []).length} findings.</p>
            <p>{row.recommended_action}</p>
            <p>{row.required_role}</p>
            {row.id === selected ? <Body row={row} more={more} setMore={setMore} roles={roles} pending={pending.data?.total || 0} lineage={lineage} onUnauth={onUnauth} onStepUp={onStepUp} /> : (
              <Quiet onClick={() => go(`/faults/${row.id}`)}>Open</Quiet>
            )}
          </article>
        ))}
      </div>
      {open ? null : null}
    </div>
  );
}

function Body({ row, more, setMore, roles, pending, lineage, onUnauth, onStepUp }) {
  const findings = row.findings || [];
  const shown = more ? findings : findings.slice(0, 8);
  const max = Math.max(1, ...findings.map((item) => Number(item.defects || 0)));
  return (
    <div>
      {row.id === "tool_drift" ? findings.map((item) => (
        <p key={item.chamber}>{item.chamber} {item.defects}<span className="ff-bar-track"><span className="ff-bar-fill" style={{ width: `${(Number(item.defects || 0) / max) * 100}%` }} /></span></p>
      )) : null}
      {shown.map((item, index) => (
        <p key={index}>
          {row.id === "outlier_wafer" ? `${item.sample_id || ""} measured ${item.measured} spec ${item.spec_low} to ${item.spec_high}` : null}
          {row.id === "unqualified_supplier" ? `${item.part_id || ""} ${item.qualification_state}` : null}
          {row.id === "lot_genealogy" ? `${item.lot_id} ${item.recipe_version} and ${item.recipe_rev} Differ` : null}
          {item.lot_id && item.parameter ? <Quiet onClick={() => go(`/lots/${encodeURIComponent(item.lot_id)}/spc/${encodeURIComponent(item.parameter)}`)}>Open chart</Quiet> : null}
          {item.lot_id && row.id === "lot_genealogy" ? <Quiet onClick={() => go(`/lots/${encodeURIComponent(item.lot_id)}?mismatches=1`)}>Open lot</Quiet> : null}
        </p>
      ))}
      {findings.length > 8 ? <Quiet onClick={() => setMore(!more)}>{more ? "Show fewer" : "Show the rest"}</Quiet> : null}
      {roles.includes(row.required_role) ? <p>Your role reviews this.</p> : <p>{row.required_role} reviews this.</p>}
      {pending > 0 ? <Quiet onClick={() => go("/approvals")}>Items waiting for your role.</Quiet> : null}
      <AskPanel lineage={lineage} subject="fault" id={row.id} onUnauth={onUnauth} onStepUp={onStepUp} />
    </div>
  );
}
