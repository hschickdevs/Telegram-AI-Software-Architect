from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
import sys

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle('Stock Simulator')
window.setGeometry(100, 100, 400, 200)

label = QLabel('Click the button to simulate stock return', window)
label.move(50, 50)

button = QPushButton('Simulate', window)
button.move(150, 100)

window.show()
sys.exit(app.exec_())