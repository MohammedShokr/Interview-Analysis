from database_functions import *
from audio_processing import *
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
wavnum = divide_audio("test_interviews/y2mate_short.wav", "tone_analysis/seg_result", 5000, 3000)
print(wavnum)

