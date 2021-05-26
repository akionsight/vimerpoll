# This file houses pydantic models 

from pydantic import BaseModel
from typing import List
import pydantic


class Poll(BaseModel):
    poll_question: str
    poll_options: List[str]
