from pathlib import Path
from retriever import FAISSIndexer
from schemas import EvidenceOutput

MODEL_NAME = 'sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco'
EMBEDDING_DIM = 768
# TODO needs to be changed to dot_product
SIMILARITY = 'cosine'
BASE_DIR = Path(__file__).resolve(strict=True).parent


class RetrieverService:

    def __init__(self) -> None:
        self.faiss_indexer = FAISSIndexer(f'{BASE_DIR}/data/', MODEL_NAME, EMBEDDING_DIM, SIMILARITY)

    def find_relevant_evidences(self, claim: str, top_k: int = 10, threshold: float = None) -> list[EvidenceOutput]:
        evidences = self.faiss_indexer.retrieve_matches_for_a_phrase(claim, top_k)
        result = []
        for i, evidence_doc in enumerate(evidences):
            similarity = evidence_doc.score
            if (threshold and similarity > threshold) or (not threshold):
                res_evidence = EvidenceOutput(num=i + 1, similarity=similarity,
                                              title=evidence_doc.meta.get("title", ""),
                                              abstract=evidence_doc.content,
                                              doi=evidence_doc.meta.get("doi", None),
                                              openalex_id=evidence_doc.meta.get("open_alex_id", None),
                                              year=evidence_doc.meta.get("publication_year", None))
                result.append(res_evidence)
        return result


if __name__ == '__main__':
    retriever_service = RetrieverService()
    res = retriever_service.find_relevant_evidences(
        "A belt of vulnerable, poor countries around the equator will probably be hit hardest , "
        "even though many did not enjoy the economic benefits of burning fossil fuels for energy",
        threshold=0.92)
    for evidence in res:
        print(evidence)
