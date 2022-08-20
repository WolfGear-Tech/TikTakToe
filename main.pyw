# Use this file to build TikTakToe
from PyQt5 import QtWidgets
from style import style
from mainUi import Ui_form

version = "1.0.0"


class Extended_Ui_form(Ui_form):
    def initForm(self):
        pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(style())
    form = QtWidgets.QWidget()
    ui = Extended_Ui_form()
    ui.setupUi(form)
    form.show()
    ui.initForm()
    sys.exit(app.exec_())
