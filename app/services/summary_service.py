from fastapi import HTTPException
import re
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import os

# 요약 import
import warnings
from concurrent.futures import ThreadPoolExecutor
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langchain.text_splitter import CharacterTextSplitter
import torch

# 경고 메시지 무시
warnings.filterwarnings("ignore", category=FutureWarning, module='huggingface_hub')

async def textProcessing(texts):
    try: 
        res = texts
        res = process_text(res)
        abstract = res['abstract']
        introduction = extract_key_sentences(res['introduction'])
        conclusion = extract_key_sentences(res['conclusion'])

        res = {"abstract": abstract, "introduction": introduction, "conclusion": conclusion}
        
        return {"resultCode" : 200, "data" : res}
    except Exception as e:
        return {"resultCode": 500, "data": str(e)}

# 전체 텍스트를 초록, 서론, 결론 추출
async def process_text(text):
    try:
        # Define regex patterns for abstract, introduction, and conclusion
        abstract_pattern = re.compile(r'(?i)abstract\s*(.*?)(?=(introduction|1\s*(.*?)Introduction))', re.DOTALL)
        introduction_pattern = re.compile(r'(?i)(introduction|1\sIntroduction)\s*(.*?)(?=\\n\\n2\s)', re.DOTALL)
        conclusion_pattern = re.compile(r'(?i)(conclusion|6\sConclusion)\s*(.*)', re.DOTALL)

        # Find matches
        abstract_match = abstract_pattern.search(text)
        introduction_match = introduction_pattern.search(text)
        conclusion_match = conclusion_pattern.search(text)

        # Extract matched sections
        abstract = abstract_match.group(1).strip() if abstract_match else "Abstract not found."
        introduction = introduction_match.group(2).strip() if introduction_match else "Introduction not found."
        conclusion = conclusion_match.group(2).strip() if conclusion_match else "Conclusion not found."

        response = {
            "abstract": abstract,
            "introduction": introduction,
            "conclusion": conclusion
        }

        return response
    except Exception as e:
        print(f"Error processing text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def extract_key_sentences(text, num_sentences=6):
    sentences = sent_tokenize(text)
    if len(sentences) < num_sentences:
        num_sentences = len(sentences)
    tfidf = TfidfVectorizer().fit_transform(sentences)
    similarity_matrix = cosine_similarity(tfidf, tfidf)
    
    nx_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(nx_graph)
    
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    key_sentences = " ".join([ranked_sentences[i][1] for i in range(num_sentences)])
    return key_sentences

# # Hugging Face 요약 모델 설정
# model_name_en = "facebook/bart-large-cnn"

# model_name_ko = "eenzeenee/t5-base-korean-summarization"
base_dir = os.path.dirname(os.path.abspath(__file__))
print(base_dir)
models_dir = os.path.join(base_dir, "../models")

tokenizer_en_path = os.path.join(models_dir, "facebook_bart-large-cnn_tokenizer")
model_en_path = os.path.join(models_dir, "facebook_bart-large-cnn")
tokenizer_kr_path = os.path.join(models_dir, "facebook_bart-large-cnn_tokenizer")
model_kr_path = os.path.join(models_dir, "facebook_bart-large-cnn")

# 로컬에서 모델과 토크나이저 로드
tokenizer_en = AutoTokenizer.from_pretrained(tokenizer_en_path)
model_en = AutoModelForSeq2SeqLM.from_pretrained(model_en_path)

tokenizer_ko = AutoTokenizer.from_pretrained(tokenizer_kr_path)
model_ko = AutoModelForSeq2SeqLM.from_pretrained(model_kr_path)

async def summarizePaper(texts: dict):
    resultCode = texts["resultCode"]
    if resultCode == 200:
        texts = texts["data"]
    else:
        return {"resultCode": 422, "data": "No content available"}
    
    # 스플리터 지정
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\\n\\n",  # 분할 기준
        chunk_size=2000,   # 청크 사이즈
        chunk_overlap=100, # 중첩 사이즈
    )
    
    combined_summaries = []
    summaries = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        for text in texts:
            split_texts = text_splitter.split_text(text)
            futures = [executor.submit(summarize_paragraph, paragraph) for paragraph in split_texts]
            for future in futures:
                summaries.append(future.result())
    
    combined_summaries.extend(summaries)
    
    if combined_summaries:
        return {"resultCode": 200, "data": combined_summaries}
    else:
        return {"resultCode": 404, "data": "Summarization failed"}
    
async def summarizePdf(texts: str, lang: str):
    # 스플리터 지정
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\\n\\n",  # 분할 기준
        chunk_size=2000,   # 청크 사이즈
        chunk_overlap=100, # 중첩 사이즈
    )
    split_texts = text_splitter.split_text(texts)
    summaries = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        if lang == 'kr':
            summarize_def = summarize_paragraph_ko
        else:
            summarize_def = summarize_paragraph
        futures = [executor.submit(summarize_def, paragraph) for paragraph in split_texts]
        for future in futures:
            summaries.append(future.result())
    
    if summaries:
        return {"resultCode": 200, "data": summaries}
    else:
        return {"resultCode": 404, "data": "Summarization failed"}
    
def summarize_paragraph(paragraph):
    try:
        inputs = tokenizer_en(paragraph, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model_en.generate(inputs["input_ids"], max_length=514, min_length=100, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer_en.decode(summary_ids[0], skip_special_tokens=True)
        print(f"Summary is okey\n")
        return summary
    except Exception as e:
        print(f"Error summarizing paragraph: {e}")
        return paragraph

def summarize_paragraph_ko(paragraph):
    try:
        inputs = tokenizer_ko.encode(paragraph, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model_ko.generate(inputs, max_length=514, no_repeat_ngram_size=3)
        summary = tokenizer_ko.decode(summary_ids[0], skip_special_tokens=True)
        print(f"Summary is okey\n")
        return summary
    except Exception as e:
        print(f"Error summarizing paragraph: {e}")
        return paragraph
    
async def summarize_texts(text, lang):
    try:
        print("Summarizing text: ", len(text))
        if lang == 'kr':
            inputs = tokenizer_ko.encode(text, return_tensors="pt", max_length=514, truncation=True)
            summary_ids = model_ko.generate(inputs)
            summary = tokenizer_ko.decode(summary_ids[0], skip_special_tokens=True)
            print(f"Summary is okey\n")
        else:
            inputs = tokenizer_en(text, return_tensors="pt", max_length=514, truncation=True)
            summary_ids = model_en.generate(inputs["input_ids"], max_length=256, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
            summary = tokenizer_en.decode(summary_ids[0], skip_special_tokens=True)
            print(f"Summary is okey\n")
        return summary
    except Exception as e:
        print(f"Error summarizing paragraph: {e}")
        return text