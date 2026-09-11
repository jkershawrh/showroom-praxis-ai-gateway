# Publication prerequisites

These do not block local development or Publishing House intake, but must be
resolved before the catalog item is published:

1. Move or recreate this monorepo in the Publishing House-approved RHDP GitHub
   organization so AgnosticD, Argo CD, and Showroom can clone it.
2. Run `qa-automation/healthcheck.yml` and `qa-automation/e2e.yml` on an
   allocation selected from the registered `ai-qs-praxis` shared
   cluster.

This integration CI selects the shared cluster by logical Sandbox API labels; it
does not pin a physical CNV pool. Do not infer anything about the hardware behind
the remote MaaS endpoint from the OpenShift cluster selection.
