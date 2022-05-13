import librosa
import librosa.display
import keras
import pickle
import numpy as np
from audio_processing import *


def scoring_tone_expressions(expression_weights):
    score = 0
    angry = expression_weights[0]
    if angry < 0.1:
        score += 10
    elif angry < 0.3:
        score += 5
    elif angry < 0.5:
        score += 1
    fear = expression_weights[1]
    if fear < 0.1:
        score += 10
    elif fear < 0.3:
        score += 5
    elif fear < 0.5:
        score += 1
    happy = expression_weights[2]
    if happy < 0.1:
        score += 1
    elif happy < 0.3:
        score += 5
    elif happy < 0.6:
        score += 10
    elif happy < 0.8:
        score += 5
    else:
        score += 1
    sad = expression_weights[3]
    if sad < 0.2:
        score += 10
    elif sad < 0.3:
        score += 5
    elif sad < 0.5:
        score += 1
    surprise = expression_weights[4]
    if surprise < 0.3:
        score += 10
    elif surprise < 0.5:
        score += 5
    else:
        score += 1
    return round(score/5, 2)


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
    model = keras.models.load_model('./tone_analysis/model') #####./tone_analysis/model
    with open(r"./tone_analysis/scaler", "rb") as input_file: ####./tone_analysis/scaler
        scaler = pickle.load(input_file)
    with open(r"./tone_analysis/encoder", "rb") as input_file: ####./tone_analysis/encoder
        encoder = pickle.load(input_file)
    # apply feature extraction and transformations before predicting
    feature = get_features(audio_path)
    transformed_feature = scaler.transform(feature.reshape(1, -1))
    transformed_feature = np.expand_dims(transformed_feature, axis=2)
    # predict using the model
    predict_test = model.predict(transformed_feature)
    return predict_test[0]


def analyze_audio_segments(segments_folder_path, wav_num):
    expression_matrix = {}
    for i in range(0, wav_num):
        audio_path = f'{segments_folder_path}/wav_{i+1}.wav'
        prediction = analyze_audio(audio_path)
        expression_matrix[i]=list(prediction)
    return expression_matrix


def analyze_tone(audio_file):
    wav_num = divide_audio(audio_file, "./tone_analysis/seg_result") #CHANGE PATH TO: "./tone_analysis/seg_result"
    expression_matrix = analyze_audio_segments("./tone_analysis/seg_result", wav_num) #CHANGE PATH TO: "./tone_analysis/seg_result"
    expression_weights = np.mean(np.array(list(expression_matrix.values())), axis=0)
    score = scoring_tone_expressions(expression_weights)
    return score*10, expression_matrix, expression_weights
