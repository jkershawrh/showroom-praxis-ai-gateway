# Solution architect presenter guide

## Purpose

This guide supports a 20–30 minute customer-facing Praxis demonstration with
optional operations and governance depth. The goal is to help customer
application, platform, and security stakeholders decide whether a governed AI
gateway pattern merits a bounded proof of concept.

The presenter demonstrates a live capability and its evidence. Do not spend
the opening session installing infrastructure, running repository tests, or
describing preview functionality as implemented.

## Key messages

1. Applications can use one stable interface while platform teams control
   model endpoints and upstream credentials.
2. Red Hat OpenShift supplies the identity, Secret, networking, lifecycle, and
   operational boundary around the upstream Praxis gateway.
3. MaaS is replaceable lab model access, not the recommended production
   architecture or a Praxis dependency.
4. Exact-request evidence is more defensible than an unrelated latest-event
   view.
5. Authorization, sensitive-data policy, and durable audit evidence require
   explicit customer designs beyond a gateway deployment.

## Audience

- customer application architect or development lead;
- AI platform or cloud platform owner;
- security, risk, or governance architect;
- operations or observability lead; and
- Red Hat solution architect facilitating the discussion.

## Presenter preflight

Complete these checks 20–30 minutes before the session:

1. Confirm the RHDP service reports ready and sufficient lifetime remains.
2. Open Instructions, App UI, Terminal, and OpenShift Console in separate tabs.
3. Verify the App UI redirects through OpenShift OAuth and loads successfully.
4. Submit one neutral prompt and retain its status, model, elapsed time, and
   trace ID.
5. Confirm `oc project -q` returns the assigned namespace.
6. Confirm `praxis-ai` and `praxis-ui` Deployments are available.
7. Confirm the model credential is a Secret reference without reading it.
8. If demonstrating failure, save the current NetworkPolicy and verify there
   is enough time to restore and retest.
9. Keep screenshots or a clearly identified previously captured result as a
   fallback. Never describe fallback evidence as a live request.

Stop rather than improvise if the assigned namespace is wrong, the App UI is
not OAuth protected, or the baseline request fails repeatedly.

## Discovery prompts

Use two or three questions, not the entire list:

- How many model providers and model endpoints do application teams use today?
- Where are provider credentials stored and rotated?
- What application changes are required when a provider or model changes?
- Which identities need model, route, or tool authorization?
- What model-access evidence must operations, security, or audit teams retain?
- Which data classes may reach an external model endpoint?
- What should happen when a model, policy service, or evidence service fails?

Select optional modules from the answers.

## Default 25-minute storyboard

| Time | Screen | Presenter action | Proof statement |
| ---: | --- | --- | --- |
| 0–3 | Instructions | State the endpoint, credential, and provider-coupling problem | The customer problem comes before the technology |
| 3–8 | App UI | Submit one neutral request and narrate the topology | The application sees Praxis, not the provider credential |
| 8–12 | Terminal | Inspect the Secret reference and Routes | OpenShift owns credential and exposure boundaries |
| 12–17 | Terminal | Invoke the same Praxis API contract with `curl` | Another client uses the same stable northbound contract |
| 17–21 | App UI | Submit a second request and compare trace IDs | Evidence remains attached to the exact request |
| 21–25 | Instructions | Map customer gaps and select one next proof | The session ends with an architecture decision |

## Optional depth

### Operations

Use request correlation when the customer asks about observability. Use the
controlled NetworkPolicy fault only for a prepared technical audience and an
isolated namespace. Explain that gateway readiness, backend reachability, and
model-request success are different signals.

### Governance

Inspect RBAC, NetworkPolicy, and Secret references. Use the architecture map to
discuss application identity, workload identity, tenant authorization,
sensitive-data handling, retention, and evidence.

The PPE-to-OCSF immutable-ledger path is preview material. The current
reference adapter validates fixtures; the pinned Praxis build does not natively
emit live PPE decisions into that path.

## Objection handling

**Is Praxis a supported Red Hat product?**

No. Praxis is an upstream project demonstrated on Red Hat OpenShift. The lab
shows an architecture pattern and OpenShift platform responsibilities.

**Is MaaS the proposed production backend?**

No. MaaS supplies model access for the shared lab. Red Hat OpenShift AI or
another compatible endpoint can satisfy the same backend boundary after
qualification.

**Does the gateway make the application compliant?**

No. It creates a useful control point. Compliance depends on customer-specific
identity, policy, data handling, retention, evidence, and operating processes.

**Does the trace ID prove every network hop?**

No. This release proves exact-request correlation. Full distributed tracing
requires a tested telemetry pipeline.

**Can every provider be swapped transparently?**

No. The stable OpenAI-compatible contract reduces coupling, but provider
extensions and model behavior require qualification.

## Recovery guidance

| Symptom | Presenter response |
| --- | --- |
| App UI redirects repeatedly | Reopen it from Showroom and verify OAuth; do not expose Praxis directly |
| Initial model request is slow | Wait once for the bounded request; avoid repeated retries |
| Port-forward command reports the port in use | Stop the previous port-forward or choose another local port |
| Optional fault does not recover | Restore `/tmp/praxis-egress-before.yaml`; verify NetworkPolicy before continuing |
| Model backend remains unavailable | Show previously captured evidence, label it as fallback, and continue the architecture discussion |
| Console access fails | Continue with the namespace-scoped Terminal and record Console access as a follow-up |

## Close

End with three statements:

1. The session demonstrated a stable application boundary and platform-owned
   upstream credential on OpenShift.
2. Operations and governance capabilities must be selected and proven against
   the customer's identities, data, model endpoints, and evidence systems.
3. The recommended next step is one bounded proof with agreed success evidence,
   not a broad production claim.
