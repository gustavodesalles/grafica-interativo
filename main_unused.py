import sys
from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QPushButton

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Teste')
window.setFixedWidth(1000)
window.setFixedHeight(800)

lista_objetos = QListWidget()
lista_objetos.insertItem(0, 'Alice')
lista_objetos.insertItem(1, 'Bob')

button_widget = QWidget(parent=window)

layout = QVBoxLayout()

QPushButton('Up')
layout.addWidget(lista_objetos, 200)
layout.addWidget(QPushButton('Up'))
layout.addWidget(QPushButton('Down'))
button_widget.setLayout(layout)
button_widget.setFixedWidth(70)
button_widget.setFixedHeight(80)

window.show()
sys.exit(app.exec())