import operator
from typing_extensions import TypedDict, Annotated, List
from dataclasses import dataclass, field

@dataclass(kw_only=True)
class SummaryState:
  topic : str = field(default="None")
  generation: str = field(default="None")
  query: str = field(default="None")
  loop_step: Annotated[int, operator.add] = field(default_factory=list)
  documents: List[str] = field(default_factory=list)

@dataclass(kw_only=True)
class SummaryStateInput(TypedDict):
  topic : str = field(default="None")