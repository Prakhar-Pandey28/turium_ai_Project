from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()  # load API keys from .env file

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_llm(context, question):
    """
    Sends context + question to Groq's LLM
    Using llama-3.3-70b-versatile (the old model got deprecated)
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # current model as of 2026
        messages=[
            {"role": "system", "content": "Answer using the context. If answer is not in context, say I don't know"},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
        ]
    )
    
    return response.choices[0].message.content