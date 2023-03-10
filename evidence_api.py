import uvicorn
from fastapi import FastAPI

from retriever_service import RetrieverService
from schemas import Claim, EvidenceOutput

app = FastAPI(title="Evidence retrieval")
retriver_service = RetrieverService()


#
# @app.on_event("startup")
# def on_startup():
#     retriver_service = utils.RetrieverService()

# @app.post("/api/evidence", response_model=Evidence)
@app.post("/api/evidence", response_model=list[EvidenceOutput])
def get_evidences(claim: Claim) -> list[EvidenceOutput]:
    """Get top_k scientific evidences to a claim"""
    return retriver_service.find_relevant_evidences(claim.claim, claim.top_k, claim.threshold)


@app.get("/healthcheck")
def healthcheck():
    return


if __name__ == "__main__":
    uvicorn.run("evidence_api:app", reload=True)
