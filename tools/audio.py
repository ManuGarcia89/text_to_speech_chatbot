import os
from io import BytesIO
from gtts import gTTS
from playsound import playsound
from multiprocessing import Process, Queue
import pygame


class TextToSpeech:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            pygame.init()
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

    def play_sound_with_file(self, text):
        tts = gTTS(text, lang="es", slow=False, lang_check=False, tld="com.mx")

        filename = "temp_audio.mp3"

        mp3_fp = BytesIO()
        # tts.write_to_fp(mp3_fp)

        tts.save(filename)
        playsound(filename)
        # playsound(mp3_fp)
        os.remove(filename)

    def play_sound_in_memory(self, text):
        tts = gTTS(text, lang="es", slow=False, lang_check=False, tld="com.mx")
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        pygame.mixer.init()
        pygame.mixer.music.load(mp3_fp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()

    def text_to_speech(self, text):
        self.play_sound_in_memory(text)

    def speak(self, text):
        self.queue.put(text)

    def stop(self):
        self.queue.put(None)
        self.process.join()
