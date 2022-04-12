import os
import librosa
import librosa.display
from pydub import AudioSegment
import keras
import pickle
import numpy as np
from moviepy.editor import *

def convert_video_to_audio(video_file, output_ext="wav"):
    filename, ext = os.path.splitext(video_file)
    audio_file = f"{filename}.{output_ext}"
    video = VideoFileClip(video_file)
    video.audio.write_audiofile(audio_file)
    return audio_file

def analyze_audio(audio_path):
    # used internal functions
    def extract_features(data, sample_rate):
        # ZCR
        result = np.array([])
        zcr = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)
        result = np.hstack((result, zcr))  # stacking horizontally
        # Chroma_stft
        stft = np.abs(librosa.stft(data))
        chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
        result = np.hstack((result, chroma_stft))  # stacking horizontally
        # MFCC
        mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate).T, axis=0)
        result = np.hstack((result, mfcc))  # stacking horizontally
        # Root Mean Square Value
        rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
        result = np.hstack((result, rms))  # stacking horizontally
        # MelSpectrogram
        mel = np.mean(librosa.feature.melspectrogram(y=data, sr=sample_rate).T, axis=0)
        result = np.hstack((result, mel))  # stacking horizontally
        return result

    def get_features(path):
        # duration and offset are used to take care of the no audio in start and the ending of each audio files
        # as seen above.
        data, sample_rate = librosa.load(path, duration=2.5, offset=0.6)
        # without augmentation
        res1 = extract_features(data, sample_rate)
        result = np.array(res1)
        return result

    # load needed objects (model and scaler and encoder)
    model = keras.models.load_model('./tone_analysis/model')
    with open(r"./tone_analysis/scaler", "rb") as input_file:
        scaler = pickle.load(input_file)
    with open(r"./tone_analysis/encoder", "rb") as input_file:
        encoder = pickle.load(input_file)
    # apply feature extraction and transformations before predicting
    feature = get_features(audio_path)
    transformed_feature = scaler.transform(feature.reshape(1, -1))
    transformed_feature = np.expand_dims(transformed_feature, axis=2)
    # predict using the model
    predict_test = model.predict(transformed_feature)
    y_predict = encoder.inverse_transform(predict_test)
    # return the predicted label
    return y_predict[0][0]

def divide_audio(audio_path, output_folder_path):
    my_audio = AudioSegment.from_wav(audio_path)
    audio_len = len(my_audio)
    # self.TextResultTone.append(audio_len)
    num_of_segments = audio_len // 5000
    remainder = audio_len % 5000

    seg = 0
    wav_num = 1
    for _ in range(num_of_segments):
        # self.TextResultTone.append(wav_num)
        segment = my_audio[seg:seg + 5000]
        segment.export(f'{output_folder_path}/wav_{wav_num}.wav', format="wav")
        seg += 3000
        wav_num += 1
    if remainder > 0:
        segment = my_audio[-5000:]
        segment.export(f'{output_folder_path}/wav_{wav_num}.wav', format="wav")
    return wav_num


def analyze_audio_segments(segments_folder_path, wav_num):
    text = ""
    for i in range(1, wav_num):
        audio_path = f'{segments_folder_path}/wav_{i}.wav'
        prediction = analyze_audio(audio_path)
        text += "tone of wav_"+str(i)+": "+str(prediction)+"\n"
    return text

def analyze_tone(video_file):
    audio_file = convert_video_to_audio(video_file)
    wav_num = divide_audio(audio_file, "./tone_analysis/seg_result")
    prediction = analyze_audio_segments("./tone_analysis/seg_result", wav_num)
    #prediction = analyze_audio(video_file)
    tone_weights = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.4]
    tone_score = 0
    return tone_score, tone_weights

#print(analyze_tone("./interview samples/introduceyourself.webm"))