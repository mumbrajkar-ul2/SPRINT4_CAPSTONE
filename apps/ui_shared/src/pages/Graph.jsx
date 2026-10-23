import { useEffect, useState } from "react";
import { go, PageHead, Quiet, shortLabel, useFetch } from "./kit.jsx";

const KINDS = {
  architecture: "architecture",
  business_rule: "business rule",
  code_intelligence: "code intelligence",
  data_relationship: "data relationship",
  decision: "decision",
  dependency: "dependency",
  domain_knowledge: "domain knowledge",
};
const TYPES = ["maps_to", "implements", "conflicts_with", "supersedes", "governs", "evidenced_by", "depends_on", "tested_by"];

export function GraphPage({ t, route, onUnauth }) {
  const initial = route.parts[1] ? decodeURIComponent(route.parts[1]) : "";
  const [text, setText] = useState(initial);
  const [trail, setTrail] = useState(initial ? [initial] : []);
  const [type, setType] = useState("");
  const [nextHop, setNextHop] = useState(false);
  const [focus, setFocus] = useState(null);
  useEffect(() => {
    setText(initial);
  }, [initial]);
  const suggestions = useFetch("/api/graph", onUnauth);
  const graph = useFetch(initial ? `/api/graph/${encodeURIComponent(initial)}` : "", onUnauth);

  function load(id, push) {
    const encoded = encodeURIComponent(id);
    if (push) {
      setTrail((current) => [...current, id]);
    }
    setNextHop(false);
    setFocus(null);
    go(`/graph/${encoded}`);
    setText(id);
  }

  const nodes = graph.data?.nodes || [];
  const edges = graph.data?.edges || [];
  const limited = nextHop ? nodes : nodes.filter((node) => node.hop <= 1);
  const seed = limited.find((node) => node.hop === 0);
  const near = limited.filter((node) => node.hop === 1).slice(0, 12);
  const outer = nextHop ? limited.filter((node) => node.hop === 2) : [];
  const pool = [seed, ...near, ...outer].filter(Boolean);
  const poolIds = new Set(pool.map((node) => node.id));
  const typed = (type ? edges.filter((edge) => edge.type === type) : edges).filter((edge) => poolIds.has(edge.from_id) && poolIds.has(edge.to_id));
  const keep = new Set(seed ? [seed.id] : []);
  let grew = true;
  while (grew) {
    grew = false;
    typed.forEach((edge) => {
      if (keep.has(edge.from_id) && poolIds.has(edge.to_id) && !keep.has(edge.to_id)) {
        keep.add(edge.to_id);
        grew = true;
      }
      if (keep.has(edge.to_id) && poolIds.has(edge.from_id) && !keep.has(edge.from_id)) {
        keep.add(edge.from_id);
        grew = true;
      }
    });
  }
  const drawnNodes = pool.filter((node) => keep.has(node.id));
  const drawnEdges = typed.filter((edge) => keep.has(edge.from_id) && keep.has(edge.to_id));
  const placed = place(drawnNodes);

  return (
    <div>
      <PageHead kicker="Force Fab" title={t("page.graph.title")} sentence={t("page.graph.sentence")} />
      <form className="ff-filters" onSubmit={(event) => { event.preventDefault(); load(text.trim(), true); }}>
        <label>Item id<input value={text} onChange={(event) => setText(event.target.value)} /></label>
        <button type="submit" className="primary">{t("btn.show_graph")}</button>
        <Quiet onClick={() => { const previous = trail[trail.length - 2]; if (previous) { setTrail(trail.slice(0, -1)); load(previous, false); } }}>{t("btn.back")}</Quiet>
      </form>
      <p>{trail.map((id) => <Quiet key={id} onClick={() => load(id, false)}>{id}</Quiet>)}</p>
      <p>Suggested items</p>
      {(suggestions.data?.items || []).map((item) => (
        <Quiet key={item.id} pressed={item.id === initial} onClick={() => load(item.id, true)}>{item.id}</Quiet>
      ))}
      <p>
        <Quiet pressed={!type} onClick={() => setType("")}>{t("link.all")}</Quiet>
        {TYPES.map((name) => <Quiet key={name} pressed={type === name} onClick={() => setType(name)}>{t(`link.${name}`)}</Quiet>)}
      </p>
      {graph.loading && initial ? <p role="status">Loading the graph.</p> : null}
      {graph.error ? <p role="status">{graph.error}</p> : null}
      <div className="ff-graph" style={{ minHeight: Math.max(near.length, outer.length) > 8 ? 720 : 420 }}>
        <svg viewBox={viewBoxFor(placed)} width="100%" role="img" aria-label="Knowledge graph">
          {drawnEdges.map((edge, index) => {
            const from = placed.find((node) => node.id === edge.from_id);
            const to = placed.find((node) => node.id === edge.to_id);
            if (!from || !to) {
              return null;
            }
            return <line key={index} x1={from.x} y1={from.y} x2={to.x} y2={to.y} stroke="var(--line)" tabIndex="0" onFocus={() => setFocus({ edge })}><title>{edge.from_id} {t(`link.${edge.type}`)} {edge.to_id}</title></line>;
          })}
          {placed.map((node) => (
            <g key={node.id} tabIndex="0" role="button" onClick={() => load(node.id, true)} onFocus={() => setFocus({ node })} onMouseEnter={() => setFocus({ node })}>
              <circle cx={node.x} cy={node.y} r="16" fill={node.id === initial ? "var(--accent)" : "#2a343e"} stroke="var(--line)" />
              <text x={node.x + 20} y={node.y} fill="var(--ink)">{KINDS[node.kind] || node.kind} {shortLabel(node.statement)}</text>
            </g>
          ))}
        </svg>
      </div>
      {!nextHop && nodes.some((node) => node.hop === 2) ? <Quiet onClick={() => setNextHop(true)}>Show the next hop</Quiet> : null}
      <p>{focus?.node ? focus.node.statement : focus?.edge ? `${focus.edge.from_id} ${t(`link.${focus.edge.type}`)} ${focus.edge.to_id}.` : drawnNodes[0]?.statement}</p>
      <table>
        <tbody>
          {drawnEdges.map((edge, index) => (
            <tr key={index}>
              <td><Quiet onClick={() => load(edge.from_id, true)}>{edge.from_id}</Quiet></td>
              <td>{t(`link.${edge.type}`) || edge.type}</td>
              <td><Quiet onClick={() => load(edge.to_id, true)}>{edge.to_id}</Quiet></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const LABEL_GAP = 18;

function place(nodes) {
  const seed = nodes.find((node) => node.hop === 0) || nodes[0];
  if (!seed) {
    return [];
  }
  const rest = nodes.filter((node) => node !== seed);
  const inner = rest.filter((node) => node.hop <= 1);
  const outer = rest.filter((node) => node.hop > 1);
  const out = [{ ...seed, x: 300, y: 210 }];
  ring(inner, 120, out);
  ring(outer, 200, out);
  spreadBaselines(out, LABEL_GAP);
  return out;
}

function spreadBaselines(nodes, gap) {
  const ordered = [...nodes].sort((a, b) => a.y - b.y || String(a.id).localeCompare(String(b.id)));
  for (let index = 1; index < ordered.length; index += 1) {
    const floor = ordered[index - 1].y + gap;
    if (ordered[index].y < floor) {
      ordered[index].y = floor;
    }
  }
}

function viewBoxFor(nodes) {
  if (!nodes.length) {
    return "0 0 640 420";
  }
  const minX = Math.min(...nodes.map((node) => node.x)) - 36;
  const maxX = Math.max(...nodes.map((node) => node.x)) + 220;
  const minY = Math.min(...nodes.map((node) => node.y)) - 24;
  const maxY = Math.max(...nodes.map((node) => node.y)) + 24;
  return `${minX} ${minY} ${Math.max(640, maxX - minX)} ${Math.max(420, maxY - minY)}`;
}

function ring(nodes, radius, out) {
  nodes.forEach((node, index) => {
    const angle = (Math.PI * 2 * index) / Math.max(nodes.length, 1);
    out.push({ ...node, x: 300 + radius * Math.cos(angle), y: 210 + radius * Math.sin(angle) });
  });
}
