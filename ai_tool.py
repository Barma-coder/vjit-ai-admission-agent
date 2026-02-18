import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from memory_tool import get_history_string, save_history

# Load variables from .env
load_dotenv()

# Initialize the Gemini Client using the .env key
# Version 2.5-flash as per your preference
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def analyze_student_query(user_query, brochure_text):
    """
    Intuitively analyzes the query. 
    High confidence (>=0.8) triggers Gmail.
    Low confidence (<0.8) triggers a concise WhatsApp alert.
    """
    chat_history = get_history_string()
    
    system_prompt = f"""
    You are the Intelligent Admission Agent for VJIT. 
    
    ### KNOWLEDGE SOURCE:
    {brochure_text}
    
    ### CONTEXTUAL MEMORY:
    {chat_history}

    ### INTUITIVE RULES:
    1. **Domain Evaluation**: If the query is about food, jokes, or non-college topics, set "confidence_score": 0.0.
    2. **Evidence Requirement**: Set "confidence_score": 1.0 ONLY if the brochure explicitly answers the question.
    3. **WhatsApp Constraints**: If the information is missing (score < 0.8), keep the "answer" field under 1000 characters. 
       Summarize what was asked and why it couldn't be answered so the human admin can read it quickly.
    4. **Email Constraint**: If score is 1.0, provide a professional email draft.

    Return ONLY valid JSON with keys: "confidence_score", "answer", and "reason".
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=f"{system_prompt}\n\nStudent Query: {user_query}",
            config=types.GenerateContentConfig(
                response_mime_type='application/json',
            )
        )
        
        # Safe JSON parsing
        result = json.loads(response.text)
        
        # Logic to save to memory only for valid institutional answers
        if result.get('confidence_score', 0) >= 0.8:
            save_history(user_query, result.get('answer', ''))
        
        return result

    except Exception as e:
        print(f"AI Tool Error: {e}")
        return {
            "answer": "Error: The AI could not process this query.",
            "confidence_score": 0.0,
            "reason": str(e)
        }