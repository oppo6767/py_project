from pet_widget import PetWidget 
from PySide6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Windows = PetWidget()
    Windows.show()
    app.exec()