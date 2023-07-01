# Anpassungen in speech.py
import boto3
import os
import pygame
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import numpy as np
import sounddevice as sd

polly_client = boto3.Session(
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name='eu-central-1').client('polly')

def get_voice_command():
    # Anfang der Aufnahme
    print("Sprechen Sie jetzt...")
    duration = 10  # vorläufige Dauer
    fs = 44100  # Sample-Rate
    my_recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Warten, bis die Aufnahme abgeschlossen ist
    nonsilent = detect_nonsilent(AudioSegment(my_recording, frame_rate=fs))
    # Wenn die Sprache aufhört, die Aufnahme stoppen
    if nonsilent:
        end_time = nonsilent[-1][1]
        my_recording = my_recording[:end_time*fs]
    # Verwenden Sie Amazon Transcribe, um die Sprache zu transkribieren
    transcribe_client = boto3.client('transcribe', region_name='eu-central-1')
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName='MyTranscriptionJob',
        LanguageCode='de-DE',
        Media={'MediaFileUri': 's3://my-bucket/my-recording.wav'}
    )
    while True:
        status = transcribe_client.get_transcription_job(TranscriptionJobName='MyTranscriptionJob')
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_text = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    else:
        transcript_text = ''
    print(f"Sie sagten: {transcript_text}\n")
    return transcript_text

def speak(text):
    response = polly_client.synthesize_speech(VoiceId='Hans',
                OutputFormat='mp3', 
                Text = text)
    file = open('speech.mp3', 'wb')
    file.write(response['AudioStream'].read())
    file.close()

    pygame.mixer.init()
    pygame.mixer.music.load("speech.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy() == True:
        continue

    os.remove('speech.mp3')


