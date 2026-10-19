# Image digest and demo key file

| Field | Value |
|---|---|
| Stage | Phase 18 / DEV-016. |
| Date / version | 2026-10-19, v1.0 |
| Author / agent | Executor agent (Grok 4.7), correlation id corr-p18b-doc-20261019-001 |
| Status | CLOSED on the digest and the file path. |
| Evidence sources | `Dockerfile.platform`; `secrets/demo-api-key.txt` |
| Assumptions | Compose still passes `FABPULSE_API_KEY` into the process. The gitignored file is the local copy of that demo key. |
| Unresolved issues | A company signing service was not named. A company vault was not named. |
| Residual risks | This digest is the sha256 of the Dockerfile that installs Node and builds the React screens. It is not a registry signature. |

The sha256 of `Dockerfile.platform` is `303065d4735d4d2fd6da888e05069200ffcee92bb0a1b4265ebfea213a2ce0d3`.

That file installs Node and runs `npm run build` for Application A and Application B. That is the Phase 17 image build definition.

The demo API key is read from `secrets/demo-api-key.txt`. That path is listed in `.gitignore`. The file contains the documented local demo key. A company signing service and a company vault stay unnamed.
