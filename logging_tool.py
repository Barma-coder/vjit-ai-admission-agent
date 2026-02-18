import csv
import os
from datetime import datetime

LOG_FILE = "admission_logs.csv"

def log_transaction(query, confidence, action, reason):
    file_exists = os.path.isfile(LOG_FILE)
    
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Student Query", "Confidence", "Action Taken", "Reasoning"])
        
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            query,
            confidence,
            action,
            reason
        ])