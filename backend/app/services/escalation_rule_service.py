from app.models.escalation_rule import EscalationRule
from app.database.connection import get_database

# CRUD for escalation rules
def create_rule(rule_data):
    db = get_database()
    rule = EscalationRule(**rule_data)
    db["escalation_rules"].insert_one(rule.dict(by_alias=True, exclude_none=True))
    return rule

def get_rules():
    db = get_database()
    rules = list(db["escalation_rules"].find({"enabled": True}))
    return [EscalationRule(**r) for r in rules]

def update_rule(rule_id, updates):
    db = get_database()
    db["escalation_rules"].update_one({"_id": rule_id}, {"$set": updates})

def delete_rule(rule_id):
    db = get_database()
    db["escalation_rules"].delete_one({"_id": rule_id})
