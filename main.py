import os
from dotenv import load_dotenv
from ai_tool import analyze_student_query
from drive_tool import download_brochure
from pdf_tool import extract_text_from_pdf
from gmail_tool import create_gmail_draft
from twilio_tool import send_whatsapp_alert 
from logging_tool import log_transaction 

load_dotenv()
BROCHURE_FILE_ID = os.getenv("BROCHURE_FILE_ID")

def run_agentic_workflow(user_query):
    """
    Main Logic Engine:
    1. Fetches Brochure
    2. Extracts Text
    3. AI Reasoning
    4. Executes Action (Gmail/WhatsApp)
    5. Logs Transaction
    """
    # Safety check for Brochure ID
    if not BROCHURE_FILE_ID:
        return {"confidence": 0.0, "action": "Error", "reason": "Brochure ID missing in .env"}

    # 1. Get the Brochure
    file_path = download_brochure(BROCHURE_FILE_ID)
    
    # 2. Read the Brochure
    brochure_text = extract_text_from_pdf(file_path)
    
    # 3. Analyze with AI
    llm_output = analyze_student_query(user_query, brochure_text)
    
    confidence_score = llm_output.get("confidence_score", 0.0)
    answer = llm_output.get("answer", "No specific answer found.")
    reason = llm_output.get("reason", "No reason provided.")
    
    # 4. Determine and Execute Action
    if confidence_score >= 0.8:
        action_taken = "Gmail Draft"
        # Using your default recipient for the draft
        recipient = "barma.seshubabu@gmail.com" 
        create_gmail_draft(user_query, answer, recipient)
    else:
        action_taken = "WhatsApp Alert"
        alert_msg = f"Unresolved Query: {user_query}\nReason: {reason}"
        send_whatsapp_alert(alert_msg)

    # 5. Log the results to CSV
    log_transaction(user_query, confidence_score, action_taken, reason)

    # 6. Return Data for the UI
    return {
        "confidence": confidence_score,
        "action": action_taken,
        "reason": reason,
        "answer": answer
    }

# NOTICE: No 'while True' or 'input()' here. 
# This file is now a dedicated logic module for app.py.