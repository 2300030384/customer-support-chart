from fastapi import APIRouter, HTTPException
from app.services.escalation_rule_service import create_rule, get_rules, update_rule, delete_rule

router = APIRouter(tags=["EscalationRules"], prefix="/escalation-rules")

@router.post("")
def add_rule(rule: dict):
    return create_rule(rule)

@router.get("")
def list_rules():
    return get_rules()

@router.put("/{rule_id}")
def edit_rule(rule_id: str, updates: dict):
    update_rule(rule_id, updates)
    return {"status": "updated"}

@router.delete("/{rule_id}")
def remove_rule(rule_id: str):
    delete_rule(rule_id)
    return {"status": "deleted"}
