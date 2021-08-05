import time                           # time access
import datetime as datetime           # basic date and time info
from datetime import datetime
import os.path                       # pathname manipulation
import speech_recognition as sr      # speech recognition
import playsound                     # play audio files
import os                            # to interact with the system and files
import random                        # random
from gtts import gTTS                # google text to speech
import webbrowser                    # open browser
from urllib.request import urlopen   # to open URLs
from tkinter import *                # to develop GUI
import tkinter as tk
                   



div_color = "#ABB2B9"     # divider color - light grey
bg_color = "#17202A"    # backgtound color - dark blue
text_color = "#EAECEE" # text color - platinum

font = "Helvetica 14"   # text font
font_bold = "Helvetica 13 bold" # text font lable

# Main GUI

window = Tk()  # GUI window
window.title("Eli Voice Assistant") # window title
window.configure(width=470, height=480, bg=bg_color) # window configuration

global var  # global variable
var = StringVar()  # managing the value of the widget


# head label
head_label = Label(window, bg=bg_color, fg=text_color, # background color, text color
                           text="Welcome", font=font_bold, pady=5) # message, font, vertical margin
head_label.place(relwidth=1) # head label position
        
# top divider
top_divider = Label(window, width=450, bg=div_color) # width and background color
top_divider.place(relwidth=1, rely=0.07, relheight=0.012) # top divider position
        
# text widget
text_widget = Label(window, textvariable=var, width=20, height=2, bg=bg_color, fg=text_color,
                                font=font, padx=5, pady=5) # global variable, widht, background color, text color, font and margin
text_widget.place(relheight=0.745, relwidth=1, rely=0.08) # text widget position

# tiny divider
bottom_divider = Label(window, width=450, bg=div_color) # width and background color
bottom_divider.place(relwidth=1, rely=0.99, relheight=0.012) # bottom divider position


class asis:
    name = ''
    def setName(self, name):    # returning the name of the voice assistant
        self.name = name

class user:
    name = ''
    def setName(self, name):    # returning the name of the user
        self.name = name


def cmd_exists(terms):          # commands function
    for term in terms:          # looping through terms
        if term in voice_data:
            return True         



r = sr.Recognizer() # intializing the recogniser and recognizer calss

# Listening for audio and converting it into text

def record_audio(ask = False):
    with sr.Microphone() as source:  #using microphone as source 
        var.set("Listening...") # setting the message when the source is active to the global variable
        window.update() # updating the GUI window
        if ask:
            eli_speak(ask) # taking the user input
        audio = r.listen(source) # listen for the audio via source
        voice_data = '' # empty string
        var.set("Processing...") # setting the message when the input is processing to the global variable
        window.update() # updating the GUI window
        try:
            voice_data = r.recognize_google(audio) # convert audio to text
            
# Exception

        except sr.UnknownValueError:              
            eli_speak("Sorry I did not get that")   # Exception in case of unclear command
        except sr.RequestError:     
            eli_speak("Sorry, my speech server is down")  #recognizer is not connected 
        return voice_data # returning the string




#Getting the string and make a audio file to be played 

def eli_speak(audio_string):
    audio_string = str(audio_string) # audio string
    tts = gTTS(text=audio_string, lang='en') # text to speech(voice)
    r = random.randint(1,20000000) # randomly generating a file in the given range
    var.set(audio_string) # setting the audio_string to the global variable
    window.update() # updating the GUI window
    audio_file = 'audio' + str(r) + '.mp3' # naming the audio file
    tts.save(audio_file) # save the file as mp3
    playsound.playsound(audio_file) # play the audio file
    os.remove(audio_file) # remove audio file
   


# respond function taking the voice data from the source(microphone) 
def respond(voice_data): 

