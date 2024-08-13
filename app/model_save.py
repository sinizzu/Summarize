from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name_en = "facebook/bart-large-cnn"
model_name_ko = "eenzeenee/t5-base-korean-summarization"

# 모델과 토크나이저를 로컬 디스크에 저장
tokenizer_en = AutoTokenizer.from_pretrained(model_name_en)
model_en = AutoModelForSeq2SeqLM.from_pretrained(model_name_en)

tokenizer_ko = AutoTokenizer.from_pretrained(model_name_ko)
model_ko = AutoModelForSeq2SeqLM.from_pretrained(model_name_ko)

# 로컬 디스크에 저장
tokenizer_en.save_pretrained("./models/facebook_bart-large-cnn_tokenizer")
model_en.save_pretrained("./models/facebook_bart-large-cnn")

tokenizer_ko.save_pretrained("./models/t5-base-korean-summarization_tokenizer")
model_ko.save_pretrained("./models/t5-base-korean-summarization")
