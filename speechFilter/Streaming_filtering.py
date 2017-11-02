#!/usr/bin/env python

from __future__ import division

import re
import sys
import os
import json
import wave


from google.cloud import speech
from google.cloud.speech import types
from google.cloud.speech import enums


import pyaudio
from six.moves import queue
from playsound import playsound

import argparse
import io
from pydub import AudioSegment

import gensim
from sklearn.metrics.pairwise import cosine_similarity
from konlpy.tag import Twitter


RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './My Project-f557b58c64ab.json'
global frames
frames = []

def flat(content):
    token_tmp = Twitter().pos(content)
    return ["{}/{}".format(word, tag) for word, tag in token_tmp if (tag != "Punctuation"and tag != "Foreign")]

class MicStream(object):
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            stream_callback=self._fill_buffer,
            channels=1, input=True, frames_per_buffer=self._chunk,
            rate=self._rate,
        )
        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]
            frames.append(chunk)
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                    frames.append(chunk)
                except queue.Empty:
                    break
            yield b''.join(data)

class SoundFilter:
    def __init__(self):
        #self.__bad_word_dic = self.load_database()
        self.__beep_sound = AudioSegment.from_wav('./beep/censor-beep4.wav')

    def start_record(self):
        language_code = 'ko-KR'
        client = speech.SpeechClient()
        phrases = ["머머리", "븅신"]
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=language_code,
            enable_word_time_offsets=True
            # speech_contexts=[speech.types.SpeechContext(
            #    phrases = ['머머리'],
            # )],
        )
        streaming_config = types.StreamingRecognitionConfig(
            config=config)

        print ("#####녹음 시작######")

        with MicStream(RATE, CHUNK) as stream:
            audio_generator = stream.generator()
            requests = (types.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)

            responses = client.streaming_recognize(streaming_config, requests)

            # Now, put the transcription responses to use.
            self.listen_print_loop(responses)

    def listen_print_loop(self, responses):
        num_chars_printed = 0
        for response in responses:
            if not response.results:
                continue
            print(response)
            result = response.results[0]
            if not result.alternatives:
                continue
            self.print_results(result)

    def print_results(self, result):
        global bad_word_vec
        global model_words_vec
        print("###########################################")
        #    print(result)
        if result.is_final:
            speech_start_time = -1
            for candResult in result.alternatives:
                print('텍스트: ' + str(candResult.transcript))
                print('정확도: ' + str(candResult.confidence))

                b_time_arr = []
                b_word_arr = []

                for word_info in candResult.words:
                    word = word_info.word
                    start_time =  word_info.start_time.seconds + word_info.start_time.nanos / 1000000000
                    end_time = word_info.end_time.seconds + word_info.end_time.nanos / 1000000000

                    if speech_start_time is -1:
                        speech_start_time = start_time

                    tokenizied_word = flat(word)
                    for token_of_word in tokenizied_word :
                        try :
                            if (model_words_vec.vocab[token_of_word].count < 1000) :
                                print (" 학습이 부족한 단어 발견 : " + token_of_word)
                                poten_learn(token_of_word.split("/")[0])
                            if (cosine_similarity([bad_word_vec], [model_words_vec[token_of_word]])[0][0] > 0.6) :
                                print (" 욕설 발견 : " + token_of_word)
                                b_word_arr.append(word)
                                b_time_arr.append(start_time)
                                b_time_arr.append(end_time)
                                break
                        except KeyError: 
                            print ( "학습 되지 않은 단어 발견 : " + token_of_word)
                            poten_learn(token_of_word.split("/")[0])

                    print(' 단어: ' + word_info.word + ' / ' + str(
                        word_info.start_time.seconds + word_info.start_time.nanos / 1000000000) + ' / ' + str(
                        word_info.end_time.seconds + word_info.end_time.nanos / 1000000000))

            waveFile = wave.open("file.wav", 'wb')
            waveFile.setnchannels(1)
            waveFile.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()

            self.censor_audio(b_time_arr, b_word_arr, speech_start_time)

        else:
            for candResult in result.alternatives:
                print('텍스트: ' + str(candResult.transcript))
                print('정확도: ' + str(candResult.confidence))

    def censor_audio(self, c_time_list, c_word_arr, speech_start_time):
        audio_sound = AudioSegment.from_wav('./file.wav')

        intervals = list(map(float, c_time_list))
        censored_result = audio_sound

        for index in range(0, len(c_word_arr)):
            interval_dur = (intervals[index * 2 + 1] - intervals[index * 2]) * 1000
            beep_count = int((interval_dur / 100))
            remain = interval_dur - (beep_count * 100)
            sound_beep = self.__beep_sound * beep_count + self.__beep_sound[:remain]
            s1 = censored_result[:intervals[index * 2] * 1000]
            s2 = censored_result[intervals[index * 2 + 1] * 1000:]
            censored_result = s1 + sound_beep + s2
        censored_result[speech_start_time * 1000:].export("./output/change.wav", format="wav")
        #censored_result.export("./output/change.wav", format="wav")
        playsound("./output/change.wav")
        print("OK")

bad_word_vec = []

def loading_word2vec_model() :
    print ("word2vec 모델 로딩중...")
    global bad_word_vec
    global model_words_vec

    model = gensim.models.Word2Vec.load('model')
    
    bad_word_vec = model.bad_word_vec

    model_words_vec = model.wv
    del model
    print("모델 로딩 완료")

def poten_learn(word):
    flag = 0
    unlearned_word_txt = open("unlearned_word.txt", 'r')
    for ul_word in unlearned_word_txt.readlines() :
        if(ul_word.split("\n")[0] == word) :
            flag = 1
            break
    unlearned_word_txt.close()

    if (flag == 0) :
        unlearned_word_txt = open("unlearned_word.txt", 'a')
        unlearned_word_txt.write(word + "\n")
        unlearned_word_txt.close()

def main():
    loading_word2vec_model()
    soundFilter = SoundFilter()
    soundFilter.start_record()

if __name__ == '__main__':
    main()
