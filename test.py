from transformers import AutoTokenizer
from optimum.onnxruntime import ORTModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("./models/opus-mt-it-en")
model = ORTModelForSeq2SeqLM.from_pretrained("./models/opus-mt-it-en")

# inputs = tokenizer(["Ciao, mi chiamo Simone",
#                    "Sono molto felice di conoscerti!"],
#                    return_tensors="pt", padding=True)
# outputs = model(**inputs)

src_text = [
    "So chi è il mio nemico.",
    "Tom è illetterato; non capisce assolutamente nulla.",
]

# src_text = [
#     "I know who my enemy is.",
#     "Tom is an illiterate; he doesn't understand anything."
# ]

translated = model.generate(**tokenizer(src_text, return_tensors="pt", padding=True))

for t in translated:
    print(tokenizer.decode(t, skip_special_tokens=True))
