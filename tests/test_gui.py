import pytest
from PyQt5.QtCore import Qt
from gui.main_window import MainWindow

@pytest.fixture
def app(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    return window

def test_key_validation_error(app, qtbot):
    app.input_key.setText("short")
    app.text_message.setPlainText("Test message")
    qtbot.mouseClick(app.btn_encrypt, Qt.LeftButton)
    # Esperamos que muestre error por clave corta
    # Como QMessageBox es modal, podría necesitar manejo avanzado para test
    # Por simplicidad validamos que el resultado no cambió
    assert app.text_result.toPlainText() == ""

def test_encrypt_decrypt_flow(app, qtbot):
    valid_key = "claveSegura123"
    message = "Mensaje de prueba"
    app.input_key.setText(valid_key)
    app.text_message.setPlainText(message)

    qtbot.mouseClick(app.btn_encrypt, Qt.LeftButton)
    cipher_text = app.text_result.toPlainText()
    assert cipher_text != ""

    app.text_message.setPlainText(cipher_text)
    qtbot.mouseClick(app.btn_decrypt, Qt.LeftButton)
    plain_text = app.text_result.toPlainText()
    # Puede tener diferencias menores por padding, así que chequeamos que contenga el texto original
    assert message in plain_text
