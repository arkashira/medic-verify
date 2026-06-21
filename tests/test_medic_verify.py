import json
import os
import pytest
from medic_verify import load_model, load_data, compute_reliability_metrics, generate_report

def test_load_model():
    model_path = 'test_model.json'
    with open(model_path, 'w') as f:
        json.dump({'test': 'model'}, f)
    model = load_model(model_path)
    assert model == {'test': 'model'}
    with pytest.raises(ValueError):
        load_model('non_existent_model.json')
    os.remove(model_path)

def test_load_data():
    data_path = 'test_data.json'
    with open(data_path, 'w') as f:
        json.dump([{'prediction': 1, 'label': 1}, {'prediction': 0, 'label': 0}], f)
    data = load_data(data_path)
    assert data == [{'prediction': 1, 'label': 1}, {'prediction': 0, 'label': 0}]
    with pytest.raises(ValueError):
        load_data('non_existent_data.json')
    os.remove(data_path)

def test_compute_reliability_metrics():
    model = {'test': 'model'}
    data = [{'prediction': 1, 'label': 1}, {'prediction': 0, 'label': 0}]
    metrics = compute_reliability_metrics(model, data)
    assert metrics.accuracy == 1.0
    assert metrics.calibration_error == 0.0
    assert metrics.drift_detection == 0.0

def test_generate_report(tmp_path):
    model_path = tmp_path / 'test_model.json'
    data_path = tmp_path / 'test_data.json'
    output_path = tmp_path / 'report.json'
    with open(model_path, 'w') as f:
        json.dump({'test': 'model'}, f)
    with open(data_path, 'w') as f:
        json.dump([{'prediction': 1, 'label': 1}, {'prediction': 0, 'label': 0}], f)
    generate_report(str(model_path), str(data_path), str(output_path))
    with open(output_path, 'r') as f:
        report = json.load(f)
    assert report['accuracy'] == 1.0
    assert report['calibration_error'] == 0.0
    assert report['drift_detection'] == 0.0
    with pytest.raises(FileNotFoundError):
        generate_report(str(model_path), str(data_path), str(output_path))
    os.remove(model_path)
    os.remove(data_path)
    os.remove(output_path)

def test_generate_report_empty_dataset(tmp_path):
    model_path = tmp_path / 'test_model.json'
    data_path = tmp_path / 'test_data.json'
    output_path = tmp_path / 'report.json'
    with open(model_path, 'w') as f:
        json.dump({'test': 'model'}, f)
    with open(data_path, 'w') as f:
        json.dump([], f)
    with pytest.raises(ValueError):
        generate_report(str(model_path), str(data_path), str(output_path))
    os.remove(model_path)
    os.remove(data_path)
