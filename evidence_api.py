import uvicorn
from fastapi import FastAPI

from evaluator_service import EvaluatorService
from retriever_service import RetrieverService
from schemas import Claim, EvidenceOutput, VerifiedEvidenceOutput

import nltk

app = FastAPI(title="Evidence retrieval")
abstract_retriever_service = RetrieverService.get_abstract_retriever()
phrase_retriever_service = RetrieverService.get_phrase_retriever()
evaluator_service = EvaluatorService()


def map_evidence_doc_to_text(include_title):
    if include_title:
        return lambda evidence: f"{evidence.title}.{evidence.text}"
    else:
        return lambda evidence: evidence.text


@app.on_event("startup")
def on_startup():
    nltk.download('punkt')


@app.post("/api/abstract/evidence", response_model=list[EvidenceOutput])
def get_evidences(claim: Claim) -> list[EvidenceOutput]:
    """Get top_k relevant evidence abstracts from scientific articles"""
    return abstract_retriever_service.find_relevant_evidences(claim.claim, claim.top_k, claim.threshold)


@app.post("/api/phrase/evidence", response_model=list[EvidenceOutput])
def get_evidences(claim: Claim) -> list[EvidenceOutput]:
    """Get top_k relevant evidence phrases from scientific articles"""
    return phrase_retriever_service.find_relevant_evidences(claim.claim, claim.top_k, claim.threshold)


@app.post("/api/phrase/verify")
def verify(claim: Claim, include_title: bool | None = True) -> list[VerifiedEvidenceOutput]:
    """Verify claim against phrases extracted from scientific paper abstracts"""
    evidences = phrase_retriever_service.find_relevant_evidences(claim.claim, claim.top_k, claim.threshold)
    # Important validation is against evidence article title + evidence article phrase
    labels, probs = evaluator_service.predict_supports_or_refutes(claim.claim,
                                                                  list(map(map_evidence_doc_to_text(include_title),
                                                                           evidences)))
    return [VerifiedEvidenceOutput(num=evidence.num,
                                   title=evidence.title,
                                   text=evidence.text,
                                   similarity=evidence.similarity,
                                   doi=evidence.doi,
                                   openalex_id=evidence.openalex_id,
                                   year=evidence.year,
                                   label=label,
                                   probability=prob) for evidence, label, prob in zip(evidences, labels, probs)]


@app.post("/api/abstract/verify")
def verify(claim: Claim, include_title: bool | None = True) -> list[VerifiedEvidenceOutput]:
    """Verify claim against phrases extracted from scientific paper abstracts"""
    evidences = abstract_retriever_service.find_relevant_evidences(claim.claim, claim.top_k, claim.threshold)
    separated_evidences = [EvidenceOutput(num=ev.num,
                                          title=ev.title,
                                          text=phrase,
                                          similarity=ev.similarity,
                                          doi=ev.doi,
                                          openalex_id=ev.openalex_id,
                                          year=ev.year
                                          ) for ev in evidences for phrase in nltk.sent_tokenize(ev.text)]
    # Important: validation is against evidence article title + evidence article phrase by default
    labels, probs = evaluator_service.predict_supports_or_refutes(claim.claim,
                                                                  list(map(map_evidence_doc_to_text(include_title),
                                                                           separated_evidences)))
    return [VerifiedEvidenceOutput(num=evidence.num,
                                   title=evidence.title,
                                   text=evidence.text,
                                   similarity=evidence.similarity,
                                   doi=evidence.doi,
                                   openalex_id=evidence.openalex_id,
                                   year=evidence.year,
                                   label=label,
                                   probability=prob) for evidence, label, prob in
            zip(separated_evidences, labels, probs)]


@app.get("/healthcheck")
def healthcheck() -> str:
    return "Seems to be running"


@app.get("/")
def readme() -> str:
    return "An API for scientific evidence retrieval and climate change related claim verification against " \
           "scientific evidence"


if __name__ == "__main__":
    # claim = Claim(claim="co2 is not the cause of global warming",
    #               top_k=10,
    #               threshold=0.7)
    # print(verify(claim))
    uvicorn.run("evidence_api:app", reload=True)
