import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *


class myclass:
    def __init__(self, window):
        self.firstClick = 0
        self.response_json = []
        self.window = window
        self.canvas = None
        self.eSpotifyLink = Entry(window)
        self.eSpotifyLink.pack()
        self.eSpotifyLink.insert(
            # 0, "https://open.spotify.com/playlist/1kw9wSUDPWsAEDCGKAMkGU?si=ace2030540ad4fae")
            0, "https://open.spotify.com/playlist/6tc6fT8N9907y4Wqwb5FDS?si=6b887c9ca1b14ffc")

        self.eToken = Entry(window)
        self.eToken.pack()
        self.eToken.insert(1, "BQDarUoWvUrKCU9XCPEwhP2RO7fcqXSOwM5q76fLrsQz4NfAwlJhE2_fAvNMLmzBSE4P4zI2cMcNKpV0SU1bZFv28aC9Ao1mZ0izU2SqK5cInPbccg7AKT0mRsp6RAMFGPtFOgJZuU-w0lOIsQJvmkhL7IDga7gTOY4Qrz11KGzdnwt0KjIKPGKfNGQmg8jtt4YsdcPpex5M8KkvJ0eFukspDKFEC7q_SNzvydVzDzr_iW73xYKybywgK3p06kz89ASr8CTZi1AI24c7-CkuXQ")

        self.button = Button(window, text="Analyse", command=self.analyse)
        self.button.pack()

    def clear_space(self):
        self.canvas._tkcanvas.destroy()

    def analyse(self):
        self.playlistId = self.eSpotifyLink.get().split(
            "playlist/")[1].split("?")[0]
        self.token = self.eToken.get()

        counter = {}
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
            if name in counter.keys():
                counter[name] += 1
            else:
                counter[name] = 1

        counter = dict(
            sorted(counter.items(), key=lambda item: item[1], reverse=True))
        fig, ax = plt.subplots()
        # if self.firstClick:
        #     chart.get_tk_widget().destroy()
        # firstClick = 1
        self.chart = FigureCanvasTkAgg(fig, root)
        self.chart.get_tk_widget().pack(side="top", fill='both', expand=True)
        ax.barh(list(range(len(counter))), list(
            counter.values()), align="center")
        ax.invert_yaxis()
        ax.set_xticks(list(range(0, 100, 3)))
        ax.set_xticks(list(range(100)), minor="True")
        ax.xaxis.grid(which='major', alpha=0.5)
        ax.xaxis.grid(which='minor', alpha=0.2)
        plt.yticks(range(len(counter)), list(counter.keys()))
        plt.plot()
        plt.show()

    def requestNames(self, offset):
        url = f"https://api.spotify.com/v1/playlists/{self.playlistId}/tracks?fields=items(track(artists(name)))&offset={offset}"
        response = requests.get(url,
                                headers={
                                    "Content-Type": "application.json",
                                    "Authorization": f"Bearer {self.token}"
                                }
                                )
        self.response_json = self.response_json + response.json()["items"]


if __name__ == "__main__":
    root = Tk()
    classinstance = myclass(root)
    root.mainloop()
