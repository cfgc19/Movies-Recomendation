from Tkinter import *
from open_data import *
from sentiment_analysis import final_review
import tkMessageBox

class StartPage(Frame):

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.pack()
        btn_1 = Button(self,text = "Analyse existing review", command=lambda: controller.show_frame(Application))
        btn_1.pack()

        btn_2 = Button(self,text="Insert a new review")
        btn_2.pack()



root = Tk()
root.title("Sentiment Analysis")
root.geometry("400x100+300+300")

app = StartPage()

app.mainloop()
class Application(Frame):

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
        global user_id
        global review
        global sent_review
        sent_review = ""

        user_id = value1
        review = get_review(movie_name, user_id)

        self.S = Scrollbar(self)
        self.S.pack(side=RIGHT, fill=Y)
        self.review_text = Text(self,height=30, width=50)
        self.review_text.pack(side=BOTTOM, fill=Y)
        self.review_text.insert(END,review)
        self.S.config(command=self.review_text.yview)
        self.review_text.config(yscrollcommand=self.S.set)

        btn_sentiment = Button(text = "Sentiment", command = self.get_sentiment)
        btn_sentiment.pack()


    def createWidgets(self):

        global value
        global oml
        users_list=[""]

        optionList = get_movies("all")
        self.v = StringVar()
        self.v.set("Choose a movie")
        self.om = OptionMenu(self, self.v, *optionList, command=self.users_by_movie)
        self.om.pack(side=TOP, padx = 10, pady = 10)


        self.v1 = StringVar()
        self.v1.set("Choose a user")
        self.om1 = OptionMenu(self, self.v1, *users_list, command=self.show_review)
        self.om1.pack(side=TOP, padx = 10 , pady = 10)


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
root.title("Sentiment Analysis")
root.geometry("500x700+300+300")

app = Application(master=root)

app.mainloop()

