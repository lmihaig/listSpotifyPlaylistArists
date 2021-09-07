import sys
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np


class listSpotifyPlaylistArists(QtWidgets.QMainWindow):
    def __init__(self):
        if not QtWidgets.QApplication.instance():
            self.app = QtWidgets.QApplication(sys.argv)
        else:
            self.app = QtWidgets.QApplication.instance()

        super().__init__()
        QtWidgets.QMainWindow.__init__(self)
        self.firstClick = 0
        self.response_json = []
        self.widget = QtWidgets.QWidget()
        self.initUI()

        self.show()
        self.app.exec_()

    def initUI(self):
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QtWidgets.QGridLayout())

        self.widget.layout().setContentsMargins(0, 0, 0, 0)
        self.widget.layout().setSpacing(0)

        self.setWindowTitle("listSpotifyPlaylistArists")
        self.setWindowIcon(QtGui.QIcon('listSpotifyPlaylistArists.png'))

        self.playlistLinktext = QtWidgets.QLineEdit(
            self.widget, placeholderText="Spotify Playlist Link")
        self.widget.layout().addWidget(self.playlistLinktext, 0, 0)
        self.tokentext = QtWidgets.QLineEdit(
            self.widget, placeholderText="Token")
        self.widget.layout().addWidget(self.tokentext, 1, 0)
        self.analyseButton = QtWidgets.QPushButton(
            "Analyse", clicked=self.analyse)
        self.widget.layout().addWidget(self.analyseButton, 2, 0)

    def analyse(self):
        self.playlistId = self.playlistLinktext.text().split(
            "playlist/")[1].split("?")[0]
        self.token = self.tokentext.text()

        self.counter = {}
        numberofItems = requests.get(f"https://api.spotify.com/v1/playlists/{self.playlistId}/tracks?fields=total",
                                     headers={
                                         "Content-Type": "application.json",
                                         "Authorization": f"Bearer {self.token}"
                                     }
                                     ).json()["total"]
        iterations = (numberofItems // 100) + 1

        for i in range(iterations):
            self.requestNames(i*100)

        for i in self.response_json:
            name = i["track"]["artists"][0]["name"]
            if name in self.counter.keys():
                self.counter[name] += 1
            else:
                self.counter[name] = 1
        self.counter = dict(
            sorted(self.counter.items(), key=lambda item: item[1], reverse=True))
        self.plotGraph()

    def plotGraph(self):
        self.widget.layout().setColumnStretch(0, 1)
        self.widget.layout().setColumnStretch(1, 6)

        max_songs = next(iter(self.counter.values())) + 1

        if self.firstClick:
            self.widget.layout().removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None
            self.widget.layout().removeWidget(self.clipboardButton)
            self.clipboardButton.deleteLater()
            self.clipboardButton = None

        self.firstClick = 1
        self.clipboardButton = QtWidgets.QPushButton(self)
        self.clipboardButton.setText("Copy to Clipboard")
        self.clipboardButton.clicked.connect(self.copytoclipboard)
        self.widget.layout().addWidget(self.clipboardButton, 3, 0)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.ax.barh(list(range(len(self.counter))), list(
            self.counter.values()), align="center", color="#1DB954")

        self.ax.bar_label(self.ax.containers[0], label_type='edge')
        self.ax.set_xticks(list(range(0, max_songs, 3)))
        self.ax.set_xticks(list(range(max_songs)), minor="True")
        self.ax.xaxis.grid(which='major', alpha=0.5)
        self.ax.xaxis.grid(which='minor', alpha=0.2)
        plt.yticks(range(len(self.counter)), list(self.counter.keys()))

        self.canvas.draw()
        self.widget.layout().addWidget(self.canvas, 4, 0)

        self.scroll = QtWidgets.QScrollBar(QtCore.Qt.Vertical)
        self.step = 0.1
        self.setupSlider()
        self.widget.layout().addWidget(self.scroll, 4, 1, 1, 1)

    def setupSlider(self):
        self.lims = np.array(self.ax.get_ylim())
        self.scroll.setPageStep(int(self.step*100))
        self.scroll.actionTriggered.connect(self.update)
        self.update()

    def update(self, evt=None):
        r = self.scroll.value()/((1+self.step)*100)
        l1 = self.lims[0]+r*np.diff(self.lims)
        l2 = l1 + np.diff(self.lims)*self.step
        self.ax.set_ylim(l1, l2)
        self.ax.invert_yaxis()
        self.fig.canvas.draw_idle()

    def requestNames(self, offset):
        url = f"https://api.spotify.com/v1/playlists/{self.playlistId}/tracks?fields=items(track(artists(name)))&offset={offset}"
        response = requests.get(url,
                                headers={
                                    "Content-Type": "application.json",
                                    "Authorization": f"Bearer {self.token}"
                                }
                                )
        self.response_json = self.response_json + response.json()["items"]

    def copytoclipboard(self):
        QtWidgets.QApplication.clipboard().clear()
        formatted = ""
        for i in self.counter:
            formatted += f"{self.counter[i]} songs from {i}\n"
        QtWidgets.QApplication.clipboard().setText(formatted)


if __name__ == "__main__":
    appWindow = listSpotifyPlaylistArists()
