import multiprocessing, sys
from PySide6.QtWidgets import QApplication


def main():
    QApplication(sys.argv)
    print(QApplication.clipboard().text())


if __name__ == '__main__':
    main()