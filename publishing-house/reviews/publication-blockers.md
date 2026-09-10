# Publication prerequisites

These do not block local development or Publishing House intake, but must be
resolved before the catalog item is published:

1. Move or recreate this monorepo in the Publishing House-approved RHDP GitHub
   organization so AgnosticD, Argo CD, and Showroom can clone it.
2. Run `qa-automation/healthcheck.yml` and `qa-automation/e2e.yml` on an actual
   `ocpv09` allocation.

The application runtime may be described as running on Intel-backed `ocpv09`.
Do not claim that the remote MaaS model inference runs on Intel unless the MaaS
service publishes that guarantee separately.
