from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def remove_json_formatting(text: str) -> str:
    if text.startswith("```json"):
        text = text[7:]
    if text.endswith("```"):
        text = text[:-3]
    return text

def remove_text_formatting(text: str) -> str:
    if text.startswith("..."):
        text = text[3:]
    return text

def check_json(text: str):
    for item in text:
        if not (isinstance(item, dict) and set(item.keys()) == {'front', 'back'}):
            raise ValueError('Invalid JSON format')

def check_similarity(input: str, output: str, threshold=0.1):
    if output != "''":
        tfidf=TfidfVectorizer()
        matrix=tfidf.fit_transform([input, output])
        score = cosine_similarity(matrix[0], matrix[1])[0][0]
        if score < threshold:
            raise ValueError('Incorrect Output')