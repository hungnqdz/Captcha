import os
import argparse
import requests
import random
import pytesseract
from PIL import Image
from io import BytesIO
import speech_recognition as sr
from pydub import AudioSegment


class CaptchaSolver:
    def __init__(self):
        self.temp_folder = os.path.join(os.path.dirname(__file__), 'temp')
        os.makedirs(self.temp_folder, exist_ok=True)

    def bypass_image_captcha(self, captcha_image_url):
        response = requests.get(captcha_image_url)
        img = Image.open(BytesIO(response.content))
        captcha_text = pytesseract.image_to_string(img, config='--psm 8').strip()
        return captcha_text

    def is_mp3_format(self, audio_data):
        header = audio_data[:3]
        return header == b"ID3" or header[:2] == b"\xff\xfb"

    def bypass_audio_captcha(self, captcha_audio_url):
        response = requests.get(captcha_audio_url)
        audio_data = BytesIO(response.content)

        if self.is_mp3_format(audio_data.getvalue()):
            path_to_mp3 = os.path.join(self.temp_folder, f"captcha_audio_{random.randrange(1, 1000)}.mp3")
            path_to_wav = os.path.join(self.temp_folder, f"captcha_audio_{random.randrange(1, 1000)}.wav")

            with open(path_to_mp3, 'wb') as f:
                f.write(audio_data.getvalue())

            sound = AudioSegment.from_mp3(path_to_mp3)
            sound.export(path_to_wav, format="wav")
            return path_to_wav

        else:
            path_to_wav = os.path.join(self.temp_folder, f"captcha_audio_{random.randrange(1, 1000)}.wav")
            with open(path_to_wav, 'wb') as f:
                f.write(audio_data.getvalue())
            return path_to_wav

    def recognize_audio(self, wav_path):
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source)

        try:
            captcha_text = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            captcha_text = ""

        return captcha_text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bypass CAPTCHA for CTF")
    parser.add_argument('-i', action='store_true', help="Bypass image CAPTCHA")
    parser.add_argument('-a', action='store_true', help="Bypass audio CAPTCHA")
    parser.add_argument('-u', '--url', type=str, required=True, help="URL of CAPTCHA image or audio")

    args = parser.parse_args()

    solver = CaptchaSolver()

    if args.i:
        captcha_text = solver.bypass_image_captcha(args.url)
        print("Image Captcha:", captcha_text)
    elif args.a:
        wav_path = solver.bypass_audio_captcha(args.url)
        captcha_text = solver.recognize_audio(wav_path)
        print("Audio Captcha:", captcha_text)
    else:
        print("Select Captcha type for bypass (-i for image or -a for audio)")
