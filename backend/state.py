import operator
from typing_extensions import TypedDict, Annotated, List
from dataclasses import dataclass, field

@dataclass(kw_only=True)
class SummaryState(TypedDict):
  filename : str = field(default=None)
  generation: str = field(default=None)
  documents: List[str] = field(default_factory=list)