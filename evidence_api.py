import uvicorn
from fastapi import FastAPI

from retriever_service import RetrieverService
from schemas import Claim, EvidenceOutput, VerifiedEvidenceOutput, Claims, TextToSplit

from utils import split_into_sentences, evidences_to_verified_evidences

app = FastAPI(title="Evidence retrieval")
abstract_retriever_service = RetrieverService.get_abstract_retriever()
phrase_retriever_service = RetrieverService.get_phrase_retriever()


@app.post("/api/abstract/evidence", response_model=list[EvidenceOutput])
def get_evidences(claim: Claim, re_rank: bool | None = True) -> list[EvidenceOutput]:
    """Get top_k relevant evidence abstracts from scientific articles"""
    return abstract_retriever_service.find_relevant_evidences(claim.claim, claim.top_k, claim.threshold,
                                                              re_rank=re_rank)


@app.post("/api/abstract/evidence/batch", response_model=list[list[EvidenceOutput]])
def get_evidences(claims: Claims, re_rank: bool | None = True) -> list[list[EvidenceOutput]]:
    """Get top_k relevant evidence abstracts from scientific articles"""
    return abstract_retriever_service.find_relevant_evidences_batch(claims.claims,
                                                                    claims.top_k,
                                                                    claims.threshold,
                                                                    re_rank=re_rank)


@app.post("/api/phrase/evidence", response_model=list[EvidenceOutput])
def get_evidences(claim: Claim, re_rank: bool | None = True) -> list[EvidenceOutput]:
    """Get top_k relevant evidence phrases from scientific articles"""
    return phrase_retriever_service.find_relevant_evidences(claim.claim,
                                                            claim.top_k,
                                                            claim.threshold,
                                                            re_rank=re_rank)


@app.post("/api/phrase/evidence/batch", response_model=list[list[EvidenceOutput]])
def get_evidences(claims: Claims, re_rank: bool | None = True) -> list[list[EvidenceOutput]]:
    """Get top_k relevant evidence phrases from scientific articles"""
    return phrase_retriever_service.find_relevant_evidences_batch(claims.claims,
                                                                  claims.top_k,
                                                                  claims.threshold,
                                                                  re_rank=re_rank)


@app.post("/api/phrase/verify")
def verify(claim: Claim,
           include_title: bool | None = True,
           re_rank: bool | None = True,
           filter_nei: bool | None = True) -> list[VerifiedEvidenceOutput]:
    """Verify claim against phrases extracted from scientific paper abstracts"""
    evidences = phrase_retriever_service.find_relevant_evidences(claim.claim, claim.top_k,
                                                                 claim.threshold, re_rank=re_rank)
    # Important: validation is against evidence article title + evidence article phrase by default
    return evidences_to_verified_evidences(claim.claim, evidences, include_title, filter_nei)


@app.post("/api/phrase/verify/batch")
def verify(claims: Claims,
           include_title: bool | None = True,
           re_rank: bool | None = True,
           filter_nei: bool | None = True) -> list[list[VerifiedEvidenceOutput]]:
    """Verify claim against phrases extracted from scientific paper abstracts"""
    evidences_list = phrase_retriever_service.find_relevant_evidences_batch(claims.claims,
                                                                            claims.top_k,
                                                                            claims.threshold,
                                                                            re_rank=re_rank)
    # Important: validation is against evidence article title + evidence article phrase by default
    return [evidences_to_verified_evidences(claim, evidences, include_title, filter_nei)
            for claim, evidences in zip(claims.claims, evidences_list)]


@app.post("/api/abstract/verify")
def verify(claim: Claim,
           include_title: bool | None = True,
           re_rank: bool | None = True,
           filter_nei: bool | None = True) -> list[VerifiedEvidenceOutput]:
    """Verify claim against phrases extracted from scientific paper abstracts"""
    evidences = abstract_retriever_service.find_relevant_evidences(claim.claim,
                                                                   claim.top_k,
                                                                   claim.threshold,
                                                                   re_rank=re_rank)
    separated_evidences = [EvidenceOutput(num=ev.num,
                                          title=ev.title,
                                          text=phrase,
                                          similarity=ev.similarity,
                                          doi=ev.doi,
                                          openalex_id=ev.openalex_id,
                                          year=ev.year,
                                          citation_count=ev.citation_count,
                                          influential_citation_count=ev.influential_citation_count,
                                          ) for ev in evidences for phrase in split_into_sentences(ev.text)]
    # Important: validation is against evidence article title + evidence article phrase by default
    return evidences_to_verified_evidences(claim.claim, separated_evidences, include_title, filter_nei)


@app.post("/api/abstract/verify/batch")
def verify(claims: Claims,
           include_title: bool | None = True,
           re_rank: bool | None = True,
           filter_nei: bool | None = True) -> list[list[VerifiedEvidenceOutput]]:
    """Verify claim against phrases extracted from scientific paper abstracts"""
    evidences_list = abstract_retriever_service.find_relevant_evidences_batch(claims.claims,
                                                                              claims.top_k,
                                                                              claims.threshold,
                                                                              re_rank=re_rank)
    res = []
    for claim, evidences in zip(claims.claims, evidences_list):
        separated_evidences = [EvidenceOutput(num=ev.num,
                                              title=ev.title,
                                              text=phrase,
                                              similarity=ev.similarity,
                                              doi=ev.doi,
                                              openalex_id=ev.openalex_id,
                                              year=ev.year,
                                              citation_count=ev.citation_count,
                                              influential_citation_count=ev.influential_citation_count,
                                              ) for ev in evidences for phrase in split_into_sentences(ev.text)]
        # Important: validation is against evidence article title + evidence article phrase by default
        res.append(evidences_to_verified_evidences(claim, separated_evidences, include_title, filter_nei))

    return res


@app.post("/api/split")
def split(text: TextToSplit) -> list[str]:
    return split_into_sentences(text.text)


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
