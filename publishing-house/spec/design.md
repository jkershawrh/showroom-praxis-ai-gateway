# Praxis AI Gateway lab design

This is one progressive lab with three tracks, not three independent labs. The
private quickstart repository remains the engineering reference. Publishing
House owns the deployable Showroom, Ansible, GitOps, health-check, and E2E
artifacts in this repository.

## Runtime boundary

The Praxis gateway and learner UI run on Red Hat OpenShift provisioned from the
`ocpv09` CNV pool. RHDP MaaS is consumed only through its OpenAI-compatible API.
The lab therefore claims Intel infrastructure for its OpenShift application
runtime, but makes no claim about the hardware behind the remote MaaS endpoint.

## Secret flow

1. RHDP provisions a `MaaSSandbox` containing an API base URL, virtual key, and
   allowed model list.
2. The custom `configure_praxis` role writes the endpoint to a ConfigMap and the
   key to `model-backend-credentials` in the application namespace.
3. GitOps deploys workloads that reference the existing ConfigMap and Secret.
4. Showroom receives the authenticated UI URL, never the virtual key.
5. The custom role removes the application namespace, while RHDP destroys the
   MaaSSandbox and its virtual key through the sandbox lifecycle.

## Image publication

Images are AMD64-compatible and pinned by digest. The learner UI is published as
`quay.io/redhat-gpte/praxis-ai-gateway-ui@sha256:e67615e04af243e2f06d7450f2a1b776c4ac07ebd75c1250a7b7f1f36d694e53`.
