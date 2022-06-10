import os
import librosa
import librosa.display
import numpy as np
from pydub import AudioSegment
from moviepy.editor import *


def convert_video_to_audio(video_file, output_ext="wav"):
    filename, ext = os.path.splitext(video_file)
    audio_file = f"{filename}.{output_ext}"
    video = VideoFileClip(video_file)
    video.audio.write_audiofile(audio_file)
    return audio_file


def divide_audio(audio_path, output_folder_path, seg_len, stride):
    my_audio = AudioSegment.from_wav(audio_path)
    audio_len = len(my_audio)
    # self.TextResultTone.append(audio_len)
    num_of_segments = int(((audio_len - seg_len)/stride)+1)
    remainder = audio_len-(((num_of_segments-1)*stride)+seg_len)

    seg = 0
    wav_num = 1
    for _ in range(num_of_segments):
        # self.TextResultTone.append(wav_num)
        segment = my_audio[seg:seg + seg_len]
        segment.export(f'{output_folder_path}/wav_{wav_num}.wav', format="wav")
        seg += stride
        wav_num += 1
    if remainder > 0:
        segment = my_audio[-seg_len//2:]
        segment.export(f'{output_folder_path}/wav_{wav_num}.wav', format="wav")
    silence_percentage = analyze_silence_segments(output_folder_path, wav_num)
    return wav_num, silence_percentage


def analyze_silence_segments(segments_folder_path, wav_num):
    energies = []
    silent_count = 0
    for i in range(0, wav_num):
        audio_path = f'{segments_folder_path}/wav_{i+1}.wav'
        data, sample_rate = librosa.load(audio_path)
        rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
        print(rms[0])
        energies.append(rms[0])
    max_energy = max(energies)
    zeros = 0
    if max_energy*10 >= 1:
        zeros = 1
    if max_energy*100 >= 1:
        zeros = 2
    # #########
    zeros += 1
    integer_energies = [e*(10**zeros) for e in energies]
    max_energy = max(integer_energies)
    threshold = 0.68*max_energy
    threshold = 17
    for e in integer_energies:
        print(f'lol: {e}')
        if e <= threshold:
            silent_count += 1
    return (silent_count/wav_num)*100  # percent of silence
