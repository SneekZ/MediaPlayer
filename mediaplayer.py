from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

from mainwindow import Ui_MainWindow


def timef(t):
    h, r = divmod(t, 3600000)
    m, r = divmod(r, 60000)
    s, _ = divmod(r, 1000)
    if h != 0:
        if s < 10:
            return "{}:{}:0{}".format(h, m, s)
        else:
            return "{}:{}:{}".format(h, m, s)
    else:
        if s < 10:
            return "{}:0{}".format(m, s)
        else:
            return "{}:{}".format(m, s)


class ViewerWindow(QMainWindow):
    state = pyqtSignal(bool)


class PlaylistModel(QAbstractListModel):
    def __init__(self, playlist):
        super(PlaylistModel, self).__init__()
        self.playlist = playlist

    def data(self, index, role):
        if role == Qt.DisplayRole:
            media = self.playlist.media(index.row())
            return media.canonicalUrl().fileName()

    def rowCount(self, index):
        return self.playlist.mediaCount()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.player = QMediaPlayer()

        self.player.play()

        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)

        self.viewer = ViewerWindow(self)
        self.viewer.setWindowFlags(self.viewer.windowFlags() | Qt.WindowStaysOnTopHint)
        self.viewer.setMinimumSize(QSize(480,360))

        videoWidget = QVideoWidget()
        self.viewer.setCentralWidget(videoWidget)
        self.player.setVideoOutput(videoWidget)

        self.playButton.pressed.connect(self.player.play)
        self.pauseButton.pressed.connect(self.player.pause)
        self.volumeSlider.valueChanged.connect(self.player.setVolume)

        self.viewButton.toggled.connect(self.toggle_viewer)
        self.viewer.state.connect(self.viewButton.setChecked)

        self.model = PlaylistModel(self.playlist)
        self.playlistView.setModel(self.model)
        self.playlist.currentIndexChanged.connect(self.cpp)

        self.player.durationChanged.connect(self.ut)
        self.player.positionChanged.connect(self.up)
        self.timeSlider.valueChanged.connect(self.player.setPosition)

        self.open_file_action.triggered.connect(self.openfile)

        self.setAcceptDrops(True)

        self.show()


    def openfile(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open mediafile", "", "*.mp3;*.mp4"
                                                                     ";*.mov")
        if path:
            self.playlist.addMedia(
                QMediaContent(
                    QUrl.fromLocalFile(path)
                )
            )

        self.model.layoutChanged.emit()

    def ut(self, mc):
        self.timeSlider.setMaximum(self.player.duration())
        duration = self.player.duration()

        if duration >= 0:
            self.totalTimeLabel.setText(timef(duration))

    def up(self):
        position = self.player.position()
        if position >= 0:
            self.currentTimeLabel.setText(timef(position))

        self.timeSlider.blockSignals(True)
        self.timeSlider.setValue(position)
        self.timeSlider.blockSignals(False)



    def cpp(self, i):
        if i > -1:
            ix = self.model.index(i)
            self.playlistView.setCurrentIndex(ix)

    def toggle_viewer(self, state):
        if state:
            self.viewer.show()
        else:
            self.viewer.hide()


if __name__ == '__main__':
    app = QApplication([])


    window = MainWindow()
    app.exec_()
