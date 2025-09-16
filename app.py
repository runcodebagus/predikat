# app.py
from flask import Flask, render_template, request
from model import load_artifacts, predict_grade

app = Flask(__name__)

# Load sekali di startup
load_artifacts()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/base')
def base():
    return render_template('base.html')

# (Matikan route /get kalau generate_response belum diimport)
# from process import generate_response
# @app.route("/get")
# def get_bot_response():
#     user_input = str(request.args.get('msg'))
#     result = generate_response(user_input)
#     return result

@app.route('/prediksi')   # hanya menampilkan form
def prediksi_page():
    return render_template('prediksi.html', hasil_prediksi=None)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/about')
def about():
    return render_template('about.html')

def _get_float(name):
    """Ambil angka dari form; izinkan desimal."""
    raw = request.form.get(name, "").strip()
    # Ganti koma ke titik kalau user pakai format Indonesia
    raw = raw.replace(",", ".")
    return float(raw)

@app.route("/predict", methods=["POST"])
def predict():
    # IPS sebaiknya float, bukan int
    ips1 = _get_float('ips1')
    ips2 = _get_float('ips2')
    ips3 = _get_float('ips3')
    ips4 = _get_float('ips4')
    ips5 = _get_float('ips5')
    ips6 = _get_float('ips6')
    ips7 = _get_float('ips7')
    ips8 = _get_float('ips8')

    data_baru = [ips1, ips2, ips3, ips4, ips5, ips6, ips7, ips8]

    hasil = predict_grade(data_baru)

    # render halaman yang sama, tampilkan hasil
    return render_template('prediksi.html',
                           hasil_prediksi=hasil,
                           form_values={
                               "ips1": ips1, "ips2": ips2, "ips3": ips3, "ips4": ips4,
                               "ips5": ips5, "ips6": ips6, "ips7": ips7, "ips8": ips8
                           })

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
