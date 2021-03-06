import Tkinter as tk     # python 2
import tkFont as tkfont  # python 2
from recommender_system import *

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Courier', size=12, weight="bold")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        frame = StartPage(parent=container, controller=self)
        frame.grid(row=0, column=0, sticky="nsew")

class StartPage(tk.Frame):

    def recommender_film(self,value):
        name_movies_list, movies_already_like, similiar_users= recommender_film(value,option=3, clustering_option='kmeans') #clusterion_option : kmeans, hierarchical, dbscan
        text = ""
        for movie in movies_already_like:
            text = text + movie + "\n"

        if self.review_text.winfo_exists():  # apagar o texto se houver texto nas caixas de texto
            self.review_text.delete("1.0", "end")
        if self.text1.winfo_exists():
            self.text1.delete("1.0", "end")
        if self.text2.winfo_exists():
            self.text2.delete("1.0", "end")
        if self.text3.winfo_exists():
            self.text3.delete("1.0", "end")

        self.review_text.pack(side="top", fill="y")

        print1 = name_movies_list[0]
        self.review_text.insert("end", print1)

        self.review_text.config(yscrollcommand=self.S.set)

        self.label.pack(side="top", fill="x", pady=10)

        self.text1.pack(side="top", fill="y")
        self.text1.insert("end", similiar_users[0])

        self.label2.pack(side="top", fill="x", pady=10)
        self.text2.pack(side="top", fill="y")
        self.text2.insert("end", text)

        print2 = name_movies_list[1] + "\n" + name_movies_list[2]
        self.label3.pack(side="top", fill="x", pady=10)
        self.text3.pack(side="top", fill="y")
        self.text3.insert("end", print2)

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="A tool for recommendatiom of movies", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        optionList = get_all_users()
        self.v = tk.StringVar()
        self.v.set("Choose a user")
        self.om = tk.OptionMenu(self, self.v, *optionList, command=self.recommender_film)
        self.om.pack(side="top", padx = 10, pady = 10)

        # recommended movie
        self.S = tk.Scrollbar(self)
        self.review_text = tk.Text(self, height=3, width=30)

        # similar user
        self.label = tk.Label(self, text="Seems that you have similar tastes to...", font='courier')
        self.text1 = tk.Text(self, height=3, width=30)

        # movies liked
        self.label2 = tk.Label(self, text="You already like: ", font='courier')
        self.text2 = tk.Text(self, height=4, width=30)

        # other recommended movies
        self.label3 = tk.Label(self, text="You will possibly like: ", font='courier')
        self.text3 = tk.Text(self, height=4, width=30)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

