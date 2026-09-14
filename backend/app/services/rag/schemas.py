from typing import Literal

from pydantic import BaseModel, Field


class RiskFinding(BaseModel):

    category: Literal[
        "Risk",
        "Fee",
        "Restriction",
        "Important Clause"
    ]

    title: str

    severity: Literal[
        "Low",
        "Medium",
        "High"
    ]

    explanation: str

    page_number: int

    evidence: str


class AnalysisResult(BaseModel):

    overall_risk: Literal[
        "Low",
        "Medium",
        "High"
    ]

    summary: str

    findings: list[RiskFinding] = Field(
        default_factory=list
    )