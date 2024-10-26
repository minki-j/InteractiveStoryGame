from pydantic import BaseModel, Field
from typing import List

class WriterAgentState(BaseModel):
    previous_story: str = Field(default="")
    
