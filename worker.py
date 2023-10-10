from celery import Celery
from transformers import AutoTokenizer
from optimum.onnxruntime import ORTModelForSeq2SeqLM

from constants import SupportedLanguages


english_to_italian = ORTModelForSeq2SeqLM.from_pretrained("./models/opus-mt-en-it")
english_to_italian_tokenizer = AutoTokenizer.from_pretrained("./models/opus-mt-en-it")

italian_to_english = ORTModelForSeq2SeqLM.from_pretrained("./models/opus-mt-it-en")
italian_to_english_tokenizer = AutoTokenizer.from_pretrained("./models/opus-mt-it-en")

app = Celery("tasks", backend="rpc://", broker="pyamqp://username:password@localhost/")


@app.task
def translate(
    source_language: SupportedLanguages, target_language: SupportedLanguages, text: str
):
    if (
        source_language == SupportedLanguages.ITALIAN
        and target_language == SupportedLanguages.ENGLISH
    ):
        translated = italian_to_english.generate(
            **italian_to_english_tokenizer(text, return_tensors="pt", padding=True)
        )
        return italian_to_english_tokenizer.decode(translated, skip_special_tokens=True)
    if (
        source_language == SupportedLanguages.ENGLISH
        and target_language == SupportedLanguages.ITALIAN
    ):
        translated = english_to_italian.generate(
            **english_to_italian_tokenizer(text, return_tensors="pt", padding=True)
        )
        return english_to_italian_tokenizer.decode(translated, skip_special_tokens=True)
    return text
