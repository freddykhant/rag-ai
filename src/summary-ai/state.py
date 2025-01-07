import operator
from typing_extensions import TypedDict, Annotated, List

class SummaryState:
  topic : str
  generation: str
  query: str
  loop_step: Annotated[int, operator.add]
  documents: List[str]