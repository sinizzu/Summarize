from fastapi import HTTPException
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from app.db.connect_db import get_weaviate_client
from weaviate.classes.query import Filter
import re

client = get_weaviate_client()
documentCollection = client.collections.get("Document")

def summaryPaper(texts):
    try: 
        res = texts
        res = process_text(res)
        return {"resultCode" : 200, "data" : res}
    except Exception as e:
        return {"resultCode": 500, "data": str(e)}

# 전체 텍스트를 초록, 서론, 결론 추출
def process_text(text):
    try:
        # Define regex patterns for abstract, introduction, and conclusion
        abstract_pattern = re.compile(r'(?i)abstract\s*(.*?)(?=(introduction|1\sIntroduction))', re.DOTALL)
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

def extract_key_sentences(text, num_sentences=7):
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