import ast
import operator
from typing import Dict, Any, Union

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

_ALLOWED_FUNCTIONS = {
    "min": min,
    "max": max,
    "round": round,
    "int": int,
    "float": float,
    "abs": abs,
}

def parse_happiness_value(raw_val: Any) -> float:
    if raw_val is None:
        return 70.0
    if isinstance(raw_val, (int, float)):
        val = float(raw_val)
        if 0.0 <= val <= 1.0:
            return val * 100.0
        return val
    s = str(raw_val).replace("%", "").strip().replace(",", ".")
    try:
        val = float(s)
        if 0.0 <= val <= 1.0 and "%" not in str(raw_val):
            return val * 100.0
        return val
    except ValueError:
        return 70.0

def _safe_eval_node(node: ast.AST, context: Dict[str, Any]) -> Union[int, float]:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        return 0.0

    elif isinstance(node, ast.Name):
        var_name = node.id.lower()
        if var_name in context:
            val = context[var_name]
            if isinstance(val, (int, float)):
                return val
            try:
                return float(str(val).replace(".", "").replace(",", ""))
            except ValueError:
                return 0.0
        return 0.0

    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            left = _safe_eval_node(node.left, context)
            right = _safe_eval_node(node.right, context)
            if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right == 0:
                return 0.0
            return _ALLOWED_OPERATORS[op_type](left, right)
        return 0.0

    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            operand = _safe_eval_node(node.operand, context)
            return _ALLOWED_OPERATORS[op_type](operand)
        return 0.0

    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            fn_name = node.func.id.lower()
            if fn_name in _ALLOWED_FUNCTIONS:
                args = [_safe_eval_node(arg, context) for arg in node.args]
                return _ALLOWED_FUNCTIONS[fn_name](*args)
        return 0.0

    return 0.0

def evaluate_formula(formula: str, context: Dict[str, Any]) -> float:
    if not formula or not isinstance(formula, str):
        return 0.0
    try:
        parsed = ast.parse(formula.strip(), mode="eval")
        res = _safe_eval_node(parsed.body, context)
        return float(res)
    except Exception:
        return 0.0

def calculate_event_effect(efeito: Dict[str, Any], raw_context: Dict[str, Any]) -> Dict[str, int]:
    if not efeito or not isinstance(efeito, dict):
        return {}

    pop_val = raw_context.get("populacao", raw_context.get("population", 10000))
    try:
        pop_int = int(str(pop_val).replace(".", "").replace(",", ""))
    except (ValueError, TypeError):
        pop_int = 10000

    hap_float = parse_happiness_value(raw_context.get("felicidade", raw_context.get("happiness", "70%")))

    gold_val = raw_context.get("dinheiro", raw_context.get("gold", 5000))
    try:
        gold_int = int(str(gold_val).replace(".", "").replace(",", ""))
    except (ValueError, TypeError):
        gold_int = 5000

    mil_val = raw_context.get("poder_militar", raw_context.get("military", 1000))
    try:
        mil_int = int(str(mil_val).replace(".", "").replace(",", ""))
    except (ValueError, TypeError):
        mil_int = 1000

    normalized_context = {
        "populacao": pop_int,
        "population": pop_int,
        "felicidade": hap_float,
        "happiness": hap_float,
        "dinheiro": gold_int,
        "ouro": gold_int,
        "gold": gold_int,
        "poder_militar": mil_int,
        "military": mil_int,
        "dia_atual": int(raw_context.get("dia_atual", raw_context.get("current_day", 1)))
    }

    result = {}

    formula = efeito.get("formula")
    target_resource = efeito.get("recurso", "dinheiro")

    if formula and isinstance(formula, str):
        evaluated = evaluate_formula(formula, normalized_context)
        result[target_resource] = int(round(evaluated))

    for k, v in efeito.items():
        if k in ("formula", "recurso", "aliquota", "descricao_calculo", "tipo"):
            continue
        if isinstance(v, (int, float)):
            result[k] = int(v)
        elif isinstance(v, str) and ("populacao" in v or "felicidade" in v or "+" in v or "*" in v or "/" in v or "-" in v):
            eval_val = evaluate_formula(v, normalized_context)
            result[k] = int(round(eval_val))

    return result
