#!/usr/bin/env python3
"""Validate an SCOS change-order evidence manifest without writing live data."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FINAL_STATUSES = {"DRAFT", "READY FOR HUMAN REVIEW", "READY FOR OWNERSHIP REVIEW"}
EVIDENCE_STATUSES = {"Confirmed", "Inferred", "Missing", "Conflicting"}


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def finite_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def nested(data: dict, *keys: str) -> object:
    current: object = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def validate(data: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    status = data.get("status")
    if status not in FINAL_STATUSES:
        errors.append(f"status must be one of {sorted(FINAL_STATUSES)}")

    required_text = [
        ("project.projectID", nested(data, "project", "projectID")),
        ("project.projectName", nested(data, "project", "projectName")),
        ("change.description", nested(data, "change", "description")),
        ("buyout.buyoutUID", nested(data, "buyout", "buyoutUID")),
        ("buyout.buyoutPackage", nested(data, "buyout", "buyoutPackage")),
    ]
    for label, value in required_text:
        if not nonempty(value):
            errors.append(f"{label} is required")

    change_order_id = nested(data, "change", "changeOrderID")
    if change_order_id is not None and not isinstance(change_order_id, str):
        errors.append("change.changeOrderID must be a string when supplied")

    description = nested(data, "change", "description")
    if isinstance(description, str) and len(description) > 2000:
        errors.append("change.description exceeds the SCOS 2,000-character limit")

    source_url = nested(data, "change", "sourceDocumentUrl")
    if source_url:
        parsed = urlparse(str(source_url))
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append("change.sourceDocumentUrl must be a non-expiring HTTPS URL")
    else:
        warnings.append("change.sourceDocumentUrl is not yet populated")

    cost = data.get("cost")
    if not isinstance(cost, dict):
        errors.append("cost object is required")
    else:
        for key in ("subcontractorCO", "gcOverheadProfit", "finalOCO"):
            if not finite_number(cost.get(key)):
                errors.append(f"cost.{key} must be a finite number")
        if all(finite_number(cost.get(key)) for key in ("subcontractorCO", "gcOverheadProfit", "finalOCO")):
            calculated = round(float(cost["subcontractorCO"]) + float(cost["gcOverheadProfit"]), 2)
            final = round(float(cost["finalOCO"]), 2)
            if abs(calculated - final) > 0.01:
                errors.append(
                    "cost reconciliation failed: subcontractorCO + gcOverheadProfit "
                    f"= {calculated:.2f}, finalOCO = {final:.2f}"
                )

    references = data.get("drawingReferences")
    if not isinstance(references, list) or not references:
        errors.append("at least one drawingReferences row is required")
    else:
        sheets: list[str] = []
        details: list[str] = []
        for index, reference in enumerate(references, start=1):
            prefix = f"drawingReferences[{index}]"
            if not isinstance(reference, dict):
                errors.append(f"{prefix} must be an object")
                continue
            for key in ("sheet", "changeShown", "evidenceFile", "evidenceStatus"):
                if not nonempty(reference.get(key)):
                    errors.append(f"{prefix}.{key} is required")
            if reference.get("evidenceStatus") not in EVIDENCE_STATUSES:
                errors.append(f"{prefix}.evidenceStatus must be one of {sorted(EVIDENCE_STATUSES)}")
            page = reference.get("pdfPage")
            if not isinstance(page, int) or isinstance(page, bool) or page < 1:
                errors.append(f"{prefix}.pdfPage must be a positive integer")
            issue_date = reference.get("issueDate")
            if issue_date and (not isinstance(issue_date, str) or not DATE_PATTERN.match(issue_date)):
                errors.append(f"{prefix}.issueDate must use YYYY-MM-DD")
            if nonempty(reference.get("sheet")):
                sheets.append(str(reference["sheet"]).strip())
            if nonempty(reference.get("detailSection")):
                details.append(str(reference["detailSection"]).strip())

        if len(", ".join(dict.fromkeys(sheets))) > 80:
            warnings.append("combined Drawing Page text exceeds 80 characters; prepare a compact SCOS summary")
        if len("; ".join(dict.fromkeys(details))) > 120:
            warnings.append("combined Detail / Section text exceeds 120 characters; prepare a compact SCOS summary")
        if any(ref.get("evidenceStatus") in {"Missing", "Conflicting"} for ref in references if isinstance(ref, dict)):
            errors.append("drawing trace contains Missing or Conflicting evidence")
        elif any(ref.get("evidenceStatus") == "Inferred" for ref in references if isinstance(ref, dict)):
            warnings.append("drawing trace contains inferred evidence requiring human review")

    schedule = data.get("schedule")
    if not isinstance(schedule, dict):
        errors.append("schedule object is required")
    else:
        requested = schedule.get("timeExtensionRequested")
        days = schedule.get("days")
        zero_days_confirmed = schedule.get("zeroDaysConfirmed")
        if not isinstance(requested, bool):
            errors.append("schedule.timeExtensionRequested must be true or false")
        if not isinstance(days, int) or isinstance(days, bool) or days < 0:
            errors.append("schedule.days must be a non-negative integer")
        if zero_days_confirmed is not None and not isinstance(zero_days_confirmed, bool):
            errors.append("schedule.zeroDaysConfirmed must be true or false when supplied")
        if days == 0 and zero_days_confirmed is not True:
            errors.append(
                "schedule.zeroDaysConfirmed must be true after the user confirms that 0 days is intentional"
            )
        if requested is False and isinstance(days, int) and days != 0:
            errors.append("schedule.days must be 0 when no time extension is requested")
        if requested is True and days == 0:
            warnings.append("time extension is requested but schedule.days is 0")

    review = data.get("review")
    if not isinstance(review, dict):
        errors.append("review object is required")
    else:
        for key in ("evidenceStatus", "drawingTraceStatus", "scopeStatus", "costReconciliationStatus"):
            if review.get(key) != "READY":
                errors.append(f"review.{key} must be READY before the manifest advances")
        approval = review.get("ownershipApprovalStatus")
        if approval not in {"PENDING", "APPROVED"}:
            errors.append("review.ownershipApprovalStatus must be PENDING or APPROVED")
        if status != "DRAFT" and approval == "APPROVED":
            warnings.append("ownership approval must still be verified through the separate SCOS approval action")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(json.dumps({"ok": False, "errors": [str(error)], "warnings": []}, indent=2))
        return 2

    if not isinstance(data, dict):
        print(json.dumps({"ok": False, "errors": ["manifest root must be an object"], "warnings": []}, indent=2))
        return 2

    errors, warnings = validate(data)
    print(json.dumps({"ok": not errors, "errors": errors, "warnings": warnings}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
