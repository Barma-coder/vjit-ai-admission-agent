import streamlit as st
import pandas as pd
import os
import time
from main import run_agentic_workflow

# --- 1. Page Config & Styling ---
st.set_page_config(page_title="VJIT Admission Portal", page_icon="🎓", layout="wide")

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .stAlert { border-radius: 10px; }
    .stMetric { background-color: #f0f2f6; padding: 15px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. Logic to Refresh Logs ---
def get_logs():
    if os.path.exists("admission_logs.csv"):
        return pd.read_csv("admission_logs.csv").sort_index(ascending=False)
    return None

# --- 3. Header Section ---
st.title("🎓 VJIT Admission Agent Command Center")
st.markdown("---")

# --- 4. Metrics Row (Visual Agent Status) ---
logs_df = get_logs()
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Queries", len(logs_df) if logs_df is not None else 0)
with col2:
    if logs_df is not None:
        success_rate = (logs_df['Confidence'] >= 0.8).mean() * 100
        st.metric("Gmail Success Rate", f"{success_rate:.1f}%")
with col3:
    status = "🟢 Online" if os.getenv("GOOGLE_API_KEY") else "🔴 Offline"
    st.metric("Gemini API Status", status)
with col4:
    st.metric("Brochure Loaded", "📄 Yes" if os.path.exists("temp_brochure.pdf") else "❌ No")

st.markdown("###")

# --- 5. Interactive Query Processing ---
st.subheader("📬 Process New Student Inquiry")
with st.container():
    user_query = st.text_input("Enter the student's question:", placeholder="e.g. Does VJIT have CSE?")
    
    if st.button("🚀 Process Inquiry", use_container_width=True):
        if user_query:
            with st.status("Agent is analyzing...", expanded=True) as status:
                st.write("Step 1: Downloading & Reading Brochure...")
                # We need to capture the LLM output to give a specific message
                # For this to work perfectly, update run_agentic_workflow to return the output!
                result = run_agentic_workflow(user_query)
                st.write("Step 2: Performing Intelligent Reasoning...")
                time.sleep(1) # Visual padding
                status.update(label="Inquiry Processed!", state="complete", expanded=False)
            
            # --- Specific Confirmation Logic ---
            # We fetch the last log entry to see what happened
            latest_logs = pd.read_csv("admission_logs.csv").iloc[-1]
            if latest_logs['Confidence'] >= 0.8:
                st.success(f"✅ **High Confidence!** A draft has been created. Please verify your **Gmail Drafts**.")
            else:
                st.warning(f"⚠️ **Low Confidence!** This requires manual attention. An alert was sent to **WhatsApp** ({os.getenv('MY_WHATSAPP_NUMBER')}).")
            
            # Re-read logs immediately so they show up below
            logs_df = get_logs()
        else:
            st.error("Please enter a query first.")

st.markdown("---")

# --- 6. Graphical Logs View ---
st.subheader("📋 Interaction History & Insights")

if logs_df is not None:
    # Use tabs for a cleaner view
    tab1, tab2 = st.tabs(["🗃️ Detailed Logs", "📈 Analytics"])
    
    with tab1:
        st.dataframe(logs_df, use_container_width=True, hide_index=True)
    
    with tab2:
        # Simple bar chart of actions
        action_counts = logs_df['Action Taken'].value_counts()
        st.bar_chart(action_counts)
else:
    st.info("No history available yet. Process your first query above!")

# --- 7. Knowledge Base Section ---
with st.expander("📚 View Active Knowledge Source (Brochure Text)"):
    if os.path.exists("temp_brochure.pdf"):
        from pdf_tool import extract_text_from_pdf
        text = extract_text_from_pdf("temp_brochure.pdf")
        st.text_area("Content extracted from PDF:", value=text[:2000] + "...", height=300)
    else:
        st.error("No brochure file found in the system.")