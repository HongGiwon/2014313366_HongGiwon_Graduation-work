# coding=utf-8
import json
from watson_developer_cloud import TextToSpeechV1
from pydub import AudioSegment
from StringIO import StringIO

text_to_speech = TextToSpeechV1(
    username='9a69aac9-77b4-4f02-a9e5-42fd4cd14b86',
    password='eFmlM1Xr3Gvb',
    x_watson_learning_opt_out=True)  # Optional flag

speechstring = raw_input()

print(json.dumps(text_to_speech.voices(), indent=2))

#with open(join(dirname(__file__), '../resources/output.wav'),
#          'wb') as audio_file:
#    audio_file.write(
#        text_to_speech.synthesize(speechstring, accept='audio/wav',
#                                  voice="en-US_AllisonVoice"))

aa= AudioSegment.from_wav(StringIO(text_to_speech.synthesize(speechstring, accept='audio/wav',voice="en-US_AllisonVoice")))
aa.export("../resources/output.wav", format="wav")

print(
    json.dumps(text_to_speech.pronunciation(
        'Watson', pronunciation_format='spr'), indent=2))

print(json.dumps(text_to_speech.customizations(), indent=2))
