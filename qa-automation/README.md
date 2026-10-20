# Praxis acceptance evidence

Tracking: [GPTEINFRA-18273](https://issues.redhat.com/browse/GPTEINFRA-18273), [AgnosticV #28083](https://github.com/rhpds/agnosticv/pull/28083).

Run `healthcheck.yml` and `e2e.yml` in the provisioner's execution environment with the explicit dev cluster context and lab GUID. Override `praxis_test_model` if the per-order key uses a different model. These playbooks have not been run against a fresh order in this restoration work.

Health checks deployment availability, Route TLS and provisioned objects. The gateway TCP probe establishes listener readiness only; it does not establish model health. E2E checks the unauthenticated `/oauth/start` redirect, named Secret references and a real completion through the gateway from a running gateway pod. It never exports the backend key. A health response or OAuth redirect alone cannot pass inference acceptance.

The internal gateway check does not establish the authenticated browser path. Before promotion, record a fresh dev order and manually verify learner sign-in, UI completion and routing evidence, denied unauthorized access, failure behavior, a second tenant's isolation, cleanup and virtual-key revocation. Record source/catalog commits and image digests, not credentials or temporary access URLs. A 20–30 minute core walkthrough and optional modules up to 90 minutes must also be timed.

Keep health/E2E status in progress until the live evidence is accepted. The RHDP-owned migration repository is `rhpds/praxis-ai-gateway`, tracked by RHDPCD-2133. Publishing House owns generated AgnosticV and onboarding. Reviewer acceptance, full learner authentication/isolation and model capacity remain gates; Dallas is a separate dev environment.
