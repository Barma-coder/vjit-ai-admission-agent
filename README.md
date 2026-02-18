A great `README.md` is the "front door" of your project. It explains what the code does, how it’s built, and how others can get it running.

Since you are pushing to GitHub, you should save this content into a file named **`README.md`** in your root folder.

---

# 🎓 VJIT Autonomous AI Admission Agent

An intelligent, full-stack **Agentic Workflow** designed to automate student admission inquiries. This system uses Retrieval-Augmented Generation (RAG) to read institutional documents and intelligently routes responses via **Gmail** (for high-confidence matches) or **WhatsApp** (for human follow-up).

---

## 🚀 Features

* **Document Intelligence**: Automatically downloads and parses the VJIT brochure from Google Drive.
* **Intelligent Routing**: Uses **Gemini 2.5 Flash** to analyze queries and calculate a confidence score.
* **Gmail Integration**: Automatically creates professional email drafts for verified information.
* **WhatsApp Alerts**: Sends instant Twilio notifications to staff for queries the AI cannot resolve (low confidence).
* **Web Dashboard**: A professional **Streamlit** interface to monitor live queries, view analytics, and audit logs.
* **Persistent Logging**: Every interaction is tracked in a CSV for institutional gap analysis.

---

## 🛠️ Tech Stack

* **Language**: Python 3.10+
* **AI Model**: Google Gemini 2.5 Flash
* **Frontend**: Streamlit
* **APIs**: Google Drive API, Gmail API, Twilio API
* **Data Handling**: PyPDF, Pandas

---

## 🏗️ System Architecture

1. **Data Layer**: Service Account fetches PDF from Google Drive.
2. **Logic Layer**: AI processes query + brochure context + chat history.
3. **Action Layer**:
* `Confidence >= 0.8`: Create Gmail Draft.
* `Confidence < 0.8`: Send WhatsApp Alert.


4. **UI Layer**: Streamlit displays metrics and log history.

---

## 📦 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Barma-coder/vjit-ai-admission-agent.git
cd vjit-ai-admission-agent

```

### 2. Set up Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

```

### 3. Environment Variables

Create a `.env` file in the root directory and add your credentials:

```text
GOOGLE_API_KEY=your_gemini_api_key
BROCHURE_FILE_ID=your_google_drive_file_id
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
MY_WHATSAPP_NUMBER=whatsapp:+91XXXXXXXXXX

```

### 4. Authentication

Place your `credentials.json` (for Gmail OAuth) and `service_account.json` (for Google Drive) in the root folder.

---

## 🖥️ Usage

To launch the dashboard, run:

```bash
streamlit run app.py

```



