import sys
import requests
from bs4 import BeautifulSoup
from PyQt6 import QtWidgets

class Pencere(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.tl_miktarı = QtWidgets.QLineEdit()
        self.tl_miktarı.setPlaceholderText("TL MİKTARINIZ")
        self.dolar_karşılık = QtWidgets.QLineEdit()
        self.dolar_karşılık.setPlaceholderText("ALINABİLECEK DOLAR MİKTARI")
        self.dolar_karşılık.setReadOnly(True)  # Buraya kendi elimizle değer giremememiz için böyle yaptım.

        self.hesaplama_butonu = QtWidgets.QPushButton("HESAPLA")

        dikey = QtWidgets.QVBoxLayout()
        dikey.addWidget(self.tl_miktarı)
        dikey.addWidget(self.dolar_karşılık)
        dikey.addStretch()
        dikey.addWidget(self.hesaplama_butonu)
        self.setLayout(dikey)

        # Buton tıklanınca dolar_hesapla fonksiyonu çalışacak.
        self.hesaplama_butonu.clicked.connect(self.dolar_hesapla)

        self.tl_miktarı.setFixedHeight(40)
        self.dolar_karşılık.setFixedHeight(40)
        self.hesaplama_butonu.setFixedHeight(30)
        self.hesaplama_butonu.setFixedWidth(150)
        self.hesaplama_butonu.setStyleSheet("background-color : lightblue; color: purple;")
        self.setWindowTitle("DOLAR KURU BULMA")
        self.setGeometry(500, 100, 500, 500)

        self.show()

    def dolar_hesapla(self):
        try:
            # Web scraping işlemi
            url = "https://www.bloomberght.com/doviz/dolar"
            response = requests.get(url)
            html_icerigi = response.content
            soup = BeautifulSoup(html_icerigi, "html.parser")

            # Dolar kurunu bulma
            div = soup.find("div", {"class": "security-dolar"})
            span = div.find("span")

            if span:
                dolar_kuru = float(span.text.replace(",", "."))
                print(f"Anlık Dolar Kuru: {dolar_kuru} TL")

                # Hesaplama işlemi
                tl_miktari = float(self.tl_miktarı.text())
                dolar_miktari = tl_miktari / dolar_kuru
                self.dolar_karşılık.setText(f"{dolar_miktari:.2f} USD ALABİLİRSİNİZ !!!")
            else:
                self.dolar_karşılık.setText("Kur bulunamadı!")

        except Exception as e:
            print(f"Hata oluştu: {e}")
            self.dolar_karşılık.setText("Hata!")

# Uygulamayı başlat
app = QtWidgets.QApplication(sys.argv)
pencere = Pencere()
sys.exit(app.exec())
