import pypdf

def extract_text_from_pdf(file_stream):
    if file_stream is None:
        return ""
    
    try:
        reader = pypdf.PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"❌ PDF Tool Error: {e}")
        return ""