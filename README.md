# Chatbot mit Spracherkennung und -synthese

Dieses Projekt ist ein einfacher Chatbot, der Spracheingaben über ein Mikrofon entgegennehmen, diese in Text umwandeln, den Text verarbeiten, eine Antwort generieren und diese Antwort dann synthetisieren und aussprechen kann.

## Setup

### Umgebungsvariablen

Stellen Sie sicher, dass die folgenden Umgebungsvariablen gesetzt sind:

- AWS_ACCESS_KEY_ID: Ihr AWS Access Key.
- AWS_SECRET_ACCESS_KEY: Ihr AWS Secret Access Key.
- AWS_REGION: Die AWS-Region, in der Ihre S3-Buckets und Transcribe-Dienste gehostet werden.
- OPENAI_API_KEY: Ihr API-Schlüssel für OpenAI.

### Installation

1. Klone dieses Repository auf Ihren lokalen Computer:


2. Navigieren Sie in das Verzeichnis des Projekts:


3. Installieren Sie die erforderlichen Pakete:
   
   pip install -r requirements.txt


## Verwendung

Um den Chatbot zu starten, führen Sie das Hauptscript mit Python 3 aus:

python3 main.py


Der Chatbot wartet dann auf Spracheingaben, transkribiert diese in Text, verarbeitet den Text, generiert eine Antwort und spricht die Antwort aus.



