from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout

class Modal(QDialog):
    def __init__(self, parent=None, result=None):
        super().__init__(parent=parent)
        self.result = result
        self.setWindowTitle('Resultado')
        self.setModal(True)
        self.label = QLabel(self.result)
        self.ok_button = QPushButton('Aceptar')
        self.ok_button.clicked.connect(self.accept)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

