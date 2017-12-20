import Tkinter as tk     # python 2
import tkFont as tkfont  # python 2
from open_data import *
from recommender_system import *
from sent_analysis_final import final_review
import tkMessageBox

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
        name_film, similar_user = recommender_film(value,1)
        if self.review_text.winfo_exists():
            self.review_text.delete("1.0", "end")
        if self.text1.winfo_exists():
            self.text1.delete("1.0", "end")

        self.S.pack(side="right", fill="y")

        self.review_text.pack(side="top", fill="y")
        self.review_text.insert("end",name_film)

        self.S.config(command=self.review_text.yview)
        self.review_text.config(yscrollcommand=self.S.set)

        self.label.pack(side="top", fill="x", pady=10)

        self.S1.pack(side="right", fill="y")

        self.text1.pack(side="top", fill="y")
        self.text1.insert("end", similar_user)

        self.S1.config(command=self.text1.yview)
        self.text1.config(yscrollcommand=self.S1.set)

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

        self.S = tk.Scrollbar(self)
        self.review_text = tk.Text(self, height=5, width=30)

        self.label = tk.Label(self, text="Seems that you have similar tastes to...", font='courier')
        self.S1 = tk.Scrollbar(self)
        self.text1 = tk.Text(self, height=5, width=30)



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

