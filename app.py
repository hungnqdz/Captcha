from flask import Flask, render_template, request, send_file, session, url_for, redirect
import captcha_service
import gcloud_service

app = Flask(__name__)
app.secret_key = 'your_secret_key'
RECAPTCHA_SECRET_KEY = '6LeyInEqAAAAAFf5YooGZBQBO5XFb6u6KIYZUPMV'
API_KEY = 'AIzaSyBRNL8fe6imXQPPxNi15td7Rpvbky4EO-o'

@app.route('/captcha_audio')
def captcha_audio():
    captcha_text = captcha_service.generate_captcha_text(audio=True)
    session['captcha_text'] = captcha_text
    audio_data = captcha_service.generate_captcha_audio(captcha_text)
    return send_file(audio_data, mimetype='audio/wav')


@app.route('/captcha_image_page', methods=['GET'])
def image_captcha_page():
    return render_template('image_captcha.html')


@app.route('/audio_captcha_page', methods=['GET'])
def audio_captcha_page():
    captcha_text = captcha_service.generate_captcha_text()
    session['captcha_text'] = captcha_text
    return render_template('audio_captcha.html')


@app.route('/recaptchav3', methods=['GET'])
def recaptcha_page():
    return render_template('recaptcha_v3.html')


@app.route('/recaptchav2', methods=['GET'])
def recaptchav2_page():
    return render_template('recaptcha_v2.html')

@app.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@app.route('/captcha_image', methods=['GET'])
def captcha_image_generated():
    captcha_text = captcha_service.generate_captcha_text()
    session['captcha_text'] = captcha_text
    captcha_image = captcha_service.generate_captcha_image(captcha_text)
    return send_file(captcha_image, mimetype='image/png')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    captcha_input = request.form['captcha_input']
    captcha_text = session.get('captcha_text')

    if captcha_input == captcha_text:
        return 'Đăng nhập thành công!'
    else:
        return 'CAPTCHA không chính xác! Vui lòng thử lại.'


@app.route('/login_with_captcha_v3', methods=['POST'])
def login_with_captcha_v3():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    token = data.get('token')

    # Verify the reCAPTCHA token
    result = captcha_service.recaptcha_v3_verify(token, 'login')
    return result


@app.route('/login_with_captcha_v2', methods=['POST'])
def login_with_captcha_v2():
    username = request.form.get('username')
    password = request.form.get('password')
    recaptcha_response = request.form.get('g-recaptcha-response')
    verify_result = captcha_service.recaptcha_v2_verify(recaptcha_response)
    return verify_result


if __name__ == '__main__':
    app.run(debug=False)
