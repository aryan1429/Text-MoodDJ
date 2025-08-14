from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
import torch

_MODEL = None
_PIPE = None
_LABELS = None

def load_model():
    global _MODEL, _PIPE, _LABELS
    if _PIPE is None:
        name = "j-hartmann/emotion-english-distilroberta-base"
        _MODEL = AutoModelForSequenceClassification.from_pretrained(name)
        tok = AutoTokenizer.from_pretrained(name)
        _PIPE = TextClassificationPipeline(model=_MODEL, tokenizer=tok, framework="pt", top_k=None, return_all_scores=True)
        _LABELS = [l for l in _MODEL.config.id2label.values()]
    return _PIPE, _LABELS

def analyze_emotion(text: str):
    pipe, labels = load_model()
    outs = pipe(text)[0]  # list of {label, score}
    # pick top
    top = max(outs, key=lambda x: x["score"])
    return top["label"].lower(), float(top["score"])
