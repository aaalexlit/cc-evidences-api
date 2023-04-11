from pathlib import Path
from retriever import FAISSIndexer
from schemas import EvidenceOutput

ABSTRACT_MODEL_NAME = 'sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco'
PHRASE_MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'

BASE_DIR = Path(__file__).resolve(strict=True).parent


class RetrieverService:

    def __init__(self, model_name: str, db_folder_name: str) -> None:
        self.faiss_indexer = FAISSIndexer(f'{BASE_DIR}/data/{db_folder_name}/', model_name)

    @classmethod
    def get_phrase_retriever(cls):
        return cls(PHRASE_MODEL_NAME, 'phrase')

    @classmethod
    def get_abstract_retriever(cls):
        return cls(ABSTRACT_MODEL_NAME, 'abstract')

    def find_relevant_evidences(self, claim: str,
                                top_k: int = 10,
                                threshold: float = None,
                                re_rank: bool = True) -> list[EvidenceOutput]:
        evidences = self.faiss_indexer.retrieve_matches_for_a_phrase(claim, top_k=top_k + 5)
        return self.format_evidences(evidences, re_rank, threshold, top_k)

    def format_evidences(self, evidences, re_rank, threshold, top_k):
        result = []
        for i, evidence_doc in enumerate(evidences):
            similarity = evidence_doc.score
            if (threshold and similarity > threshold) or (not threshold):
                res_evidence = self.convert_docs_to_evidence_output(evidence_doc, i, similarity)
                result.append(res_evidence)
        if re_rank:
            RetrieverService.re_rank_evidences(result)
        return result[:top_k]

    @staticmethod
    def re_rank_evidences(evidences_list: [EvidenceOutput]):
        evidences_list.sort(key=lambda ev: (ev.influential_citation_count if ev.influential_citation_count else 0,
                                            ev.citation_count if ev.citation_count else 0,
                                            ev.year), reverse=True)

    @staticmethod
    def convert_docs_to_evidence_output(evidence_doc, i, similarity):
        res_evidence = EvidenceOutput(num=i + 1, similarity=similarity,
                                      title=evidence_doc.meta.get("title", ""),
                                      text=evidence_doc.content,
                                      doi=evidence_doc.meta.get("doi", None),
                                      openalex_id=evidence_doc.meta.get("openalex_id", None),
                                      year=evidence_doc.meta.get("year", None),
                                      )
        citation_count_str = evidence_doc.meta.get("citation_count", None)
        if citation_count_str is not None and citation_count_str is not '':
            res_evidence.citation_count = int(citation_count_str)
        infl_citation_count_str = evidence_doc.meta.get(
                                          "influential_citation_count", None)
        if infl_citation_count_str is not None and infl_citation_count_str is not '':
            res_evidence.influential_citation_count = int(infl_citation_count_str)
        return res_evidence

    def find_relevant_evidences_batch(self, claims: [str],
                                      top_k: int = 10,
                                      threshold: float = None,
                                      re_rank: bool = True) -> list[list[EvidenceOutput]]:
        all_evidences = self.faiss_indexer.retrieve_matches_for_phrases(claims, top_k + 5)
        return [self.format_evidences(evidences, re_rank, threshold, top_k) for evidences in all_evidences]


if __name__ == '__main__':
    retriever_service = RetrieverService.get_phrase_retriever()
    res = retriever_service.find_relevant_evidences(
        "A belt of vulnerable, poor countries around the equator will probably be hit hardest , "
        "even though many did not enjoy the economic benefits of burning fossil fuels for energy",
        threshold=0.6)
    for evidence in res:
        print(evidence)
