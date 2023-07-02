import boto3
import os
import pygame
import io
import soundfile as sf
import numpy as np
import sounddevice as sd
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import openai

polly_client = boto3.Session(
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name='eu-central-1').client('polly')


def numpy_to_audio_segment(audio_numpy, frame_rate):
    byte_io = io.BytesIO()
    sf.write(byte_io, audio_numpy, frame_rate, format='wav')
    byte_io.seek(0)
    audio_segment = AudioSegment.from_file(byte_io, format="wav")
    return audio_segment


def get_voice_command():
    print("Sprechen Sie jetzt...")
    duration = 10
    fs = 44100
    my_recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    my_audio_segment = numpy_to_audio_segment(my_recording, fs)
    nonsilent = detect_nonsilent(my_audio_segment)

    if nonsilent:
        end_time = nonsilent[-1][1]
        my_recording = my_recording[:int(end_time*fs)]

    transcribe_client = boto3.client('transcribe', region_name='eu-central-1')
    s3_bucket_name = 'dein-gueltiger-bucket-name'
    s3_client = boto3.client('s3', region_name='eu-central-1')

    byte_io = io.BytesIO()
    sf.write(byte_io, my_recording, fs, format='wav')
    byte_io.seek(0)
    s3_client.upload_fileobj(byte_io, s3_bucket_name, 'my-recording.wav')

    s3_uri = f's3://{s3_bucket_name}/my-recording.wav'

    response = transcribe_client.start_transcription_job(
        TranscriptionJobName='MyTranscriptionJob',
        Media={'MediaFileUri': s3_uri},
        MediaFormat='wav',
        LanguageCode='de-DE',
        OutputBucketName=s3_bucket_name
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


openai.api_key = 'YOUR_OPENAI_API_KEY'


def generate_email_body(prompt):
    response = openai.Completion.create(
        engine="text-davinci-004",
        prompt=prompt,
        temperature=0.5,
        max_tokens=300
    )


