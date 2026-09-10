# Publication prerequisites

These do not block local development or Publishing House intake, but must be
resolved before the catalog item is published:

1. Move or recreate this monorepo in the Publishing House-approved RHDP GitHub
   organization so AgnosticD, Argo CD, and Showroom can clone it.
2. Run `qa-automation/healthcheck.yml` and `qa-automation/e2e.yml` on the
   integration allocation created from the generic
   `agd-v2/ocp-cluster-cnv-pools` component.

This integration CI intentionally does not pin a physical CNV pool. Do not make
hardware-specific claims for either the application runtime or remote MaaS
inference based on this CI.
