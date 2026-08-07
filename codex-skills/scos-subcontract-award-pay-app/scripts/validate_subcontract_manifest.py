#!/usr/bin/env python3
import json
import math
import sys
from pathlib import Path


def fail(message):
    print(f"ERROR: {message}")
    return 1


def main():
    if len(sys.argv) != 2:
        return fail("usage: validate_subcontract_manifest.py manifest.json")
    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"cannot read manifest: {exc}")

    errors = []
    readiness = data.get("readiness") or {}
    bids = data.get("bids") or []
    recommendation = data.get("recommendation") or {}
    agreement = data.get("agreement") or {}
    sov = data.get("scheduleOfValues") or []

    if not isinstance(bids, list) or not bids:
        errors.append("at least one normalized bid is required")
    if recommendation.get("blocked") is False and not recommendation.get("recommendedBidder"):
        errors.append("an unblocked recommendation requires recommendedBidder")
    if readiness.get("noticeOfAwardReady") and recommendation.get("blocked") is not False:
        errors.append("Notice of Award cannot be ready while recommendation is blocked")
    if readiness.get("noticeOfAwardReady") and (readiness.get("missingDocuments") or readiness.get("missingDecisions") or readiness.get("bindingBlockers")):
        errors.append("Notice of Award cannot be ready with missing evidence, decisions, or blockers")

    amount = agreement.get("originalContractAmount")
    if amount is not None and (not isinstance(amount, (int, float)) or not math.isfinite(amount) or amount < 0):
        errors.append("originalContractAmount must be a nonnegative finite number or null")
    if readiness.get("firstPayAppReady"):
        if not readiness.get("agreementReady"):
            errors.append("first pay app cannot be ready before agreement data is ready")
        if amount is None:
            errors.append("first pay app requires originalContractAmount")
        total = sum(line.get("scheduledValue", 0) for line in sov if isinstance(line.get("scheduledValue"), (int, float)))
        if amount is not None and abs(total - amount) >= 0.005:
            errors.append(f"SOV total {total:.2f} does not equal original contract amount {amount:.2f}")
    if agreement.get("terminationCureDays") != 7:
        errors.append("terminationCureDays must equal 7")
    if agreement.get("contractTemplateStatus") != "PROVIDED" and agreement.get("terminationLanguage"):
        errors.append("termination language cannot be drafted without the base subcontract")

    for index, bid in enumerate(bids, 1):
        gap_cost = bid.get("approvedGapCost")
        evaluated = bid.get("evaluatedPrice")
        base = bid.get("baseBid")
        alternates = bid.get("acceptedAlternates")
        if gap_cost is None and evaluated is not None:
            errors.append(f"bid {index} cannot have evaluatedPrice when approvedGapCost is unknown")
        if evaluated is not None and not all(isinstance(value, (int, float)) for value in (base, alternates, gap_cost)):
            errors.append(f"bid {index} evaluatedPrice requires baseBid, acceptedAlternates, and approvedGapCost")
        if all(isinstance(value, (int, float)) for value in (base, alternates, gap_cost, evaluated)) and abs((base + alternates + gap_cost) - evaluated) >= 0.005:
            errors.append(f"bid {index} evaluatedPrice does not equal baseBid plus acceptedAlternates plus approvedGapCost")

    for message in errors:
        print(f"ERROR: {message}")
    if errors:
        return 1
    print("OK: subcontract manifest passed controlled validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
