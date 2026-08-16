import pytest
from engine.domain.evaluator import ActionEvaluator
from engine.domain.models import EvaluationResult
from engine.providers.factory import LLMFactory

def test_evaluator_multi_option_combination():
    mock_prov = LLMFactory.get_provider("mock_fallback")
    evaluator = ActionEvaluator(mock_prov)

    previous_opcoes = [
        {"texto": "1. Fortificar muralhas da capital", "impacto": {"dinheiro": -400, "poder_militar": 150}},
        {"texto": "2. Construir celeiro real", "impacto": {"dinheiro": -250, "poder_militar": 0}},
        {"texto": "3. Enviar embaixador", "impacto": {"dinheiro": -100, "poder_militar": 0}}
    ]
    world_state = {
        "gold": 2000,
        "military": 800,
        "population": 10000,
        "current_day": 10
    }

    res = evaluator.evaluate_action(
        campaign_id="c_test",
        action_text="quero fazer 1 e 2 ao mesmo tempo",
        previous_opcoes=previous_opcoes,
        current_world_state=world_state,
        active_tasks=[],
        periodic_events=[]
    )

    assert isinstance(res, EvaluationResult)
    assert 1 in res.opcoes_selecionadas and 2 in res.opcoes_selecionadas
    assert res.delta_dinheiro == -650
    assert res.delta_poder_militar == 150
    assert res.viabilidade is True
    assert res.dias_passados >= 1

def test_evaluator_insufficient_resources_unviability():
    mock_prov = LLMFactory.get_provider("mock_fallback")
    evaluator = ActionEvaluator(mock_prov)

    previous_opcoes = [
        {"texto": "1. Comprar navio de guerra", "impacto": {"dinheiro": -3000, "poder_militar": 400}}
    ]
    world_state = {
        "gold": 500,
        "military": 200,
        "population": 5000,
        "current_day": 5
    }

    res = evaluator.evaluate_action(
        campaign_id="c_test",
        action_text="quero a opção 1",
        previous_opcoes=previous_opcoes,
        current_world_state=world_state,
        active_tasks=[],
        periodic_events=[]
    )

    assert res.viabilidade is False
    assert "insuficiente" in res.motivo_inviabilidade.lower()

def test_evaluator_long_term_task_classification():
    mock_prov = LLMFactory.get_provider("mock_fallback")
    evaluator = ActionEvaluator(mock_prov)

    world_state = {
        "gold": 5000,
        "military": 1000,
        "population": 10000,
        "current_day": 1
    }

    res = evaluator.evaluate_action(
        campaign_id="c_test",
        action_text="construir um grande porto comercial no litoral",
        previous_opcoes=[],
        current_world_state=world_state,
        active_tasks=[],
        periodic_events=[]
    )

    assert isinstance(res, EvaluationResult)
    assert res.dias_passados >= 1
