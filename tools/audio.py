import pygame
import os

from gtts import gTTS
from playsound import playsound
from multiprocessing import Process, Queue
import os


class TextToSpeech:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TextToSpeech, cls).__new__(cls)
            cls._instance.queue = Queue()
            cls._instance.process = Process(target=cls._instance.run)
            cls._instance.process.start()
        return cls._instance

    def run(self):
        while True:
            text = self.queue.get()
            if text is None:
                break
            self.text_to_speech(text)

    def text_to_speech(self, text):
        tts = gTTS(text)
        filename = "temp_audio.mp3"
        tts.save(filename)
        playsound(filename)
        os.remove(filename)

    def speak(self, text):
        self.queue.put(text)

    def stop(self):
        self.queue.put(None)
        self.process.join()
