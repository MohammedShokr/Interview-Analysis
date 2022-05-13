import os
import sys
import librosa
import keras
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import specgram
from keras.models import load_model
from audio_processing import *

def analyze_audio(audio_path):
    # used internal functions
    def extract_features(data, sample_rate):
        # ZCR
        zcr = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)
        # FT
        #stft = np.abs(librosa.stft(data))
        #chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
        # MFCC
        mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate, n_mfcc=20).T, axis=0)
        # Root Mean Square Value
        rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
        # MelSpectrogram
        #mel = np.mean(librosa.feature.melspectrogram(y=data, sr=sample_rate).T, axis=0)
        #result = np.hstack((result, mel))  # stacking horizontally
        spectral_flux = np.mean(librosa.onset.onset_strength(y=data, sr=sample_rate).T, axis=0) #Spectral Flux (Stanford's). Returns 1 Value
        result = np.hstack([mfcc, rms, spectral_flux, zcr])
        return result

    def get_features(path):
        # duration and offset are used to take care of the no audio in start and the ending of each audio files
        # as seen above.
        data, sample_rate = librosa.load(path, sr=None)
        if data.ndim > 1:
            data = data[:,0]
        data = data.T

        res1 = extract_features(data, sample_rate)
        result = np.array(res1)
        return result

    # load needed objects (model and scaler and encoder)
    model = keras.models.load_model('./fluency_analysis/model') ###./fluency_analysis/model
    # apply feature extraction and transformations before predicting
    feature = get_features(audio_path)
    #transformed_feature = scaler.transform(feature.reshape(1, -1))
    extracted_feature = np.vstack([feature])
    # predict using the model
    predict_test = model.predict(extracted_feature)
    return list(predict_test[0])

def scoring_fluency_expressions(expression_weights):
    score = 0
    low = expression_weights[0]
    if low < 0.1:
        score += 10
    elif low < 0.3:
        score += 5
    elif low < 0.5:
        score += 1
    intermediate = expression_weights[1]
    if intermediate < 0.1:
        score += 1
    elif intermediate < 0.3:
        score += 5
    elif intermediate < 0.5:
        score += 10
    high = expression_weights[2]
    if high < 0.1:
        score += 1
    elif high < 0.3:
        score += 5
    elif high < 0.7:
        score += 10
    return round(score/3, 2)

def analyze_audio_segments(segments_folder_path, wav_num):
    expression_matrix = {}
    for i in range(0, wav_num):
        audio_path = f'{segments_folder_path}/wav_{i+1}.wav'
        prediction = analyze_audio(audio_path)
        expression_matrix[i]=prediction
    return expression_matrix

def analyze_fluency(audio_file):
    wav_num = divide_audio(audio_file, "./fluency_analysis/seg_result") #CHANGE PATH TO: "./tone_analysis/seg_result"
    expression_matrix = analyze_audio_segments("./fluency_analysis/seg_result", wav_num) #CHANGE PATH TO: "./tone_analysis/seg_result"
    expression_weights = np.mean(np.array(list(expression_matrix.values())), axis=0)
    score = scoring_fluency_expressions(expression_weights)
    return score*10, expression_matrix, expression_weights

#print(analyze_fluency("./fluency_analysis/seg_result/wav_1.wav"))
