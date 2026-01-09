import json
import sys
import os

MANIFEST_PATH = 'src/logic-manifest.json'

def fail_build(reason):
    print(f"❌ CONSTITUTIONAL VIOLATION: {reason}")
    sys.exit(1)

def validate_manifest():
    if not os.path.exists(MANIFEST_PATH):
        fail_build(f"Manifest not found at {MANIFEST_PATH}")

    try:
        with open(MANIFEST_PATH, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        fail_build("Manifest is not valid JSON.")

    constraints = data.get('constitutional_constraints', {})

    # 1. Enforce Memory (Article 3)
    if constraints.get('allow_erasure') is not False:
        fail_build("Attempted to enable 'allow_erasure'. This violates Article 3 (Memory).")

    # 2. Enforce Stability (Article 5)
    if constraints.get('min_review_period_hours', 0) < 72:
        fail_build("Review period dropped below 72 hours. This violates Article 5 (Stability).")

    # 3. Enforce Justification (Article 3)
    heuristics = data.get('active_heuristics', [])
    for heuristic in heuristics:
        if 'justification_ref' not in heuristic or not heuristic['justification_ref']:
            fail_build(f"Heuristic {heuristic.get('id', 'UNKNOWN')} is missing a Constitutional citation.")

    print("✅ Constitutional Integrity Verified.")
    sys.exit(0)

if __name__ == "__main__":
    validate_manifest()
