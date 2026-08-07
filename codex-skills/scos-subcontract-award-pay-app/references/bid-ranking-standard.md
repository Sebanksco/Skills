# Bid ranking standard

## Decision order

1. Required-document completeness.
2. Critical scope coverage.
3. Overall scope coverage.
4. Supported gap exposure and commercial/schedule risk.
5. Evaluated price.
6. Raw bid price as the final comparison, not the first.

## Coverage classification

- `COMPLETE`: all material requirements are covered or resolved.
- `MINOR_GAPS`: limited, priced, noncritical gaps remain.
- `MAJOR_GAPS`: material requirements are excluded, partial, silent, or conflicting.
- `UNDETERMINED`: evidence is insufficient.

Do not compare raw prices as equivalent when coverage classifications differ materially.

## Gap pricing

Calculate supported gap cost from documented sources only. Record low/high ranges when appropriate. Use the approved value for evaluated-price ranking; preserve the range and source.

`evaluatedPrice = baseBid + approvedGapCost + acceptedAlternates`

Example: Bid A is $10,000 below Bid B but carries $20,000 of supported uncovered scope. When coverage is otherwise comparable, Bid A's evaluated price is $10,000 higher and Bid B ranks ahead.

If a material gap has no supported cost, set evaluated price to null and block the final recommendation rather than assuming zero.

## Recommendation

Return the leading bidder only when required evidence is present, critical gaps are resolved, and the evaluated comparison is supported. Include reasons another bid lost, separating scope, risk, evaluated price, and raw price.
