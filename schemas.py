from pydantic import BaseModel


class EvidenceOutput(BaseModel):
    num: int
    title: str
    abstract: str
    similarity: float
    doi: str | None
    openalex_id: str | None
    year: int | None


class Claim(BaseModel):
    claim: str
    threshold: float | None
    top_k: int | None

    class Config:
        schema_extra = {
            "example": {
                "claim": "A belt of vulnerable, poor countries around the equator will probably be hit hardest , "
                         "even though many did not enjoy the economic benefits of burning fossil fuels for energy",
                "threshold": 0.7,
                "top_k": 10
            }
        }
