import speech_recognition as sr
from speech import get_voice_command, generate_email_body, speak
from send_email import create_email_draft
import Contacts
import openai
import os
import osascript

# Setzen Sie Ihren OpenAI API Schlüssel
openai.api_key = os.environ['OPENAI_API_KEY']

def mask_special_characters(text):
    text = text.replace('"', '\\"')  # Maskiert Anführungszeichen
    text = text.replace('\\', '\\\\')  # Maskiert Escape-Zeichen
    return text

def get_contact_email(name):
    print(f"Suche Kontakt für Name: {name}")
    store = Contacts.CNContactStore.new()
    predicate = Contacts.CNContact.predicateForContactsMatchingName_(name)
    keys_to_fetch = [Contacts.CNContactEmailAddressesKey]
    contacts = store.unifiedContactsMatchingPredicate_keysToFetch_error_(predicate, keys_to_fetch, None)
    
    if not contacts:
        print("Keine Kontakte gefunden.")
        return None
    
    for contact in contacts:
        print(f"Kontakt gefunden: {contact}")
        email_addresses = contact.valueForKey_(Contacts.CNContactEmailAddressesKey)
        if email_addresses:
            first_email_address = email_addresses[0].valueForKey_("value")
            return str(first_email_address)

    print("Keine E-Mail-Adressen für Kontakt gefunden.")
    return None

def process_email_command(command):
    if "schreibe eine e-mail an" in command.lower():
        to_name = command.split("an")[-1].strip() # Nimmt den Namen nach "an".
        return get_contact_email(to_name)
    return None

def main():
    command = get_voice_command()
    to_address = process_email_command(command)
    if to_address:
        print(f"E-Mail-Adresse gefunden: {to_address}")
        subject_prompt = "Was ist der Betreff der E-Mail?"
        speak(subject_prompt)
        subject = get_voice_command()
        body_prompt = "Was möchten Sie in der E-Mail schreiben?"
        speak(body_prompt)
        body_input = get_voice_command()

        # Hier rufen Sie die OpenAI-API mit `body_input` auf
        body = generate_email_body(body_input)
        
        create_email_draft(to_address, subject, body)

if __name__ == "__main__":
    main()









