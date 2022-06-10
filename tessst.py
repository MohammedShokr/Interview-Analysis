from database_functions import *
from audio_processing import *
from matplotlib.style import available
import streamlit as st
import pandas as pd
import numpy as np
import io
from FER import analyze_face
from tone import analyze_tone
from fluency_analysis import analyze_fluency
from database_functions import *
from audio_processing import convert_video_to_audio
from coherence_assessment import coherence_scoring
from speech_to_text import short_speech_to_text
from Queries import *
# # user = get_company("6989")
# # if len(user) > 0:
# #     password = user[0][2]
#
# users_raw = get_company_IDs()
# users = [u[0] for u in users_raw]
# passwords = [get_company(u)[0][2] for u in users]
# print(users)
# print(passwords)
# "test_interviews/y2mate_short.wav"
# my_audio = AudioSegment.from_wav("test_interviews/y2mate_short.wav")
# my_audio.export(f'sss.wav', format="wav")
# audio_path = convert_video_to_audio("test_interviews/ss_test.mp4")
# wavnum, _ = divide_audio("test_interviews/y2mate_short.wav", "tone_analysis/seg_result", 5000, 3000)
# print(wavnum)
# video_path = "test_interviews/newnew_vid.mp4"
# audio_path = convert_video_to_audio(video_path)
# tone_score, tone_matrix, tone_weights, silence = analyze_tone(audio_path)
# print(f'SCORE: {tone_score}')
# print(f'weights: {tone_weights}')
# print(f'silence: {silence}')
from tensorflow.keras.utils import plot_model
model = keras.models.load_model('./tone_analysis/model') #####./tone_analysis/model
plot_model(model, to_file='model.png', show_shapes=True, show_layer_names=True)