from typing import Counter
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.widgets import Slider
from tkinter import *


class listSpotifyPlaylistArists:
    def __init__(self, window):
        self.firstClick = 0
        self.response_json = []
        self.canvas = None
        self.window = window
        self.window.iconbitmap("listSpotifyPlaylistArists.ico")
        self.window.wm_title("listSpotifyPlaylistArists")
        self.eSpotifyLink = Entry(self.window)
        self.eSpotifyLink.pack()
        self.eSpotifyLink.insert(
            0, "https://open.spotify.com/playlist/1kw9wSUDPWsAEDCGKAMkGU?si=ace2030540ad4fae")
        # 0, "https://open.spotify.com/playlist/6tc6fT8N9907y4Wqwb5FDS?si=6b887c9ca1b14ffc")

        self.eToken = Entry(self.window)
        self.eToken.pack()
        self.eToken.insert(1, "BQAXvbD5v1A4LF8Xhj6votX2QkUujqgrYhVu3UARLSoFPJ8REKfCmZKCV-xkVA6dROx0-_6ykN9aV0My9ZdDsfH1Bc1Y0_aPGtDyPztvzuvfY9dGFucSiORU7z6huGLXRmCRDAMf6p1nIi8NYXWr-HZdGoFzCKdB1w23PmlZsCKsd2taNeM9IBLbcEyqjIJ8JazfOe8-h7zqvvvTv1aKw6RIx-9RIEGr1opHvTpzR7OGnuS5NYF-ZpMxZyRwJdsyT2eCnMXEL1Wc-zYOBhP1PA")

        self.button = Button(self.window, text="Analyse", command=self.analyse)
        self.button.pack()

    def analyse(self):
        self.playlistId = self.eSpotifyLink.get().split(
            "playlist/")[1].split("?")[0]
        self.token = self.eToken.get()

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

        fig, ax = plt.subplots()
        if self.firstClick:
            self.chart.get_tk_widget().destroy()
            self.clipboardButton.destroy()
        self.firstClick = 1
        self.clipboardButton = Button(
            self.window, text="Copy to Clipboard", command=self.copytoclipboard)
        self.clipboardButton.pack()
        self.chart = FigureCanvasTkAgg(fig, root)
        self.chart.get_tk_widget().pack(side="top", fill='both', expand=True)
        ax.barh(list(range(len(self.counter))), list(
            self.counter.values()), align="center", color="#1DB954")
        for i, v in enumerate(list(self.counter.values())):
            ax.text(v + 0.08, i + .25, str(v),
                    color='black', fontweight='bold')
        ax.invert_yaxis()
        ax.set_xticks(list(range(0, 100, 3)))
        ax.set_xticks(list(range(100)), minor="True")
        ax.xaxis.grid(which='major', alpha=0.5)
        ax.xaxis.grid(which='minor', alpha=0.2)
        plt.yticks(range(len(self.counter)), list(self.counter.keys()))
        plt.plot()
        plt.show()
        # toolbar = NavigationToolbar2Tk(self.chart, root)
        # toolbar.update()
        # self.chart.get_tk_widget().pack(side="top", fill='both', expand=True)
        # scrollbar = Scrollbar(master=root, orient=VERTICAL)
        # scrollbar.pack(side="right", fill=X)
        # scrollbar["command"] = self.chart.get_tk_widget().yview
        # self.chart.get_tk_widget()["yscrollcommand"] = scrollbar.set

        # self.vbar = Scrollbar(orient=VERTICAL)
        # self.vbar.config(command=self.canvas.get_tk_widget().yview)

        # vbar = Scrollbar(master=root, orient=VERTICAL)
        # vbar.pack(side=RIGHT, fill=Y)
        # vbar.config(command=self.canvas.yview)
        # self.config(yscrollcommand=vbar.set)

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
        root.clipboard_clear()
        formatted = ""
        for i in self.counter:
            formatted += f"{self.counter[i]} songs from {i}\n"
        root.clipboard_append(formatted)
        root.update()


if __name__ == "__main__":
    root = Tk()
    classinstance = listSpotifyPlaylistArists(root)
    root.mainloop()
