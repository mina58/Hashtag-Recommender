import sys
sys.path.append(sys.path[0] + "\\..\\")

from NLP.RecommendationEngine import RecommendationEngine
from NLP.files_reader import *

data_files = [new_US_file, new_UK_file, new_AUS_file, new_CAN_file, new_IR_file]
engine = RecommendationEngine(data_files, 15)
top_trends = engine.get_top_trends()
top_hashtags = engine.get_top_hashtags()


def recommend():
    tweet = tweet_text.get("1.0", "end-1c")
    print(tweet)
    hashtags = engine.recommend_hashtags(tweet)
    hashtag_box.delete(0, END)
    confidence_box.delete(0, END)
    for i in range(len(hashtags)):
        hashtag_box.insert(i, hashtags[i][0])
        confidence_box.insert(i, hashtags[i][1])
        hashtag_box.config(fg=labelFont)
        confidence_box.config(fg=labelFont)



import tkinter
from tkinter import *

window = Tk()
window.resizable(FALSE,FALSE)
window.title("Hashtag Recommender ")
background = "#2C3333"
textarea = "#2E4F4F"
labelFont = "#CBE4DE"
label4 ="#0E8388"
# window.geometry("920x920")
title_font = ("Helvetica", 20, "bold")
window.config(bg=background)
# frame_title = tkinter.Frame(window)
tweet_label = tkinter.Label(window, text="Enter your Tweet:", font=title_font, fg=labelFont, bg=background)
tweet_label.grid(row=0, column=0, padx=9, pady=9, columnspan=4, sticky='w')
tweet_text = Text(window, height=9, width=60,bg=textarea, fg=labelFont, font="Arial")
tweet_text.grid(row=1, column=0, padx=9, pady=9, columnspan=4, sticky='n')
recommend_button = Button(window, text="Recommend", bg=label4, command=recommend, fg=labelFont).grid(row=2, column=1, columnspan=2,
                                                                                                     padx=9, pady=9, sticky='e')
# frame_output = tkinter.Frame(window)
# scrollbar = tkinter.Scrollbar(window)
hashtag_label = Label(window, text="Hashtag: ", font=("Helvetica", 20, "bold"), bg=background, fg=labelFont).grid(row=3, column=0,
                                                                                                                  padx=9, pady=9,
                                                                                                                  sticky='w')
hashtag_box = Listbox(window, width=25, font="Arial", bg=textarea, borderwidth=0)
hashtag_box.grid(row=4, column=0, padx=9, pady=9, sticky='nw')
confidence_label = Label(window, text="Confidence: ", font=("Helvetica", 20, "bold"), bg=background, fg=labelFont)
confidence_label.grid(row=3, column=1, padx=9, pady=9, columnspan=2, sticky='w')
confidence_box = Listbox(window, width=25, font="Arial", bg=textarea, borderwidth=0)
confidence_box.grid(row=4, column=1, padx=9, pady=9, sticky='nw')
# for i in range(len(hastags)):
#     hashtag_box.insert(i,hastags[i])
# for index in range(len(confidence)):
#     confidence_box.insert(index,confidence[index])
# canvas = Canvas(window, height=1500, width=1500)
# canvas.create_line(700,0,1500,1500,fill ="pink",width=6)

toptrends_label = tkinter.Label(window, text="Top Trends:", font=title_font, fg=labelFont, bg=background)
toptrends_label.grid(row=0, column=10, padx=9, pady=9, columnspan=5, sticky='w')
toptrends_box = Listbox(window, width=25, font="Constantia", bg=textarea, borderwidth=0)
toptrends_box.grid(row=1, column=10, padx=9, pady=9, sticky='nw')
toptrendsH_label = tkinter.Label(window, text="Top  Hashtags: ", font=title_font, fg=labelFont, bg=background)
toptrendsH_label.grid(row=3, column=10, padx=9, pady=9, columnspan=5, sticky='w')
toptrendH_box = Listbox(window, width=25, font="Constantia", bg=textarea, borderwidth=0)
toptrendH_box.grid(row=4, column=10, padx=9, pady=9, sticky='nw')


for i in range(10):
    if i < len(top_trends):
        toptrends_box.insert(i, top_trends[i])
        toptrends_box.config(fg=labelFont)
    if i < len(top_hashtags):
        toptrendH_box.insert(i, '#' + top_hashtags[i])
        toptrendH_box.config(fg=labelFont)



# canvas.grid()
# scrollbar.config(command=hashtag_box.yview())
window.mainloop()