# 1: Greeting

    if cmd_exists(['hey','hi','hello']):    # recognizable commands
        greetings = ["Hello, how can I help you?", "I'm listening!", "How can I help you?", "Hello!"]  # greetings list
        window.update()   # updating the GUI window
        greet = greetings[random.randint(0,len(greetings)-1)]  # retrieving a random greeting from the list
        eli_speak(greet) # speaking the greeting

# 2: Name

    if cmd_exists(["what is your name", "what's your name", "tell me your name"]):  # recognizable commands
        window.update() # updating the GUI window
        eli_speak(f"My name is {asis_obj.name}! What is your name?")  # speaking its name

    if cmd_exists(["my name is"]):
        person_name = voice_data.split("is")[-1].strip() # splitting the string using a separator and returning a copy of the string
        window.update() # updating the GUI window
        user_obj.setName(person_name) # storing name in user object
        eli_speak(f"It is very nice to meet you {person_name}") # Eli greeting the user by speaking his name

# 3: Greeting question

    if cmd_exists(["how are you", "how are you doing", "how are you today"]):  # recognizable commands           
        window.update() # updating the GUI window
        eli_speak("I am very well, thank you for asking") # Eli responding to the question
        

# 4: Time

    if cmd_exists(["what time is it", "tell me the time", "what's the time"]):  # recognizable commands
       window.update()  # updating the GUI window
       end = "AM"   # time period
       final = "The time is " # variable assigning the voice output format
       now = datetime.now()  # retrieving current time information
       current_time = now.strftime("%H:%M") # time format 
       current_time = list(current_time) # current time list

       if len(current_time) > 4 and int(current_time[0] + current_time[1]) > 12: # checking if the list is longer than 4 characters and if the hour is after 12
            current_time[1] = int(str(current_time[0]) + str(current_time[1])) - 12 # changing the army time format to standard time format
            current_time[0] = ""

            end = 'PM' # time period

       # Adding the final time

       for i in current_time: # looping through current_time
           final += str(i) # adding the characters to the variable "final"

       final += end     # adding time information to the voice output format
       eli_speak(final) # Eli communicating the time information


  # 5: Google search 

    if cmd_exists(["Google search", "serch on Google", "Google", "open Google"]):   # recognizable commands
        window.update() # updating the GUI window
        google_search = record_audio("What do you want to search for on Google?") # taking the input from user
        url = 'https://google.com/search?q=' + google_search # searching the input on Google
        webbrowser.get().open(url)  # displaying the search result in a browser
        eli_speak("Here is what I found for " + google_search) # Eli communicating the result

  # 6: Google Maps Location search 

    if cmd_exists(["find location", "map search", "Google maps"]):   # recognizable commands
        window.update() # updating the GUI window
        location = record_audio("What is the location?") # taking the input from user
        url = 'https://google.nl/maps/place/' + location + "/&amp;" # searching the input on Google Maps
        webbrowser.get().open(url)  # displaying the search result in a browser
        eli_speak("Here is the location of " + location)  # Eli communicating the result

  # 7: Wikipedia Search

    if cmd_exists(["Wikipedia", "search on Wikipedia", "Wikipedia search"]):     # recognizable commands
        wiki_search = record_audio("What do you want to search for on Wikipedia?") # taking the input from user
        window.update() # updating the GUI window
        url = 'https://en.wikipedia.org/wiki/' + wiki_search    # searching the input on Wikipedia
        webbrowser.get().open(url)  # displaying the search result in a browser
        eli_speak("Here is what I found on Wikipedia for " + wiki_search)   # Eli communicating the result

  # 8 : YouTube Search 

    if cmd_exists(["open YouTube", "search on YouTube", "YouTube search"]):  # recognizable commands
        window.update() # updating the GUI window
        search_youtube = record_audio("What do you want to search for on YouTube?") # taking the input from user
        url = 'https://www.youtube.com/results?search_query=' + search_youtube  # searching the input on Wikipedia
        webbrowser.get().open(url)  # displaying the search result in a browser
        eli_speak("Here is what I found on Youtube for " + search_youtube)  # Eli communicating the result


