# Praxis AI Gateway lab design

This is one progressive lab with three tracks, not three independent labs. The
private quickstart repository remains the engineering reference. Publishing
House owns the deployable Showroom, Ansible, GitOps, health-check, and E2E
artifacts in this repository.

## Runtime boundary

The Praxis gateway and learner UI run as a tenant on the registered Intel
Inference integration cluster selected by `cloud: cnv-dedicated-shared` and
`lab: ai-lab-xeon6-inference`. The CI does not provision or physically pin a
cluster. RHDP MaaS is consumed only through its OpenAI-compatible API, and the
lab makes no claim about the hardware behind that remote endpoint.

## Secret flow

1. The RHDP LiteMaaS workload creates a per-order virtual key for the selected
   model and exposes `litellm_api_endpoint` and `litellm_virtual_key` to the
   remaining deployment workloads.
2. The custom `configure_praxis` role writes the endpoint to a ConfigMap and the
   key to `model-backend-credentials` in the application namespace.
3. GitOps deploys workloads that reference the existing ConfigMap and Secret.
4. Showroom receives the authenticated UI URL, never the virtual key.
5. The custom role removes the application namespace, then the LiteMaaS
   workload revokes the virtual key during the remove-workload lifecycle.

## Image publication

Images are AMD64-compatible and pinned by digest. The learner UI is published as
`quay.io/redhat-gpte/praxis-ai-gateway-ui@sha256:e67615e04af243e2f06d7450f2a1b776c4ac07ebd75c1250a7b7f1f36d694e53`.
