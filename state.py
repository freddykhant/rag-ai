import operator
from typing_extensions import TypedDict, Annotated, List
from dataclasses import dataclass, field

class SummaryState(TypedDict):
  topic : str 
  generation: str 
  query: str 
  loop_step: Annotated[int, operator.add] 
  documents: List[str] 

class SummaryStateInput(TypedDict):
  topic : str 