# 9 : Mathematical operations

    if cmd_exists(["plus","minus","multiply","divide","power","+","-","*","/"]):  # recognizable commands
       opr = voice_data.split()[1] # splitting voice data and returning the element from position 1
       window.update()  # updating the GUI window

       # operator
       if opr == '+': 
           # splitting the integers in voice data using the elements from position 0 and 2
           eli_speak(int(voice_data.split()[0]) + int(voice_data.split()[2]))
       elif opr == '-': # operator
           eli_speak(int(voice_data.split()[0]) - int(voice_data.split()[2]))
       elif opr == 'multiply': # operator
           eli_speak(int(voice_data.split()[0]) * int(voice_data.split()[2]))
       elif opr == '/': # operator
           eli_speak(int(voice_data.split()[0]) / int(voice_data.split()[2]))
       elif opr == 'power': # operator
           eli_speak(int(voice_data.split()[0]) ** int(voice_data.split()[2]))
       else:
           eli_speak("Wrong Operator") # message for unrecognizible operator


#Entertainment Functionalities


# 10 : Playing a game

    if cmd_exists(["game", "I want to play a game", "Let's play a game"]):  # recognizable commands
       moves = ["rock", "paper", "scissor"] # available options
       voice_data = record_audio("Choose among rock paper or scissor") # getting the user input
      
    
       asis_move =random.choice(moves) # Eli choosing a random move from the list
       user_move =voice_data    # getting the user move

       eli_speak("I chose " + asis_move) # Eli communicating his move
       eli_speak("You chose " + user_move) # Eli communicating the user's move
       window.update()  # updating the GUI window
        

       if user_move == asis_move:   # draw condition
            eli_speak("The match is a draw") # Eli speaking the result
       elif user_move == "rock" and asis_move == "scissor": # rock-scissor condition
            eli_speak("You won") # Eli speaking the result
       elif user_move == "rock" and asis_move == "paper":   # rock-paper condition
            eli_speak("I won")  # Eli speaking the result
       elif user_move == "paper" and asis_move == "rock":   # paper-rock condition
            eli_speak("You won") # Eli speaking the result
       elif user_move == "paper" and asis_move == "scissor": # paper-scissor condition
            eli_speak("I won") # Eli speaking the result
       elif user_move == "scissor" and asis_move == "paper": # scissor-paper condition
            eli_speak("You won") # Eli speaking the result
       elif user_move == "scissor" and asis_move == "rock": # scissor-rock condition
            eli_speak("I won") # Eli speaking the result

       

# 11 : Telling Jokes

    if cmd_exists(["tell me a joke", "make me laugh", "tell me sonething funny", "tell me another joke"]):  # recognizable commands
        window.update() # updating the GUI window
        jokes = [
            "Here is a fun food fact: The first ever french \n fries were not cooked in France. \n They were cooked in Greece.",
            "How should you address an alligator in a vest? \n in-vest-a-gator",
            "What do you call a labrador that becomes a magician? \n A labracadabrador."] # jokes list
        tell_joke = jokes[random.randint(0,len(jokes)-1)] # retriving a random joke from the list
        eli_speak(tell_joke) # Eli telling the joke
        


             
# 12: Exit 

    if cmd_exists(["goodbye", "have a good day", "bye", "exit", "quit"]):   # recognizable commands
        window.update() # updating the GUI window
        eli_speak("Have a wonderful day!") # Eli saying goodbye
        exit(0)  # terminating the program 
   
      







time.sleep(1)   # wait for 1 second
asis_obj = asis() # assigning the class asis to the variable 
asis_obj.name = 'Eli' # name of the voice assistant
eli_speak("Hello! How may I assist you today?") # greeting at the start of program
user_obj = user() # assigning the class user to the variable 



# Voice assistant's loop
while 1:
    voice_data = record_audio() # assigning the voice input to voice_data
    respond(voice_data) # responding
 

window.mainloop() # GUI main loop