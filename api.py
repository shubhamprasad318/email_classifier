from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from utils import mask_pii, demask_pii
from models import classify_email_text

class EmailInput(BaseModel):
    email_body: str

class MaskedEntity(BaseModel):
    position: List[int]
    classification: str
    entity: str

class ClassificationOutput(BaseModel):
    input_email_body: str
    list_of_masked_entities: List[MaskedEntity]
    masked_email: str
    category_of_the_email: str

app = FastAPI(title="Support Email Classifier")

@app.post("/classify-email", response_model=ClassificationOutput)
async def classify_email(request: EmailInput):
    original_text = request.email_body

    # Mask PII
    masked_email, entities, pii_data = mask_pii(original_text)

    # Classify
    category = classify_email_text(masked_email)

    # Demask back to original
    demasked_email = demask_pii(masked_email, pii_data)

    return {
        "input_email_body": original_text,
        "list_of_masked_entities": entities,
        "masked_email": masked_email,
        "category_of_the_email": category
    }