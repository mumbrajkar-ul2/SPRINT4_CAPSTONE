import { useEffect, useRef, useState } from "react";
import { callApi } from "../api.js";
import { go, PageHead, Quiet } from "./kit.jsx";

const WORDS = {
  dispose: "Dispose",
  approve_agent: "Approve the agent",
  recipe_hold_or_release: "Hold or release",
  policy_pick: "Policy pick",
  replay_confirm: "Replay confirm",
  assign_owner: "Assign an owner",
};

const TABS = ["Replay", "Recipe", "Clocks", "Policy", "Outage", "Rule trace", "Compare"];

export function Approvals({ t, me, onUnauth, onStepUp }) {
  const [list, setList] = useState(null);
  const [error, setError] = useState("");
  const [openId, setOpenId] = useState("");
  const [detail, setDetail] = useState(null);
  const [detailNote, setDetailNote] = useState("");
  const [sign, setSign] = useState(false);
  const [reason, setReason] = useState("");
  const [choice, setChoice] = useState("");
  const [extra, setExtra] = useState("");
  const [status, setStatus] = useState("");
  const [signedCase, setSignedCase] = useState("");
  const signRef = useRef(null);
  const openRef = useRef(null);

  async function load() {
    const response = await callApi("/api/approvals/pending?limit=200", {});
    if (response.status === 401) {
      onUnauth();
      return;
    }
    if (response.status >= 400) {
      setError(response.data?.message || "The request failed.");
      return;
    }
    setList(response.data);
  }

  useEffect(() => {
    load();
  }, []);

  useEffect(() => {
    if (!sign || !signRef.current) {
      return undefined;
    }
    const root = signRef.current;
    const focusable = [...root.querySelectorAll("button, input, a")];
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    first?.focus();
    function trap(event) {
      if (event.key !== "Tab" || !focusable.length) {
        return;
      }
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
    root.addEventListener("keydown", trap);
    return () => root.removeEventListener("keydown", trap);
  }, [sign, openId]);

  useEffect(() => {
    if (!openId) {
      return;
    }
    let live = true;
    callApi(`/api/cases/${encodeURIComponent(openId)}/detail`, {}).then((response) => {
      if (!live) {
        return;
      }
      if (response.status === 404) {
        setDetail(null);
        setDetailNote("This waiting item is not a row in the legacy case table.");
        return;
      }
      if (response.status >= 400) {
        setDetailNote(response.data?.message || "The case did not load.");
        return;
      }
      setDetail(response.data);
      setDetailNote("");
    });
    return () => {
      live = false;
    };
  }, [openId]);

  const items = list?.items || [];
  const groups = {};
  items.forEach((item) => {
    const key = item.action_type || "other";
    groups[key] = groups[key] || [];
    groups[key].push(item);
  });
  const open = items.find((item) => item.case_id === openId);

  function choices(action) {
    if (action === "recipe_hold_or_release") {
      return [["hold", "Hold"], ["release", "Release"]];
    }
    if (action === "replay_confirm") {
      return [["drop_duplicate", "Drop duplicate"]];
    }
    if (action === "policy_pick") {
      return [["keep_wait", "Keep waiting"], ["pick", "Use this policy id"]];
    }
    if (action === "assign_owner") {
      return [["assign", "Assign this owner"]];
    }
    return [["dispose", "Dispose"]];
  }

  async function submit() {
    if (!open || !reason.trim()) {
      setStatus("A reason is required.");
      return;
    }
    const action = open.action_type;
    const decision = choice || choices(action)[0][0];
    if (action === "assign_owner" && !extra.trim()) {
      setStatus("An owner id is required.");
      return;
    }
    if (action === "policy_pick" && decision === "pick" && !extra.trim()) {
      setStatus("A policy id is required.");
      return;
    }
    const meaning = decision === "release" ? "release" : decision === "dispose" ? "dispose" : decision === "keep_wait" ? "reject" : "approve";
    const body = {
      case_id: open.case_id,
      action_type: action,
      proposed_by: open.proposed_by || "model_draft",
      decision,
      signature: { meaning, reason: reason.trim() },
    };
    if (action === "assign_owner") {
      body.owner_id = extra.trim();
    }
    if (action === "policy_pick" && decision === "pick") {
      body.policy_id = extra.trim();
    }
    const response = await callApi("/api/approvals", {}, { method: "POST", body });
    if (response.status === 401 && response.data?.error_class === "step_up_required") {
      setStatus(response.data.message || "Sign in again with a one-time code.");
      onStepUp();
      return;
    }
    if (response.status >= 400 || response.data?.ok === false) {
      setStatus(response.data?.message || "The signature was not stored.");
      return;
    }
    setSign(false);
    setSignedCase(open.case_id);
    setStatus(`${open.case_id} signed as ${decision}.`);
    setOpenId("");
    await load();
  }

  return (
    <div>
      <PageHead kicker="Force Fab" title={t("page.approvals.title")} sentence={t("page.approvals.sentence")} />
      {list ? <p>{list.total === 1 ? "1 item" : `${list.total} items`} waiting for {(me?.roles || []).join(", ") || "your role"}.</p> : <p role="status">Loading the approvals.</p>}
      {error ? <p role="status">{error}</p> : null}
      {list && list.total === 0 ? <p>Nothing is waiting for your role on these sites. <Quiet onClick={() => go("/cases")}>Cases</Quiet></p> : null}
      {status ? (
        <p role="status">
          {status} {signedCase ? <Quiet onClick={() => go(`/audit?case=${encodeURIComponent(signedCase)}`)}>Show this write in Audit</Quiet> : null}
        </p>
      ) : null}
      {Object.entries(groups).map(([action, rows]) => (
        <section key={action}>
          <h2>{WORDS[action] || action}</h2>
          {rows.map((item) => (
            <article className="ff-card" key={item.case_id}>
              <p>{item.case_id}. Proposed by {item.proposed_by}. {item.site || item.severity || ""}</p>
              {openId !== item.case_id ? (
                <Quiet onClick={() => { setOpenId(item.case_id); setChoice(""); setSign(false); }} >Review</Quiet>
              ) : (
                <div>
                  {detailNote ? <p>{detailNote}</p> : null}
                  {detail?.case ? (
                    <div>
                      <p>{detail.case.status}. {detail.case.severity}</p>
                      {(detail.timeline || []).slice(-3).map((row, index) => <p key={index}>{row.recorded_at} {row.event_type || row.note}</p>)}
                      <Quiet onClick={() => go(`/cases/${encodeURIComponent(item.case_id)}`)}>Open the full case</Quiet>
                    </div>
                  ) : null}
                  <p>{item.status} {item.severity} {item.rank} {item.scenario}</p>
                  {TABS.includes(item.scenario) ? <Quiet onClick={() => go(`/scenarios/${encodeURIComponent(item.scenario)}`)}>{item.scenario}</Quiet> : null}
                  {sign ? (
                    <div className="sign-dialog" role="dialog" aria-label="Sign" ref={signRef}>
                      <p>I am signing as {me?.name}.</p>
                      {choices(action).map(([value, label]) => (
                        <label key={value}><input type="radio" name="decision" checked={(choice || choices(action)[0][0]) === value} onChange={() => setChoice(value)} /> {label}</label>
                      ))}
                      {action === "assign_owner" || (action === "policy_pick" && (choice || "keep_wait") === "pick") ? (
                        <input aria-label={action === "assign_owner" ? "Owner id" : "Policy id"} value={extra} onChange={(event) => setExtra(event.target.value)} />
                      ) : null}
                      <label>Reason <input value={reason} onChange={(event) => setReason(event.target.value)} /></label>
                      <button type="button" className="primary" onClick={submit}>{t("btn.sign")}</button>
                      <Quiet onClick={() => { setSign(false); openRef.current?.focus(); }}>Cancel</Quiet>
                    </div>
                  ) : (
                    <button type="button" className="primary" ref={openRef} onClick={() => setSign(true)}>{t("btn.sign")}</button>
                  )}
                </div>
              )}
            </article>
          ))}
        </section>
      ))}
    </div>
  );
}
