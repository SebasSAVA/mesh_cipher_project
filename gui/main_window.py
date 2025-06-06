import sys
import os

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QToolButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

from gui.validation import validate_key, validate_message
from mesh_cipher.core import encrypt, decrypt  # Usamos core.py

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("M.E.S.H.")
        self.setGeometry(100, 100, 600, 400)

        # Ruta base para iconos
        base_path = os.path.dirname(os.path.abspath(__file__))

        # Cargar icono candado para ventana (igual)
        icon_path = os.path.join(base_path, "icon", "unlock-keyhole-solid.svg")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"No se encontró el icono de ventana: {icon_path}")

        # Carga y aplica CSS
        try:
            css_path = os.path.join(base_path, "styles.css")
            with open(css_path, "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"No se pudo cargar el estilo CSS: {e}")

        # Widgets
        self.label_message = QLabel("Mensaje:")
        self.text_message = QTextEdit()

        self.label_key = QLabel("Clave:")
        self.input_key = QLineEdit()
        self.input_key.setEchoMode(QLineEdit.Password)

        # Botón para mostrar/ocultar clave
        self.toggle_password_btn = QToolButton(self.input_key)

        # Cargar iconos SVG y escalarlos para que sean más grandes y sin fondo
        eye_open_path = os.path.join(base_path, "icon", "eye-solid.svg")
        eye_closed_path = os.path.join(base_path, "icon", "eye-slash-solid.svg")

        icon_size = 24  # Tamaño deseado para icono ojo (más grande)

        if os.path.exists(eye_open_path):
            pixmap_open = QPixmap(eye_open_path).scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.eye_open_icon = QIcon(pixmap_open)
        else:
            self.eye_open_icon = self.style().standardIcon(QStyle.SP_DialogYesButton)
            print(f"No se encontró icono ojo abierto: {eye_open_path}")

        if os.path.exists(eye_closed_path):
            pixmap_closed = QPixmap(eye_closed_path).scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.eye_closed_icon = QIcon(pixmap_closed)
        else:
            self.eye_closed_icon = self.style().standardIcon(QStyle.SP_DialogNoButton)
            print(f"No se encontró icono ojo cerrado: {eye_closed_path}")

        # Estado inicial: campo oculto, botón con ojo abierto
        self.toggle_password_btn.setIcon(self.eye_open_icon)
        self.toggle_password_btn.setCursor(Qt.PointingHandCursor)

        # Quitar fondo visible con CSS
        self.toggle_password_btn.setStyleSheet("border: none; padding: 0px; background: transparent;")

        self.toggle_password_btn.setToolTip("Mostrar/Ocultar clave")
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)

        # Ajustar padding para botón dentro del QLineEdit
        frame_width = self.input_key.style().pixelMetric(self.input_key.style().PM_DefaultFrameWidth)
        btn_size = self.toggle_password_btn.sizeHint()

        # Fijar tamaño del botón al tamaño del ícono
        self.toggle_password_btn.setFixedSize(icon_size, icon_size)

        self.input_key.setStyleSheet(f"QLineEdit {{ padding-right: {icon_size + frame_width + 5}px; }}")

        # Posicionar el botón (se llama a move también en resizeEvent)
        self.toggle_password_btn.move(
            self.input_key.rect().right() - icon_size - frame_width,
            (self.input_key.rect().bottom() - icon_size + 1) // 2
        )

        self.btn_encrypt = QPushButton("Codificar")
        self.btn_decrypt = QPushButton("Decodificar")
        self.btn_decrypt.setObjectName("btn_decrypt")  # Para CSS rojo

        self.label_result = QLabel("Resultado:")
        self.text_result = QTextEdit()
        self.text_result.setReadOnly(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_message)
        layout.addWidget(self.text_message)
        layout.addWidget(self.label_key)
        layout.addWidget(self.input_key)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_encrypt)
        btn_layout.addWidget(self.btn_decrypt)
        layout.addLayout(btn_layout)

        layout.addWidget(self.label_result)
        layout.addWidget(self.text_result)

        self.setLayout(layout)

        # Conexiones
        self.btn_encrypt.clicked.connect(self.handle_encrypt)
        self.btn_decrypt.clicked.connect(self.handle_decrypt)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        icon_size = 24
        btn_size = self.toggle_password_btn.size()
        frame_width = self.input_key.style().pixelMetric(self.input_key.style().PM_DefaultFrameWidth)
        self.toggle_password_btn.move(
            self.input_key.rect().right() - icon_size - frame_width,
            (self.input_key.rect().bottom() - icon_size + 1) // 2
        )

    def toggle_password_visibility(self):
        if self.input_key.echoMode() == QLineEdit.Password:
            self.input_key.setEchoMode(QLineEdit.Normal)
            self.toggle_password_btn.setIcon(self.eye_closed_icon)
        else:
            self.input_key.setEchoMode(QLineEdit.Password)
            self.toggle_password_btn.setIcon(self.eye_open_icon)

    def show_error(self, message: str):
        QMessageBox.warning(self, "Error", message)

    def handle_encrypt(self):
        message = self.text_message.toPlainText()
        key = self.input_key.text()

        valid_key, key_msg = validate_key(key)
        if not valid_key:
            self.show_error(key_msg)
            return

        valid_msg, msg_msg = validate_message(message)
        if not valid_msg:
            self.show_error(msg_msg)
            return

        try:
            result = encrypt(message, key)
            self.text_result.setPlainText(result)
        except Exception as e:
            self.show_error(f"Error en cifrado: {str(e)}")

    def handle_decrypt(self):
        hex_input = self.text_message.toPlainText()
        key = self.input_key.text()

        valid_key, key_msg = validate_key(key)
        if not valid_key:
            self.show_error(key_msg)
            return

        if not hex_input:
            self.show_error("Debe ingresar un texto cifrado en hexadecimal.")
            return

        try:
            plaintext = decrypt(hex_input, key)
            self.text_result.setPlainText(plaintext)
        except Exception as e:
            self.show_error(f"Error en descifrado: {str(e)}")

def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
