#!pip install SpeechRecognition
#!python -m speech_recognition
import speech_recognition as sr
from audio_processing import *

# create a speech recognition object
r = sr.Recognizer()

def short_speech_to_text(AUDIO_FILE):
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def long_speech_to_text(AUDIO_FILE, OUT_PATH):
    wav_num, _ = divide_audio(AUDIO_FILE, OUT_PATH, 5000, 3000)  # divide the audio into shorter instances
    text = ""
    for i in range(1, wav_num):
        audio_path = f'{OUT_PATH}/wav_{i}.wav'
        text += str(short_speech_to_text(audio_path)) + "\n"  # convert each intance to text
    return text
