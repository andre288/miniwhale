from datetime import datetime
from pydantic import BaseModel
from api.models.severity import Severity


class ErrorGroup(BaseModel):
    id: str                     # hash do template
    template: str               # normalized error message
    severity: Severity          # severity of the error group
    count: int
    first_seen: datetime
    last_seen: datetime
    containers: list[str]
    sample_messages: list[str]
