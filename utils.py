import spacy

from evaluator_service import EvaluatorService
from schemas import VerifiedEvidenceOutput

evaluator_service = EvaluatorService()
nlp = spacy.load('en_core_web_sm',
                 enable=['tok2vec', 'senter'],
                 config={"nlp": {"disabled": []}})


def split_into_sentences(text):
    sentences = [sent.text for sent in nlp(text).sents]
    # replace end of line with space
    return [' '.join(inp_sent.rsplit('\n')) for inp_sent in sentences]


def evidences_to_verified_evidences(claim: str, evidences, include_title, filter_nei):
    labels, probs = evaluator_service.predict_supports_or_refutes(claim,
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
                                   citation_count=evidence.citation_count,
                                   influential_citation_count=evidence.influential_citation_count,
                                   probability=prob) for evidence, label, prob in zip(evidences, labels, probs)
            if (filter_nei and label != 'NOT_ENOUGH_INFO') or (not filter_nei)]


def map_evidence_doc_to_text(include_title):
    if include_title:
        return lambda evidence: f"{evidence.title}.{evidence.text}"
    else:
        return lambda evidence: evidence.text

