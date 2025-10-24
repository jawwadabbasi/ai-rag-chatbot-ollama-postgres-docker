import re, os

from includes.db import Db
from includes.models import Documents
from services.ollama import Ollama

class Handler:
    
    def Retrieve(question, k=5, min_cosine=0.25):

        question_vector = Ollama.Embed(question)
        
        query = """
            SELECT content, 1 - (embedding <=> %s::vector) AS cosine
            FROM public.documents
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """

        inputs = (
            question_vector, 
            question_vector, 
            k
        )

        result = Db.ExecuteQuery(query,inputs ) or []

        # Keyword re-rank
        for r in result:
            r["boost"] = Handler.KeywordScore(r["content"], question)

        result.sort(key=lambda x: (x["boost"], x["cosine"]), reverse=True)

        # Filter out weak matches
        filtered = [r for r in result if r["cosine"] >= min_cosine]

        # Return just the text chunks the generator will see
        return "\n\n".join([r["content"] for r in filtered[:k]])
    
    def ChunkTextSmart(text):

        sections = re.split(r"(?=\n\d+\.\s[A-Z ]+|\nQ\d+:)", text)
        return [s.strip() for s in sections if s.strip()]
    
    def KeywordScore(text, query):
        
        q_terms = set(re.findall(r'\w+', query.lower()))
        t_terms = set(re.findall(r'\w+', text.lower()))
        
        return len(q_terms & t_terms)

    def Injest():

        DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
        DATA_DIR = os.path.abspath(DATA_DIR)

        with Db.SessionScope() as session:

            for file in os.listdir(DATA_DIR):
                if not file.endswith((".txt", ".md")):
                    continue

                path = os.path.join(DATA_DIR, file)
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()

                chunks = Handler.ChunkTextSmart(text)
                for chunk in chunks:
                    emb = Ollama.Embed(chunk)

                    document = Documents(
                        title=file,
                        content=chunk,
                        embedding=emb
                    )
                    
                    session.add(document)

        return True