import os
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
    return wav_num


