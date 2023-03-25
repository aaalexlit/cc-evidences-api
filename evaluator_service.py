from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline


class EvaluatorService:
    def __init__(self) -> None:
        self.climate_factcheck_tokenizer = AutoTokenizer.from_pretrained("amandakonet/climatebert-fact-checking")
        self.climate_factcheck_model = AutoModelForSequenceClassification.from_pretrained(
            "amandakonet/climatebert-fact-checking")

        self.climate_factcheck_model.config.id2label = {
            0: "SUPPORTS",
            1: "REFUTES",
            2: "NOT_ENOUGH_INFO"
        }

    def predict_supports_or_refutes(self, claim: str, evidences: [str]) -> ([str], [float]):
        def claim_evidence_pair_data():
            for evidence in evidences:
                yield {"text": claim, "text_pair": evidence}

        pipe = pipeline("text-classification", model=self.climate_factcheck_model,
                        tokenizer=self.climate_factcheck_tokenizer, device=-1,
                        truncation=True, padding=True)
        labels = []
        probs = []
        for out in pipe(claim_evidence_pair_data(), batch_size=1):
            labels.append(out['label'])
            probs.append(out['score'])
        return labels, probs
