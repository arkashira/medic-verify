import argparse
import json
import os
from dataclasses import dataclass
from typing import List

@dataclass
class ReliabilityReport:
    accuracy: float
    calibration_error: float
    drift_detection: float

def load_model(model_path: str) -> dict:
    try:
        with open(model_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError(f"Model file not found: {model_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid model format: {model_path}")

def load_data(data_path: str) -> List[dict]:
    try:
        with open(data_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError(f"Data file not found: {data_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid data format: {data_path}")

def compute_reliability_metrics(model: dict, data: List[dict]) -> ReliabilityReport:
    accuracy = sum(1 for item in data if item['prediction'] == item['label']) / len(data)
    calibration_error = sum(abs(item['prediction'] - item['label']) for item in data) / len(data)
    drift_detection = sum(1 for item in data if item['prediction'] != item['label']) / len(data)
    return ReliabilityReport(accuracy, calibration_error, drift_detection)

def generate_report(model_path: str, data_path: str, output_path: str) -> None:
    if os.path.exists(output_path):
        raise FileNotFoundError(f"Output file already exists: {output_path}")
    model = load_model(model_path)
    data = load_data(data_path)
    if not data:
        raise ValueError("Empty dataset")
    metrics = compute_reliability_metrics(model, data)
    report = {
        'accuracy': metrics.accuracy,
        'calibration_error': metrics.calibration_error,
        'drift_detection': metrics.drift_detection,
    }
    with open(output_path, 'w') as f:
        json.dump(report, f)

def main() -> None:
    parser = argparse.ArgumentParser(description='Medic-Verify CLI tool')
    parser.add_argument('--model', required=True, help='Path to the model file')
    parser.add_argument('--data', required=True, help='Path to the data file')
    parser.add_argument('--output', default='report.json', help='Path to the output report file')
    args = parser.parse_args()
    generate_report(args.model, args.data, args.output)

if __name__ == '__main__':
    main()
