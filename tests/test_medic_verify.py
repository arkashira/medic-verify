import json
import pytest

from medic_verify import (
    ValidationResult,
    check_no_pii,
    format_results,
    validate_model,
)


def simple_model(features):
    """Predict 1 if age > 50 else 0."""
    return 1 if features.get("age", 0) > 50 else 0


def test_check_no_pii_passes():
    dataset = [
        {"features": {"age": 30}, "label": 0, "metadata": {"ethnicity": "A"}},
        {"features": {"age": 70}, "label": 1, "metadata": {"ethnicity": "B"}},
    ]
    # Should not raise
    check_no_pii(dataset)


def test_check_no_pii_raises_on_top_level():
    dataset = [
        {"features": {"age": 30}, "label": 0, "name": "John Doe"},
    ]
    with pytest.raises(ValueError) as exc:
        check_no_pii(dataset)
    assert "prohibited field 'name' at top level" in str(exc.value)


def test_check_no_pii_raises_in_metadata():
    dataset = [
        {"features": {"age": 30}, "label": 0, "metadata": {"ssn": "123-45-6789"}},
    ]
    with pytest.raises(ValueError) as exc:
        check_no_pii(dataset)
    assert "prohibited field 'ssn' in metadata" in str(exc.value)


def test_validate_model_happy_path():
    dataset = [
        {
            "features": {"age": 60},
            "label": 1,
            "metadata": {"ethnicity": "A"},
        },
        {
            "features": {"age": 30},
            "label": 0,
            "metadata": {"ethnicity": "A"},
        },
        {
            "features": {"age": 70},
            "label": 0,  # model will predict 1 -> wrong
            "metadata": {"ethnicity": "B"},
        },
        {
            "features": {"age": 40},
            "label": 1,  # model will predict 0 -> wrong
            "metadata": {"ethnicity": "B"},
        },
    ]

    result = validate_model(simple_model, dataset, group_by="ethnicity")
    # Two correct out of four
    assert isinstance(result, ValidationResult)
    assert result.overall_accuracy == 0.5

    # Group A: both correct
    assert result.group_accuracies["A"] == 1.0
    # Group B: both wrong
    assert result.group_accuracies["B"] == 0.0


def test_validate_model_missing_group_field():
    dataset = [
        {
            "features": {"age": 55},
            "label": 1,
            "metadata": {"ethnicity": "X"},
        },
        {
            "features": {"age": 45},
            "label": 0,
            # No ethnicity metadata
        },
    ]

    result = validate_model(simple_model, dataset, group_by="ethnicity")
    # Both predictions correct
    assert result.overall_accuracy == 1.0
    # Two groups: "X" and "unknown"
    assert result.group_accuracies["X"] == 1.0
    assert result.group_accuracies["unknown"] == 1.0


def test_validate_model_empty_dataset():
    with pytest.raises(ValueError) as exc:
        validate_model(simple_model, [], group_by="ethnicity")
    assert "Dataset must contain at least one record" in str(exc.value)


def test_format_results():
    result = ValidationResult(overall_accuracy=0.75, group_accuracies={"A": 1.0, "B": 0.5})
    json_str = format_results(result)
    parsed = json.loads(json_str)
    assert parsed["overall_accuracy"] == 0.75
    assert parsed["group_accuracies"]["A"] == 1.0
    assert parsed["group_accuracies"]["B"] == 0.5
