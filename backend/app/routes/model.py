from fastapi import APIRouter
from app.services.early_warning import train_classifier_from_conversations

router = APIRouter()

@router.post("/model/retrain")
def retrain_model():
    try:
        result = train_classifier_from_conversations()
        return {"status": "success", "details": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}
