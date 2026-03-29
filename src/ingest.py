import os
import json
from pypdf import PdfReader

DATA_PATH = "data"


#  Nettoyage texte
def clean_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


#  TXT
def load_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return clean_text(f.read())
    except Exception as e:
        print(f"[ERROR TXT] {file_path}: {e}")
        return ""


#  PDF
def load_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"

        return clean_text(text)

    except Exception as e:
        print(f"[ERROR PDF] {file_path}: {e}")
        return ""


#  JSON → TEXTE GÉNÉRIQUE 
def json_to_text(data, parent_key=""):
    text_parts = []

    if isinstance(data, dict):
        for key, value in data.items():
            key_clean = key.replace("_", " ").capitalize()
            new_key = f"{parent_key} {key_clean}".strip()

            if isinstance(value, (dict, list)):
                text_parts.append(json_to_text(value, new_key))
            else:
                text_parts.append(f"{new_key}: {value}")

    elif isinstance(data, list):
        for item in data:
            text_parts.append(json_to_text(item, parent_key))

    return "\n".join(text_parts)


def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        documents = []

        
        if isinstance(data, list):
            for item in data:
                text_parts = []

                for key, value in item.items():
                    key_clean = key.replace("_", " ").capitalize()
                    text_parts.append(f"{key_clean}: {value}")

                text = "\n".join(text_parts)

                documents.append({
                    "text": clean_text(text),
                    "source": os.path.basename(file_path)
                })

        else:
            text = json_to_text(data)
            documents.append({
                "text": clean_text(text),
                "source": os.path.basename(file_path)
            })

        return documents

    except Exception as e:
        print(f"[ERROR JSON] {file_path}: {e}")
        return []


#  Charger tous les documents
def load_documents():
    documents = []

    for filename in os.listdir(DATA_PATH):
        path = os.path.join(DATA_PATH, filename)

        if filename.endswith(".txt"):
            text = load_txt(path)

        elif filename.endswith(".pdf"):
            text = load_pdf(path)

        elif filename.endswith(".json"):
           json_docs = load_json(path)
           documents.extend(json_docs)
           continue

        else:
            continue

        
        if not text.strip():
            continue

        documents.append({
            "text": text,
            "source": filename
        })

    return documents