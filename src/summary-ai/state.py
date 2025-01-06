import operator
from typing_extensions import TypedDict, Annotated, List

class SummaryState:
  generation: str
  query: str
  max_retries: int
  loop_step: Annotated[int, operator.add]
  documents: List[str]