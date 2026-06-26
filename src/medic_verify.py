import json
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Tuple


@dataclass(frozen=True)
class ValidationResult:
    """Container for validation metrics."""
    overall_accuracy: float
    group_accuracies: Dict[str, float]


def check_no_pii(
    dataset: List[Dict[str, Any]],
    prohibited_fields: Tuple[str, ...] = ("name", "ssn", "dob")
) -> None:
    """
    Ensure that no record in the dataset contains prohibited personally identifiable
    information (PII). Raises a ValueError if a violation is found.

    The check looks at top‑level keys and also inside an optional ``metadata`` dict.
    """
    for idx, record in enumerate(dataset):
        # Direct keys
        for field in prohibited_fields:
            if field in record:
                raise ValueError(
                    f"Record {idx} contains prohibited field '{field}' at top level."
                )
        # Inside metadata, if present
        meta = record.get("metadata", {})
        if isinstance(meta, dict):
            for field in prohibited_fields:
                if field in meta:
                    raise ValueError(
                        f"Record {idx} contains prohibited field '{field}' in metadata."
                    )


def _group_key(record: Dict[str, Any], group_by: str) -> str:
    """
    Return the grouping key for a record. If the requested ``group_by`` field is
    missing, return the string ``"unknown"``.
    """
    meta = record.get("metadata", {})
    if isinstance(meta, dict) and group_by in meta:
        return str(meta[group_by])
    # Fallback to top‑level if not in metadata
    return str(record.get(group_by, "unknown"))


def validate_model(
    model: Callable[[Dict[str, Any]], Any],
    dataset: List[Dict[str, Any]],
    group_by: str
) -> ValidationResult:
    """
    Validate an AI model against a patient dataset.

    Parameters
    ----------
    model:
        Callable that receives a ``features`` dict and returns a prediction.
    dataset:
        List of records, each containing at least ``features`` (dict) and ``label``.
        Optional ``metadata`` may hold grouping attributes.
    group_by:
        The key inside ``metadata`` (or top‑level) used to compute per‑group metrics.

    Returns
    -------
    ValidationResult
        Overall accuracy and per‑group accuracies.

    Raises
    ------
    ValueError
        If the dataset is empty or contains prohibited PII fields.
    """
    if not dataset:
        raise ValueError("Dataset must contain at least one record.")

    # Compliance check
    check_no_pii(dataset)

    total = 0
    correct = 0
    group_stats: Dict[str, Tuple[int, int]] = defaultdict(lambda: (0, 0))

    for record in dataset:
        features = record.get("features", {})
        true_label = record.get("label")
        pred = model(features)

        is_correct = pred == true_label
        total += 1
        correct += int(is_correct)

        grp = _group_key(record, group_by)
        grp_correct, grp_total = group_stats[grp]
        group_stats[grp] = (grp_correct + int(is_correct), grp_total + 1)

    overall_accuracy = correct / total if total else 0.0
    group_accuracies = {
        grp: (c / t if t else 0.0) for grp, (c, t) in group_stats.items()
    }

    return ValidationResult(overall_accuracy=overall_accuracy,
                            group_accuracies=group_accuracies)


def format_results(result: ValidationResult) -> str:
    """
    Convert a ``ValidationResult`` into a pretty‑printed JSON string.
    """
    payload = {
        "overall_accuracy": result.overall_accuracy,
        "group_accuracies": result.group_accuracies,
    }
    return json.dumps(payload, indent=2, sort_keys=True)
