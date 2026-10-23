import { useState } from "react";
import { go, PageHead, Quiet, useFetch } from "./kit.jsx";

export function Glossary({ t, route, onUnauth }) {
  const [q, setQ] = useState(route.params.get("q") || "");
  const [offset, setOffset] = useState(Number(route.params.get("offset") || 0));
  const system = route.params.get("system") || "";
  const query = new URLSearchParams();
  if (route.params.get("q")) {
    query.set("q", route.params.get("q"));
  }
  query.set("limit", "200");
  query.set("offset", String(offset));
  const data = useFetch(`/api/semantic/terms?${query.toString()}`, onUnauth);
  const rows = data.data?.items || [];
  const systems = [...new Set(rows.map((row) => row.local_system).filter(Boolean))];
  const grouped = new Map();
  rows.filter((row) => !system || row.local_system === system).forEach((row) => {
    const card = grouped.get(row.term_id) || { ...row, locals: [] };
    card.locals.push(`${row.local_system || ""} — ${row.local_name || ""}`);
    grouped.set(row.term_id, card);
  });
  const cards = [...grouped.values()];

  function search(event) {
    event.preventDefault();
    const params = new URLSearchParams();
    if (q) {
      params.set("q", q);
    }
    if (system) {
      params.set("system", system);
    }
    go(`/glossary?${params.toString()}`);
    setOffset(0);
  }

  return (
    <div>
      <PageHead kicker="Force Fab" title={t("page.glossary.title")} sentence={t("page.glossary.sentence")} />
      <form onSubmit={search} className="ff-filters">
        <label>
          Search
          <input placeholder="open, recipe, hold" value={q} onChange={(event) => setQ(event.target.value)} />
        </label>
        <label>
          System
          <select value={system} onChange={(event) => go(`/glossary?q=${encodeURIComponent(route.params.get("q") || "")}&system=${encodeURIComponent(event.target.value)}`)}>
            <option value="">All systems</option>
            {systems.map((name) => <option key={name} value={name}>{name}</option>)}
          </select>
        </label>
        <button type="submit" className="primary">{t("btn.search")}</button>
        <Quiet onClick={() => { setQ(""); go("/glossary"); }}>{t("btn.clear")}</Quiet>
      </form>
      {data.loading ? <p role="status">Loading the glossary.</p> : null}
      {data.error ? <p role="status">{data.error}</p> : null}
      <p>{data.data && data.data.total > 200 ? `Showing ${offset + 1}–${Math.min(offset + rows.length, data.data.total)} of ${data.data.total}.` : `${cards.length} terms.`}</p>
      {cards.map((card) => (
        <article className="ff-card" key={card.term_id}>
          <h2>{card.canonical_name}</h2>
          <p>{card.definition}</p>
          {card.locals.map((line) => <p key={line}>{line}</p>)}
          {card.maps_to_term ? <p>Maps to {card.maps_to_term}</p> : null}
          <Quiet onClick={() => go(`/graph/${encodeURIComponent(card.term_id)}`)}>Open on the graph</Quiet>
          <Quiet onClick={async (event) => {
            try {
              await navigator.clipboard.writeText(card.canonical_name);
            } catch {
              const node = event.currentTarget;
              const range = document.createRange();
              range.selectNodeContents(node.parentElement.querySelector("h2"));
              const selection = window.getSelection();
              selection.removeAllRanges();
              selection.addRange(range);
            }
          }}>Copy the name</Quiet>
        </article>
      ))}
      {data.data && data.data.total > 200 ? (
        <p>
          <Quiet disabled={offset <= 0} onClick={() => setOffset(Math.max(0, offset - 200))}>Previous</Quiet>
          <Quiet disabled={offset + 200 >= data.data.total} onClick={() => setOffset(offset + 200)}>Next</Quiet>
        </p>
      ) : null}
    </div>
  );
}
