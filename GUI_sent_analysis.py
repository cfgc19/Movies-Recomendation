import Tkinter as tk     # python 2
import tkFont as tkfont  # python 2
from open_data import *
from sent_analysis import final_review
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

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="A tool for sentiment analysis of movie reviews", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Analyse existing review",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Insert a new review",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()

class PageOne(tk.Frame):

    def users_by_movie(self, value):
        global movie_name
        global users_list
        movie_name = value
        users_list = get_users_of_a_movie(value)
        menu = self.om1.children["menu"]
        menu.delete(0, "end")
        for value in users_list:
            menu.add_command(label=value, command=lambda v=value:self.show_review(v))

    def get_sentiment(self):
        sent_review = final_review(review)
        tkMessageBox.showinfo("Review's sentiment", sent_review)

    def show_review(self, value1):
        if self.review_text.winfo_exists():
            self.review_text.delete("1.0", "end")
        global user_id
        global review
        global sent_review
        sent_review = ""

        user_id = value1
        self.S.pack(side="right", fill="y")
        review = get_review(movie_name, user_id)
        self.review_text.pack(side="bottom", fill="y")
        self.review_text.insert("end",review)
        self.S.config(command=self.review_text.yview)
        self.review_text.config(yscrollcommand=self.S.set)

        self.btn_sentiment.pack()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Analyse existing review", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        global value
        global oml
        users_list=[""]

        optionList = get_movies("all")
        self.v = tk.StringVar()
        self.v.set("Choose a movie")
        self.om = tk.OptionMenu(self, self.v, *optionList, command=self.users_by_movie)
        self.om.pack(side="top", padx = 10, pady = 10)


        self.v1 = tk.StringVar()
        self.v1.set("Choose a user")
        self.om1 = tk.OptionMenu(self, self.v1, *users_list, command=self.show_review)
        self.om1.pack(side="top", padx = 10 , pady = 10)

        self.S = tk.Scrollbar(self)
        self.review_text = tk.Text(self, height=20, width=50)
        self.btn_sentiment = tk.Button(text = "Sentiment", command = self.get_sentiment)

class PageTwo(tk.Frame):

    def new_review(self, value):
        global movie_name
        global users_by_movie
        movie_name = value
        users_by_movie = get_users_of_a_movie(value)
        print(users_by_movie)

    def get_score(self):
        sent_review = final_review(self.v2.get())
        tkMessageBox.showinfo("Review's sentiment", sent_review)


    def user_already_reviewed(self):
        users_by_movie = get_users_of_a_movie(movie_name)
        for user in users_by_movie:
            if user == self.v1.get():
                tkMessageBox.showinfo("ERROR", "You already write a review about this movie.")
                self.quit()

        self.v2 = tk.StringVar()
        self.e1 = tk.Entry(self, textvariable=self.v2, width=100)
        self.e1.pack()
        self.v2.set("Insert your review...")

        self.button3 = tk.Button(self, text="Save review",command = self.get_score)
        self.button3.pack()



    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Insert a new review", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        optionList = get_movies("all")
        self.v = tk.StringVar()
        self.v.set("Choose a movie")
        self.om = tk.OptionMenu(self, self.v, *optionList, command=self.new_review)
        self.om.pack(side="top", padx = 10, pady = 10)

        self.v1 = tk.StringVar()
        self.e = tk.Entry(self, textvariable=self.v1)
        self.e.pack()
        self.v1.set("user ID")

        self.button2 = tk.Button(self, text="Next",command = self.user_already_reviewed)
        self.button2.pack()



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

