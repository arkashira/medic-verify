from medic_verify import validate_ai_model, validate_ai_model_compliance, format_validation_results
from medic_verify import PatientData, AIModel
import pytest

@pytest.fixture
def patient_data():
    return [PatientData(1, 25, "diagnosis1"), PatientData(2, 30, "diagnosis2")]

@pytest.fixture
def ai_model():
    return AIModel("model1", 0.9)

def test_validate_ai_model(patient_data, ai_model):
    validation_results = validate_ai_model(patient_data, ai_model)
    assert validation_results["model_name"] == ai_model.name
    assert validation_results["accuracy"] == ai_model.accuracy
    assert len(validation_results["patient_data"]) == len(patient_data)

def test_validate_ai_model_compliance(patient_data, ai_model):
    assert validate_ai_model_compliance(patient_data, ai_model) == True

def test_format_validation_results(patient_data, ai_model):
    validation_results = validate_ai_model(patient_data, ai_model)
    formatted_results = format_validation_results(validation_results)
    assert "model_name" in formatted_results
    assert "accuracy" in formatted_results
    assert "patient_data" in formatted_results

def test_validate_ai_model_edge_case():
    patient_data = [PatientData(1, 25, "diagnosis1")]
    ai_model = AIModel("model1", 0.7)
    validation_results = validate_ai_model(patient_data, ai_model)
    assert validation_results["validation_result"] == "failed"

def test_validate_ai_model_compliance_edge_case():
    patient_data = [PatientData(1, 25, "diagnosis1")]
    ai_model = AIModel("model1", 0.9)
    assert validate_ai_model_compliance(patient_data, ai_model) == True
