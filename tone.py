import librosa
import librosa.display
import keras
import pickle
import numpy as np
from audio_processing import *


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


def analyze_audio_segments(segments_folder_path, wav_num):
    text = ""
    for i in range(1, wav_num):
        audio_path = f'{segments_folder_path}/wav_{i}.wav'
        prediction = analyze_audio(audio_path)
        text += "tone of wav_"+str(i)+": "+str(prediction)+"\n"
    return text

def analyze_tone(audio_file):
    wav_num = divide_audio(audio_file, "./tone_analysis/seg_result")
    prediction = analyze_audio_segments("./tone_analysis/seg_result", wav_num)
    #prediction = analyze_audio(video_file)
    return 0, prediction
