from pydantic import BaseModel, Field
from typing import Dict

class PredictionResponse(BaseModel):
    predicted_category: int = Field(..., 
                                    description="The predicted attrition of employee", 
                                    example="0")
    confidence: float = Field(..., 
                              description="Model's confidence score (0 to 1)", 
                              example=0.855)
    class_probabilities: Dict[str, float] = Field(..., 
                                                  description="Probability distribution amoung different classes", 
                                                  example= {"0" : 0.15, "1" : 0.85})

    

