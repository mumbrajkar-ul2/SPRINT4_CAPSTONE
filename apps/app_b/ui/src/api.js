export const ROLES = [
  { id: "RT-01", label: "RT-01 Fab Exception Reviewer" },
  { id: "RT-02", label: "RT-02 Shift Lead" },
  { id: "RT-03", label: "RT-03 Process Engineer" },
  { id: "RT-04", label: "RT-04 Policy Owner" },
  { id: "RT-05", label: "RT-05 Operations Analyst" },
  { id: "RT-06", label: "RT-06 Operations Lead" },
];

export function headers(actor) {
  return {
    "Content-Type": "application/json",
    "X-Api-Key": actor.apiKey || "local-demo-only",
    "X-Actor-Id": actor.actorId,
    "X-Actor-Role": actor.role,
  };
}

export async function callApi(path, actor, options = {}) {
  const response = await fetch(path, {
    method: options.method || "GET",
    headers: headers(actor),
    body: options.body ? JSON.stringify(options.body) : undefined,
  });
  const data = await response.json();
  return { status: response.status, data };
}
