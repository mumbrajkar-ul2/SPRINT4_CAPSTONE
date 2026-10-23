export const ROLES = [
  { id: "RT-01", label: "RT-01 Fab Exception Reviewer" },
  { id: "RT-02", label: "RT-02 Shift Lead" },
  { id: "RT-03", label: "RT-03 Process Engineer" },
  { id: "RT-04", label: "RT-04 Policy Owner" },
  { id: "RT-05", label: "RT-05 Operations Analyst" },
  { id: "RT-06", label: "RT-06 Operations Lead" },
];

let csrfToken = "";

export function setCsrf(value) {
  csrfToken = value || "";
}

export async function callApi(path, actor, options = {}) {
  const response = await fetch(path, {
    method: options.method || "GET",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(csrfToken ? { "X-CSRF-Token": csrfToken } : {}),
      ...(options.correlationId ? { "X-Correlation-Id": options.correlationId } : {}),
    },
    body: options.body ? JSON.stringify(options.body) : undefined,
  });
  const data = await response.json();
  return { status: response.status, data };
}

export async function callRaw(path) {
  return fetch(path, {
    method: "GET",
    credentials: "include",
    headers: csrfToken ? { "X-CSRF-Token": csrfToken } : {},
  });
}
