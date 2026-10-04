from typing import Literal

from pydantic import BaseModel, Field

Severity = Literal["Low", "Medium", "High"]


class RiskFinding(BaseModel):
    category: Literal["Risk", "Fee", "Restriction", "Important Clause"]
    title: str
    severity: Severity
    explanation: str
    page_number: int
    evidence: str


class AnalysisResult(BaseModel):
    overall_risk: Severity
    summary: str
    findings: list[RiskFinding] = Field(default_factory=list)
