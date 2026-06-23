import pytest
from src.marketplace import Model, Marketplace

def test_add_model():
    marketplace = Marketplace()
    model = Model("Test Model", "Test Indication", "Test Performance Summary", "Test Badge", "Test Specialty", "Test Data Source Diversity", "Test Compliance Level", "Test Compliance Package")
    marketplace.add_model(model)
    assert len(marketplace.models) == 1

def test_list_models():
    marketplace = Marketplace()
    model1 = Model("Test Model 1", "Test Indication 1", "Test Performance Summary 1", "Test Badge 1", "Test Specialty 1", "Test Data Source Diversity 1", "Test Compliance Level 1", "Test Compliance Package 1")
    model2 = Model("Test Model 2", "Test Indication 2", "Test Performance Summary 2", "Test Badge 2", "Test Specialty 2", "Test Data Source Diversity 2", "Test Compliance Level 2", "Test Compliance Package 2")
    marketplace.add_model(model1)
    marketplace.add_model(model2)
    assert len(marketplace.list_models()) == 2
    assert len(marketplace.list_models(specialty="Test Specialty 1")) == 1

def test_get_compliance_package():
    marketplace = Marketplace()
    model = Model("Test Model", "Test Indication", "Test Performance Summary", "Test Badge", "Test Specialty", "Test Data Source Diversity", "Test Compliance Level", "Test Compliance Package")
    marketplace.add_model(model)
    assert marketplace.get_compliance_package("Test Model") == "Test Compliance Package"
    assert marketplace.get_compliance_package("Non-existent Model") is None
