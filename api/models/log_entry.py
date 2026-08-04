class LogEntry(BaseModel):
    container: str
    timestamp: datetime
    severity: Severity        # enum: info | warning | error | critical
    message: str               # primeira linha, usada pro agrupamento
    raw: str                   # texto original completo (pode ter várias linhas)
    source_format: str         # "json" | "loguru" | "winston" | "plaintext"

