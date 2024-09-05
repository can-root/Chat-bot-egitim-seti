from flask import Flask, render_template, request, jsonify
from difflib import get_close_matches
import json
from gtts import gTTS
from playsound import playsound
import os

app = Flask(__name__)

def veritabanini_yukle():
    with open('veri.json', 'r') as dosya:
        return json.load(dosya)

def seslendirme(mesaj):
    tts = gTTS(text=mesaj, lang='tr')
    tts.save("temp.mp3")
    playsound("temp.mp3")
    os.remove("temp.mp3")

def yakin_sonuc(soru, sorular):
    eslesen = get_close_matches(soru, sorular, n=1, cutoff=0.7)
    return eslesen[0] if eslesen else None

def cevabini_bul(soru, veri):
    for sorucevaplar in veri["sorular"]:
        if sorucevaplar["soru"] == soru:
            return sorucevaplar["cevap"]
    return "Bu konu hakkında bilgim yok."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/soru', methods=['POST'])
def soru():
    veri = veritabanini_yukle()
    soru = request.form['soru']
    gelen_sonuc = yakin_sonuc(soru, [soru_cevaplar["soru"] for soru_cevaplar in veri["sorular"]])

    if gelen_sonuc:
        verilecek_cevap = cevabini_bul(gelen_sonuc, veri)
    else:
        verilecek_cevap = "Bu konu hakkında bilgim yok."

    seslendirme(verilecek_cevap)
    return jsonify({"cevap": verilecek_cevap})

if __name__ == '__main__':
    app.run(debug=True)
