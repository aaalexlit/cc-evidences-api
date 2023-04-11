from pydantic import BaseModel
from pydantic.schema import Literal


class EvidenceOutput(BaseModel):
    num: int
    title: str
    text: str
    similarity: float | None
    doi: str | None
    openalex_id: str | None
    year: int | None
    citation_count: int | None
    influential_citation_count: int | None


class VerifiedEvidenceOutput(EvidenceOutput):
    label: Literal['SUPPORTS', 'REFUTES', 'NOT_ENOUGH_INFO']
    probability: float


class BaseClaim(BaseModel):
    threshold: float | None
    top_k: int | None


class Claim(BaseClaim):
    claim: str

    class Config:
        schema_extra = {
            "example": {
                "claim": "There is no climate emergency",
                "threshold": 0.7,
                "top_k": 10
            }
        }


class Claims(BaseClaim):
    claims: list[str]

    class Config:
        schema_extra = {
            "example": {
                "claims": ["CO2 is not the cause of our current warming trend.",
                           "Natural variation explains a substantial part of global warming observed since 1850"],
                "threshold": 0.6,
                "top_k": 10
            }
        }


class TextToSplit(BaseModel):
    text: str

    class Config:
        schema_extra = {
            "example": {
                "text": "There is no climate emergency. OPINION: The science and data strongly support that our "
                        "planet’s ecosystems are thriving and that humanity is benefiting from modestly increasing "
                        "temperature and an increase in carbon dioxide. These facts refute the claim that Earth is "
                        "spiraling into one man-made climate catastrophe after another. Carbon dioxide (CO2) is "
                        "portrayed as a demon molecule fueling run-away greenhouse warming. If you get your news "
                        "only from mainstream media, you would likely believe that CO2 levels are dangerously "
                        "high and unprecedented. You would be wrong. Concentrations of this gas are slightly "
                        "less than 420 parts-per-million (ppm), or one-sixth the average historic levels of "
                        "2,600 ppm for the last 600 million years. Increases in carbon dioxide in the last "
                        "150 years, largely from the burning of fossil fuels, have reversed a dangerous downward "
                        "trend in the gas’ concentration. During the last glacial period, concentrations nearly "
                        "reached the “line of death” at 150 parts per million, below which plants die. Viewed in the "
                        "long-term geologic context, we are actually CO2 impoverished."
            }
        }
