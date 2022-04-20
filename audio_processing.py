import os
from pydub import AudioSegment
from moviepy.editor import *


def convert_video_to_audio(video_file, output_ext="wav"):
    filename, ext = os.path.splitext(video_file)
    audio_file = f"{filename}.{output_ext}"
    video = VideoFileClip(video_file)
    video.audio.write_audiofile(audio_file)
    return audio_file


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

