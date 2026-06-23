import json
from dataclasses import dataclass
from typing import List

@dataclass
class Model:
    name: str
    indication: str
    performance_summary: str
    badge: str
    specialty: str
    data_source_diversity: str
    compliance_level: str
    compliance_package: str

class Marketplace:
    def __init__(self):
        self.models = []

    def add_model(self, model: Model):
        self.models.append(model)

    def list_models(self, specialty: str = None, data_source_diversity: str = None, compliance_level: str = None):
        filtered_models = self.models
        if specialty:
            filtered_models = [model for model in filtered_models if model.specialty == specialty]
        if data_source_diversity:
            filtered_models = [model for model in filtered_models if model.data_source_diversity == data_source_diversity]
        if compliance_level:
            filtered_models = [model for model in filtered_models if model.compliance_level == compliance_level]
        return filtered_models

    def get_compliance_package(self, model_name: str):
        for model in self.models:
            if model.name == model_name:
                return model.compliance_package
        return None
