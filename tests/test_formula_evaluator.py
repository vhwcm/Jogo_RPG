import pytest
from engine.domain.formula_evaluator import evaluate_formula, calculate_event_effect, parse_happiness_value

def test_parse_happiness_value():
    assert parse_happiness_value("70%") == 70.0
    assert parse_happiness_value("70") == 70.0
    assert parse_happiness_value(70) == 70.0
    assert parse_happiness_value(0.7) == 70.0
    assert parse_happiness_value("100%") == 100.0
    assert parse_happiness_value("0%") == 0.0
    assert parse_happiness_value(None) == 70.0

def test_evaluate_basic_arithmetic():
    context = {"populacao": 10000, "felicidade": 70.0}
    formula = "(populacao * 0.05) * (felicidade / 100)"
    result = evaluate_formula(formula, context)
    assert result == 350.0

def test_evaluate_with_functions_and_operations():
    context = {"populacao": 12500, "felicidade": 80.0, "ouro": 500}
    formula = "round((populacao * 0.08) * (felicidade / 100))"
    result = evaluate_formula(formula, context)
    assert result == 800.0

def test_evaluate_invalid_or_malicious_syntax_safety():
    context = {"populacao": 10000}
    assert evaluate_formula("__import__('os').system('ls')", context) == 0.0
    assert evaluate_formula("open('/etc/passwd').read()", context) == 0.0
    assert evaluate_formula("invalid +++ syntax", context) == 0.0

def test_calculate_event_effect_formula():
    efeito = {
        "formula": "(populacao * 0.05) * (felicidade / 100)",
        "recurso": "dinheiro"
    }
    context = {
        "populacao": 10000,
        "felicidade": "70%",
        "gold": 5000
    }
    result = calculate_event_effect(efeito, context)
    assert result == {"dinheiro": 350}

def test_calculate_event_effect_static():
    efeito = {
        "dinheiro": 500,
        "poder_militar": 50
    }
    context = {
        "populacao": 10000,
        "felicidade": "70%"
    }
    result = calculate_event_effect(efeito, context)
    assert result == {"dinheiro": 500, "poder_militar": 50}

def test_calculate_event_effect_tax_increase():
    efeito = {
        "formula": "(populacao * 0.08) * (felicidade / 100)",
        "recurso": "dinheiro"
    }
    context = {
        "populacao": 20000,
        "felicidade": "75%"
    }
    result = calculate_event_effect(efeito, context)
    assert result == {"dinheiro": 1200}
