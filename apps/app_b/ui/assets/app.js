function headers() {
  const key = document.getElementById("apiKey").value.trim();
  const [actor, role] = document.getElementById("actor").value.split("|");
  return {
    "X-Api-Key": key,
    "X-Actor-Id": actor,
    "X-Actor-Role": role,
    "X-Correlation-Id": "corr-ui-b-" + Date.now(),
    "Content-Type": "application/json",
  };
}

function show(id) {
  document.querySelectorAll(".panel").forEach((el) => el.classList.add("hidden"));
  document.getElementById(id).classList.remove("hidden");
}

async function call(path, options) {
  const response = await fetch(path, options);
  const text = await response.text();
  let body;
  try { body = JSON.parse(text); } catch { body = { raw: text }; }
  return { status: response.status, body };
}

document.querySelectorAll("nav button").forEach((btn) => {
  btn.addEventListener("click", () => show(btn.getAttribute("data-panel")));
});

document.getElementById("loadQueue").addEventListener("click", async () => {
  const result = await call("/api/queue", { headers: headers() });
  document.getElementById("queueOut").textContent = JSON.stringify(result, null, 2);
});

document.getElementById("loadCase").addEventListener("click", async () => {
  const id = document.getElementById("caseId").value.trim();
  const result = await call("/api/cases/" + encodeURIComponent(id), { headers: headers() });
  document.getElementById("caseOut").textContent = JSON.stringify(result, null, 2);
});

async function runQuestion(question) {
  const caseId = document.getElementById("caseId").value.trim();
  const result = await call("/api/query", {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({
      question,
      case_id: caseId,
      job: document.getElementById("job").value,
    }),
  });
  const banner = document.getElementById("abstainBanner");
  if (result.body && result.body.verdict === "ABSTAIN") banner.classList.remove("hidden");
  else banner.classList.add("hidden");
  document.getElementById("queryOut").textContent = JSON.stringify(result, null, 2);
}

document.getElementById("runQuery").addEventListener("click", async () => {
  await runQuestion(document.getElementById("question").value);
});

document.getElementById("askUngrounded").addEventListener("click", async () => {
  document.getElementById("question").value = "What is the recipe_release limit for sales region MOON on 2099-01-01";
  await runQuestion(document.getElementById("question").value);
});

document.getElementById("loadRecovery").addEventListener("click", async () => {
  const result = await call("/api/recovery", { headers: headers() });
  document.getElementById("recoveryOut").textContent = JSON.stringify(result, null, 2);
});

document.querySelectorAll("#recovery button[data-mode]").forEach((btn) => {
  btn.addEventListener("click", async () => {
    const mode = btn.getAttribute("data-mode");
    const probe = await call("/api/recovery/probe?mode=" + mode, { headers: headers() });
    const status = await call("/api/recovery", { headers: headers() });
    document.getElementById("recoveryOut").textContent = JSON.stringify({ probe, status }, null, 2);
  });
});

document.getElementById("postApproval").addEventListener("click", async () => {
  const result = await call("/api/approvals", {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({
      case_id: document.getElementById("apCase").value.trim(),
      action_type: document.getElementById("apAction").value,
      decision: document.getElementById("apDecision").value.trim(),
      proposed_by: document.getElementById("apProposed").value.trim(),
      owner_id: document.getElementById("apOwner").value.trim() || null,
      policy_id: document.getElementById("apPolicy").value.trim() || null,
    }),
  });
  document.getElementById("approvalOut").textContent = JSON.stringify(result, null, 2);
});

document.getElementById("loadLineage").addEventListener("click", async () => {
  const id = document.getElementById("lineageId").value.trim();
  const result = await call("/api/lineage/" + encodeURIComponent(id), { headers: headers() });
  const phase = document.getElementById("phase10Id");
  if (result.body && result.body.phase10_correlation_id) {
    phase.textContent = "Phase 10 correlation id: " + result.body.phase10_correlation_id;
  } else {
    phase.textContent = "";
  }
  document.getElementById("lineageOut").textContent = JSON.stringify(result, null, 2);
});
