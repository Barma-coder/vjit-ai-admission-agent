import os
from dotenv import load_dotenv
from ai_tool import analyze_student_query
from drive_tool import download_brochure
from pdf_tool import extract_text_from_pdf
from gmail_tool import create_gmail_draft
from twilio_tool import send_whatsapp_alert 

# Load the .env file
load_dotenv()

# Get the Brochure ID from your .env
BROCHURE_FILE_ID = os.getenv("BROCHURE_FILE_ID")

def run_agentic_workflow(user_query):
    # Check if we actually found the ID in .env
    if not BROCHURE_FILE_ID:
        print("❌ Error: BROCHURE_FILE_ID not found in .env file!")
        return

    print(f"\n--- Processing Query: {user_query} ---")
    
    # 1. Get the Brochure
    print(f"Step 1: Downloading brochure from Google Drive...")
    file_path = download_brochure(BROCHURE_FILE_ID)
    
    # 2. Read the Brochure
    print(f"Step 2: Extracting text from PDF...")
    brochure_text = extract_text_from_pdf(file_path)
    
    file_path = download_brochure(BROCHURE_FILE_ID)
    brochure_text = extract_text_from_pdf(file_path)
    
    # 3. Analyze with AI
    llm_output = analyze_student_query(user_query, brochure_text)
    
    confidence_score = llm_output.get("confidence_score", 0.0)
    answer = llm_output.get("answer", "No specific answer found.")
    reason = llm_output.get("reason", "No reason provided.")
    
    # 4. Determine Action & Log it
    if confidence_score >= 0.8:
        action_taken = "Gmail Draft"
        # In a real UI scenario, you might pre-set a recipient or ask via UI
        # For now, we'll use a placeholder or the one you usually use
        recipient = "barma.seshubabu@gmail.com" 
        create_gmail_draft(user_query, answer, recipient)
    else:
        action_taken = "WhatsApp Alert"
        alert_msg = f"Unresolved Query: {user_query}\nReason: {reason}"
        send_whatsapp_alert(alert_msg)

    # 5. LOG THE TRANSACTION (Crucial: happens before the return)
    from logging_tool import log_transaction
    log_transaction(user_query, confidence_score, action_taken, reason)

    # 6. RETURN the data so app.py can use it for the Success/Warning messages
    return {
        "confidence": confidence_score,
        "action": action_taken,
        "reason": reason,
        "answer": answer
    }