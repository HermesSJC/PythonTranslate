from Widget import Widget
from PySide2.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)

    window = Widget()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()