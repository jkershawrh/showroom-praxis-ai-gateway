# configure_praxis

Creates or removes the per-environment Praxis namespace and its runtime
configuration. The role expects `praxis_model_base_url`,
`praxis_model_api_key`, and `praxis_oauth_cookie_secret` during provisioning.

The backend credential is accepted only as an in-memory Ansible variable and is
written directly to an opaque OpenShift Secret with `no_log: true`.
