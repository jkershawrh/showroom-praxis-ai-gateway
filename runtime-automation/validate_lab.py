"""Static preflight for the generated Praxis Showroom lab."""

import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "content/modules/ROOT/pages"
MODULES = sorted(PAGES.glob("0[2-7]-*.adoc"))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


require((ROOT / "default-site.yml").is_file(), "default-site.yml is missing")
require((ROOT / "ui-config.yml").is_file(), "ui-config.yml is missing")
require((ROOT / "content/antora.yml").is_file(), "antora.yml is missing")
require((ROOT / "content/supplemental-ui").is_dir(), "supplemental UI is missing")
require(len(MODULES) >= 5, "at least five hands-on modules are required")
for required in [
    "publishing-house/spec.yaml",
    "publishing-house/spec/automation-manifest.yaml",
    "automation/ansible/galaxy.yml",
    "automation/ansible/roles/configure_praxis/tasks/main.yml",
    "automation/gitops/praxis/Chart.yaml",
    "automation/gitops/bootstrap-infra/Chart.yaml",
    "qa-automation/healthcheck.yml",
    "qa-automation/e2e.yml",
]:
    require((ROOT / required).is_file(), f"Publishing House artifact is missing: {required}")

nav = (ROOT / "content/modules/ROOT/nav.adoc").read_text()
for target in re.findall(r"xref:([^\[]+)", nav):
    require((PAGES / target).is_file(), f"nav target does not exist: {target}")

for module in MODULES:
    text = module.read_text()
    require(len(text.splitlines()) >= 50, f"module is too short: {module.name}")
    for heading in ["== What you will learn", "== See:", "== Do:", "== Key takeaway"]:
        require(heading in text, f"{module.name} lacks {heading}")
    for marker in re.findall(r"\[source,bash[^\]]*\]", text):
        require('role="execute"' in marker, f"non-executable command block in {module.name}")
        require('subs="attributes+"' in marker, f"attributes disabled in {module.name}")

ui = yaml.safe_load((ROOT / "ui-config.yml").read_text())
require({tab["name"] for tab in ui["tabs"]} == {"Terminal", "App UI", "OCP Console"}, "UI tabs are incomplete")

catalog_text = (ROOT / "catalog/common.yaml").read_text()
catalog = yaml.safe_load(catalog_text)
require(catalog["__meta__"]["catalog"]["category"] in {"Workshops", "Demos", "Labs", "Sandboxes", "Brand_Events"}, "invalid category")
require(catalog["__meta__"]["catalog"]["reportingLabels"]["primaryBU"] == "Hybrid_Platforms", "invalid business unit")
require("components" not in catalog["__meta__"], "tenant integration CI must not provision a cluster component")
require(catalog["__meta__"]["catalog"]["workshop_user_mode"] == "none", "single-tenant lab must assign provision data directly to the workshop seat")
require(catalog["__meta__"]["sandbox_api"]["actions"]["destroy"]["catch_all"] is False, "destroy must run tenant cleanup workloads")
dev = yaml.safe_load((ROOT / "catalog/dev.yaml").read_text())
selector = dev["__meta__"]["sandboxes"][0]["cloud_selector"]
require(selector == {"purpose": "dev", "cloud": "cnv-dedicated-shared", "lab": "ai-lab-xeon6-inference"}, "dev CI must select the registered Intel Inference integration cluster")
workloads = catalog["workloads"]
require(all(isinstance(item, str) and item.count(".") == 2 for item in workloads), "workloads must use fully qualified collection names")
virtual_key_workload = "rhpds.litellm_virtual_keys.ocp4_workload_litellm_virtual_keys"
require("#include /includes/secrets/litemaas-master_api.yaml" in catalog_text, "LiteMaaS master API include is required")
require("https://github.com/rhpds/rhpds.litellm_virtual_keys.git" in catalog_text, "LiteMaaS virtual-key collection is required")
require(workloads.index("agnosticd.namespaced_workloads.ocp4_workload_tenant_keycloak_user") < workloads.index("agnosticd.namespaced_workloads.ocp4_workload_tenant_namespace") < workloads.index(virtual_key_workload) < workloads.index("praxis_ai_gateway.automation.configure_praxis") < workloads.index("agnosticd.core_workloads.ocp4_workload_gitops_bootstrap") < workloads.index("agnosticd.showroom.ocp4_workload_showroom"), "invalid tenant workload order")
require(virtual_key_workload in catalog["remove_workloads"], "LiteMaaS virtual key cleanup is required")
require(catalog["ocp4_workload_litellm_virtual_keys_models"] == ["{{ praxis_model_name }}"], "Praxis and LiteMaaS must select the same model variable")
require(catalog["praxis_model_base_url"] == "{{ litellm_api_endpoint }}/v1", "Praxis must consume the generated LiteMaaS endpoint")
require(catalog["praxis_model_api_key"] == "{{ litellm_virtual_key }}", "Praxis must consume the generated virtual key")
require(not catalog["ocp4_workload_litellm_virtual_keys_enable_user_info_data"], "LiteMaaS credentials must not enter user data")

user_data = catalog.get("ocp4_workload_showroom_user_data", {})
require(not any("maas" in key.lower() or "litellm" in key.lower() or "key" in key.lower() for key in user_data), "Showroom user data must not receive MaaS credentials")

ansible_tasks = (ROOT / "automation/ansible/roles/configure_praxis/tasks/main.yml").read_text()
require(ansible_tasks.count("no_log: true") >= 3, "credential-bearing Ansible tasks must use no_log")

runtime_values = yaml.safe_load((ROOT / "automation/gitops/praxis/values.yaml").read_text())
bootstrap_values = yaml.safe_load((ROOT / "automation/gitops/bootstrap-infra/values.yaml").read_text())
images = list(runtime_values["images"].values()) + [bootstrap_values["praxis"]["uiImage"]]
require(all("@sha256:" in image for image in images), "all runtime images must be digest pinned")
bootstrap_template = (ROOT / "automation/gitops/bootstrap-infra/templates/application.yaml").read_text()
require('namespace: {{ .Values.namespace | quote }}' in bootstrap_template, "GitOps destination must use the tenant namespace value")
require(catalog["ocp4_workload_gitops_bootstrap_helm_values"]["namespace"] == "{{ praxis_lab_namespace }}", "catalog must pass the tenant namespace to GitOps")

spec = yaml.safe_load((ROOT / "publishing-house/spec.yaml").read_text())
require(spec["project"]["deployment_mode"] == "rhdp_published", "invalid Publishing House deployment mode")
require(spec["spec"]["environment"]["topology"] == "shared-tenant", "Publishing House topology must be shared-tenant")
require(spec["spec"]["environment"]["gpu_nodes"] == 0, "the Praxis lab must not allocate a local GPU")
require(spec["spec"]["environment"]["ai_requirement"] == "maas", "MaaS must remain the replaceable model access mechanism")

print(f"LAB PREFLIGHT: GREEN ({len(MODULES)} hands-on modules)")
