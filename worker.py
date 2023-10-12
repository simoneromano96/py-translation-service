from celery import Celery
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from optimum.onnxruntime import ORTModelForSeq2SeqLM
from constants import SupportedLanguages
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
logger.info("Initialising worker")

english_to_italian = ORTModelForSeq2SeqLM.from_pretrained("./models/opus-mt-en-it")
# english_to_italian = AutoModelForSeq2SeqLM.from_pretrained("./models/opus-mt-en-it")
english_to_italian_tokenizer = AutoTokenizer.from_pretrained("./models/opus-mt-en-it")

italian_to_english = ORTModelForSeq2SeqLM.from_pretrained("./models/opus-mt-it-en")
# italian_to_english = AutoModelForSeq2SeqLM.from_pretrained("./models/opus-mt-it-en")
italian_to_english_tokenizer = AutoTokenizer.from_pretrained("./models/opus-mt-it-en")

app = Celery(
    "tasks",
    backend="rpc://",
    broker="pyamqp://username:password@localhost/",
    broker_connection_retry_on_startup=True,
)


@app.task
def translate(
    source_language: SupportedLanguages, target_language: SupportedLanguages, text: str
):
    logger.info("Received task")
    if (
        source_language == SupportedLanguages.ITALIAN
        and target_language == SupportedLanguages.ENGLISH
    ):
        translated = italian_to_english.generate(
            **italian_to_english_tokenizer([text], return_tensors="pt", padding=True)
        )
        result = ""
        for token in translated:
            result += italian_to_english_tokenizer.decode(
                token, skip_special_tokens=True
            )
        return result
    if (
        source_language == SupportedLanguages.ENGLISH
        and target_language == SupportedLanguages.ITALIAN
    ):
        translated = english_to_italian.generate(
            **english_to_italian_tokenizer([text], return_tensors="pt", padding=True)
        )
        result = ""
        for token in translated:
            result += english_to_italian_tokenizer.decode(
                token, skip_special_tokens=True
            )
        return result
    return text
