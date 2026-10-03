from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterable


DEFAULT_GOVERNANCE_PATH = Path("canon/registries/canon-governance.json")


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str  # reject | warn
    message: str
    evidence: str | None = None


@dataclass
class GateResult:
    decision: str  # PASS | WARN | REJECT
    artifact_id: str
    artifact_kind: str
    findings: list[Finding] = field(default_factory=list)
    governance_version: str | None = None
    canon_status: str = "DERIVED"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    input_sha256: str = ""

    @property
    def accepted(self) -> bool:
        return self.decision != "REJECT"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["accepted"] = self.accepted
        return payload


class CanonGate:
    """Deterministic first-line validator for Paramecia canon and production inputs.

    It never promotes content to canon. PASS means only that this gate found no
    blocking rule violation. Creator authority remains external to the gate.
    """

    HUMAN_PRESENCE_PATTERNS = (
        r"\bhuman(?:s)?\s+(?:tavern|village|city|kingdom|house|dwelling|resident|inhabitant|citizen|bartender|guard|soldier|merchant|student|teacher)s?\b",
        r"\b(?:tavern|chair|door|doorway|corridor|desk|bed|stair|tool|weapon)s?\s+(?:for|made for|sized for)\s+humans?\b",
        r"\bhuman[- ](?:sized|scale|scaled|proportioned|ergonomic|ergonomics|architecture)\b",
        r"\bpost[- ]human\b",
        r"\banthropocentric\s+(?:design|architecture|ergonomics|assumption)s?\b",
    )

    REVERSIBILITY_PATTERNS = (
        r"\benvironmental damage (?:is|was|will be) (?:fully )?reversible\b",
        r"\becological damage (?:is|was|will be) (?:fully )?reversible\b",
        r"\bthe ecosystem (?:can|will) (?:simply )?reset\b",
        r"\bhabitat damage (?:can|will) be undone (?:instantly|without consequence)\b",
    )

    COERCION_PATTERNS = (
        r"\bno escape\b",
        r"\binescapable\b",
        r"\bmandatory submission\b",
        r"\babsolute control\b",
    )

    EXIT_OR_CONSENT_PATTERNS = (
        r"\bvisible exit\b",
        r"\baccessible exit\b",
        r"\bmay leave\b",
        r"\bcan leave\b",
        r"\bred gate\b",
        r"\bstop signal\b",
        r"\bconsent\b",
    )

    def __init__(self, governance_path: str | Path = DEFAULT_GOVERNANCE_PATH, audit_log: str | Path | None = None):
        self.governance_path = Path(governance_path)
        self.audit_log = Path(audit_log) if audit_log else None
        self.governance = self._load_governance(self.governance_path)

    @staticmethod
    def _load_governance(path: Path) -> dict[str, Any]:
        if not path.exists():
            raise FileNotFoundError(f"Canon governance registry not found: {path}")
        return json.loads(path.read_text(encoding="utf-8"))

    def scan_text(
        self,
        text: str,
        *,
        artifact_id: str = "UNSPECIFIED",
        artifact_kind: str = "lore",
        target_scope: str | None = None,
        requested_status: str = "DERIVED",
    ) -> GateResult:
        findings: list[Finding] = []
        normalized = " ".join(text.lower().split())

        findings.extend(self._pattern_findings(normalized, self.HUMAN_PRESENCE_PATTERNS, "CG-NONHUMAN-001", "reject", "Human existence or human-default architecture detected. Paramecia canon does not permit human presence or human-default spatial assumptions."))
        findings.extend(self._pattern_findings(normalized, self.REVERSIBILITY_PATTERNS, "CG-ECOLOGY-001", "reject", "Environmental consequence was described as trivially reversible; consequence must not be erased by default."))

        if self._matches_any(normalized, self.COERCION_PATTERNS) and not self._matches_any(normalized, self.EXIT_OR_CONSENT_PATTERNS):
            findings.append(Finding("CG-CONSENT-001", "reject", "Confinement or absolute-control language lacks an explicit exit or consent/safety mechanism."))

        if requested_status == "LOCKED":
            findings.append(Finding("CG-AUTHORITY-001", "reject", "Canongate cannot promote material to LOCKED canon. Only explicit creator declaration may do that."))

        if target_scope and target_scope not in set(self.governance.get("scopes", [])) | set(self.governance.get("branch_boundaries", {}).keys()):
            findings.append(Finding("CG-SCOPE-001", "warn", f"Unknown target scope '{target_scope}'. Route to HOLDING until scope is resolved."))

        if "hells branch" in normalized or "hell's branch" in normalized:
            if target_scope and target_scope not in {"HELLS_BRANCH", "BRANCH", "LOCAL", "PRODUCTION"}:
                findings.append(Finding("CG-BRANCH-001", "warn", "Hell's Branch material is branch-local by default and must not silently propagate into shared Paramecia/Triquel canon."))

        result = self._finish(text, artifact_id, artifact_kind, findings)
        self._audit(result)
        return result

    def scan_asset(self, asset: dict[str, Any]) -> GateResult:
        artifact_id = str(asset.get("asset_id") or asset.get("name") or "UNSPECIFIED-ASSET")
        description = str(asset.get("description") or "")
        findings: list[Finding] = []

        required = tuple(self.governance.get("forward_build_gate", []))
        metadata = asset.get("metadata") or {}
        if not isinstance(metadata, dict):
            findings.append(Finding("CG-META-000", "reject", "Asset metadata must be an object/dictionary."))
            metadata = {}

        missing = [key for key in required if key not in metadata]
        if missing:
            findings.append(Finding("CG-META-001", "warn", "Asset is missing forward-build metadata: " + ", ".join(missing)))

        text_result = self.scan_text(
            description,
            artifact_id=artifact_id,
            artifact_kind="asset-description",
            target_scope=asset.get("scope"),
            requested_status=str(asset.get("requested_status") or "DERIVED"),
        )
        findings.extend(text_result.findings)

        result = self._finish(json.dumps(asset, sort_keys=True, default=str), artifact_id, "asset", findings)
        self._audit(result)
        return result

    @staticmethod
    def _matches_any(text: str, patterns: Iterable[str]) -> bool:
        return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)

    def _pattern_findings(self, text: str, patterns: Iterable[str], rule_id: str, severity: str, message: str) -> list[Finding]:
        out: list[Finding] = []
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                out.append(Finding(rule_id, severity, message, match.group(0)))
                break
        return out

    def _finish(self, raw_input: str, artifact_id: str, artifact_kind: str, findings: list[Finding]) -> GateResult:
        severities = {finding.severity for finding in findings}
        decision = "REJECT" if "reject" in severities else "WARN" if "warn" in severities else "PASS"
        return GateResult(
            decision=decision,
            artifact_id=artifact_id,
            artifact_kind=artifact_kind,
            findings=findings,
            governance_version=self.governance.get("schema_version"),
            canon_status="DERIVED",
            input_sha256=hashlib.sha256(raw_input.encode("utf-8")).hexdigest(),
        )

    def _audit(self, result: GateResult) -> None:
        if not self.audit_log:
            return
        self.audit_log.parent.mkdir(parents=True, exist_ok=True)
        with self.audit_log.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")
