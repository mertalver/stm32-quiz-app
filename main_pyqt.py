import sys
import serial
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import pyqtSlot
from qt_material import apply_stylesheet

# Global değişkenler
ser = None  # Serial port nesnesi
running = True  # Seri port thread kontrolü


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STM32 Soru/Cevap Uygulaması")
        self.resize(400, 300)

        # Ana widget ve layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Soru Label
        self.question_label = QLabel("Sorunuz: ---")
        self.layout.addWidget(self.question_label)

        # Durum Label
        self.status_label = QLabel("Durum: ---")
        self.layout.addWidget(self.status_label)

        # Geri sayım Label
        self.countdown_label = QLabel("Kalan süre: ---")
        self.layout.addWidget(self.countdown_label)

        # Kullanıcı cevabı için Entry ve Gönder butonu
        self.entry = QLineEdit()
        self.layout.addWidget(self.entry)

        self.send_button = QPushButton("Cevabı Gönder")
        self.send_button.clicked.connect(self.send_answer)
        self.layout.addWidget(self.send_button)

        # Yeni Soru Butonu
        self.new_question_button = QPushButton("Yeni Soru")
        self.new_question_button.clicked.connect(self.request_new_question)
        self.layout.addWidget(self.new_question_button)

        # Sonuçları Gör Butonu
        self.result_button = QPushButton("Sonucu Gör")
        self.result_button.clicked.connect(self.send_result_request)
        self.layout.addWidget(self.result_button)

        # Seri port okuma thread'i başlat
        self.thread = threading.Thread(target=self.read_serial_thread, daemon=True)
        self.thread.start()

        # Pencere kapatma olayını ele al
        self.closeEvent = self.on_closing

    def read_serial_thread(self):
        """Seri porttan gelen mesajları okuma."""
        global running
        while running:
            if ser and ser.in_waiting > 0:
                try:
                    line = ser.readline().decode(errors='ignore').strip()
                    print(line)
                    if line.startswith("Sorunuz"):
                        self.update_label(self.question_label, line)
                    elif line.startswith("Kalan sure"):
                        self.update_label(self.countdown_label, line)
                    elif line.startswith("DOGRU"):
                        self.update_label(self.question_label, line)
                    else:
                        self.update_label(self.status_label, line)
                except Exception as e:
                    self.update_label(self.status_label, f"Hata: {e}")

    def update_label(self, label, text):
        """Label güncellemesi (Qt'de thread-safe)."""
        label.setText(text)

    @pyqtSlot()
    def send_answer(self):
        """Kullanıcı cevabını STM32'ye gönder."""
        answer = self.entry.text()
        if answer:
            try:
                ser.write((answer + "\n").encode())  # STM32 \n bekliyorsa
                self.entry.clear()
                self.status_label.setText("Cevap gönderildi.")
            except Exception as e:
                self.status_label.setText(f"Hata: {e}")

    @pyqtSlot()
    def send_result_request(self):
        """Sonuçları talep et."""
        try:
            ser.write(("Sonucu Gor").encode())
            self.status_label.setText("Sonuçlar talep edildi.")
        except Exception as e:
            self.status_label.setText(f"Hata: {e}")

    @pyqtSlot()
    def request_new_question(self):
        """Yeni soru talebi gönder."""
        try:
            ser.write(("Yeni Soru").encode())
            self.status_label.setText("Yeni soru talep edildi.")
        except Exception as e:
            self.status_label.setText(f"Hata: {e}")

    def on_closing(self, event):
        """Uygulamayı kapatırken thread’i sonlandır."""
        global running
        running = False
        if ser and ser.is_open:
            ser.close()
        event.accept()


def main():
    global ser

    # 1) Seri portu aç
    try:
        ser = serial.Serial(port='COM5', baudrate=115200, timeout=0.5)
    except Exception as e:
        print(f"Seri port hatası: {e}")
        return

    # 2) PyQt uygulamasını başlat
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')  # Qt Material teması uygula
    window = MainWindow()
    window.show()

    # 3) Uygulama döngüsü
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
