from groq import Groq
import os
import time
from dotenv import load_dotenv
from llm.prompt_templates import FINANCIAL_SYSTEM_PROMPT, build_rag_prompt

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=api_key)
MODEL = "llama-3.3-70b-versatile"


def generate_answer(query, context, sources):
    prompt = build_rag_prompt(query, context, sources)
    
    start_time = time.time()
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": FINANCIAL_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=1500
        )
        latency = round(time.time() - start_time, 2)
        
        return {
            "answer": response.choices[0].message.content,
            "latency": latency,
            "sources": sources,
            "success": True
        }
    
    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "latency": 0,
            "sources": sources,
            "success": False
        }


def compute_confidence(sources):
    if not sources:
        return 0
    companies = set(s["company"] for s in sources)
    years = set(s["year"] for s in sources)
    base = min(len(sources) / 5, 1.0) * 60
    company_bonus = len(companies) * 10
    year_bonus = len(years) * 5
    return min(int(base + company_bonus + year_bonus), 97)


if __name__ == "__main__":
    from rag.retriever import retrieve_context
    
    query = "How did Apple revenue change between 2023 and 2025?"
    print(f"Query: {query}")
    print("Retrieving context...")
    
    context, sources = retrieve_context(query)
    print(f"Retrieved {len(sources)} sources")
    
    print("Generating answer...")
    result = generate_answer(query, context, sources)
    
    print(f"\nAnswer:\n{result['answer']}")
    print(f"\nLatency: {result['latency']}s")
    print(f"Confidence: {compute_confidence(sources)}%")