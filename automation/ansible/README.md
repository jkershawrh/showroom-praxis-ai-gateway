# `praxis_ai_gateway.automation`

Publishing House lifecycle automation for the Praxis AI Gateway lab. The
`configure_praxis` role consumes an RHDP MaaSSandbox credential and creates the
namespace, Praxis configuration, model credential Secret, and OAuth cookie
Secret required by the GitOps deployment.

The role marks all credential-bearing tasks `no_log` and does not emit the MaaS
key through `agnosticd_user_info` or Showroom user data.
