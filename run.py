import sys
import time
from PyQt5.QtWidgets import QMainWindow, QSplashScreen, QApplication
from PyQt5.QtGui import QPixmap, QPainter, QMovie
from lib import main


class mywindow(QMainWindow, main.Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)


class MovieSplashScreen(QSplashScreen):
    def __init__(self, movie, parent=None):
        movie.jumpToFrame(0)
        pixmap = QPixmap(movie.frameRect().size())

        QSplashScreen.__init__(self, pixmap)
        self.movie = movie
        self.movie.frameChanged.connect(self.repaint)

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    movie = QMovie("style/loading.gif")
    splash = MovieSplashScreen(movie)
    splash.show()
    splash.movie.start()
    start = time.time()
    while movie.state() == QMovie.Running and time.time() < start + 2:
        app.processEvents()
    window = mywindow()
    window.show()
    splash.finish(window)
    sys.exit(app.exec_())
