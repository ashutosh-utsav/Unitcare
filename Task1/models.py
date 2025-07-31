from pydantic import BaseModel

class EMRData(BaseModel):
    """
    Pydantic model to validate the structure of the EMR data.
    """
    chief_complaint: str
    history: str
    diagnosis: str
    plan: str