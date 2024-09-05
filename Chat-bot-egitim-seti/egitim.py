from difflib import get_close_matches as yakin_sonuclari_getir
import json

def veritabanini_yukle():
    with open('veri.json', 'r') as dosya:
        return json.load(dosya)

def veri_yaz(veriler):
    with open('veri.json', 'w') as dosya:
        json.dump(veriler, dosya, indent=2)

def bot():
    veri = veritabanini_yukle()

    while True:
        soru = input('Siz: ')

        if soru == "kapat":
            print("Bot kapatıldı. Hoşça kal!")
            break

        gelen_sonuc = yakin_sonuc(soru, [soru_cevaplar["soru"] for soru_cevaplar in veri["sorular"]])

        if gelen_sonuc:
            verilecek_cevap = cevabini_bul(gelen_sonuc, veri)
            print(f"Bot: {verilecek_cevap}")
        else:
            yeni_cevap = input("Atlamak için 'atla' yazabilir ya da bir şey öğretebilirsiniz: ")

            if yeni_cevap != 'atla':
                veri["sorular"].append({
                    "soru": soru,
                    "cevap": yeni_cevap
                })
                veri_yaz(veri)
                print("Yeni bilgi eklendi.")
            else:
                print("Öğretmek için bir şey yazmadınız.")

def yakin_sonuc(soru, sorular):
    eslesen = yakin_sonuclari_getir(soru, sorular, n=1, cutoff=0.7)
    return eslesen[0] if eslesen else None

def cevabini_bul(soru, veri):
    for sorucevaplar in veri["sorular"]:
        if sorucevaplar["soru"] == soru:
            return sorucevaplar["cevap"]

if __name__ == '__main__':
    bot()
