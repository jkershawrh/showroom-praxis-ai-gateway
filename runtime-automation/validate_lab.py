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

catalog = yaml.safe_load((ROOT / "catalog/common.yaml").read_text())
require(catalog["__meta__"]["catalog"]["category"] in {"Workshops", "Demos", "Labs", "Sandboxes", "Brand_Events"}, "invalid category")
require(catalog["__meta__"]["catalog"]["reportingLabels"]["primaryBU"] == "AI", "invalid business unit")
workloads = [item["name"] for item in catalog["workloads"]]
require(workloads.index("ocp4_workload_authentication") < workloads.index("ocp4_workload_litellm_virtual_keys") < workloads.index("ocp4_workload_showroom"), "invalid workload order")

print(f"LAB PREFLIGHT: GREEN ({len(MODULES)} hands-on modules)")
