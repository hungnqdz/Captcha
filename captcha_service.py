import requests
from captcha.image import ImageCaptcha
from captcha.audio import AudioCaptcha

from io import BytesIO

RECAPTCHA_SECRET_KEY = '6LeyInEqAAAAAFf5YooGZBQBO5XFb6u6KIYZUPMV'
SITE_KEY_CAPTCHA_V3 = '6LeF6m0qAAAAAF6dO3c9-zzo6eqoZ3xLs5P4bvQV'
API_KEY = 'AIzaSyBRNL8fe6imXQPPxNi15td7Rpvbky4EO-o'
url_v3 = f"https://recaptchaenterprise.googleapis.com/v1/projects/captcha-1730109587017/assessments?key={API_KEY}"
url_v2 = 'https://www.google.com/recaptcha/api/siteverify'
def recaptcha_v2_verify(recaptcha_response):
    data = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    verify_response = requests.post(url_v2, data=data)
    result = verify_response.json()
    return result


def recaptcha_v3_verify(token, action):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "event": {
            "token": token,
            "siteKey": "6LeF6m0qAAAAAF6dO3c9-zzo6eqoZ3xLs5P4bvQV",
            "expectedAction": action
        }
    }
    verify_response = requests.post(url_v3, json=payload, headers=headers)
    result = verify_response.json()
    return result


def generate_captcha_text(audio=False):
    if not audio:
        captcha_text = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
    else:
        captcha_text = ''.join(random.choices('0123456789', k=4))
    return captcha_text


def generate_captcha_image(captcha_text):
    image = ImageCaptcha(width=200, height=100)
    image_data = BytesIO()
    captcha_image = image.generate_image(captcha_text)
    captcha_image.save(image_data, format='PNG')
    image_data.seek(0)
    return image_data


def generate_captcha_audio(captcha_text):
    audio_captcha = AudioCaptcha()
    data = audio_captcha.generate(captcha_text)
    audio_data = BytesIO(data)
    audio_data.seek(0)
    return audio_data
