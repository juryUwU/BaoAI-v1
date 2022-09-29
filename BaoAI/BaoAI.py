#thư viện

from datetime import datetime
from datetime import date
from matplotlib import cm
from time import sleep
import random
from rich.progress import track
import webbrowser
import datetime
import pyttsx3
import speech_recognition
from pyowm import OWM
import pyowm
from pyowm.utils import config
from pyowm.utils import timestamps
import pyautogui
import subprocess
import os
import tkinter as tk
from tkinter import *
#tạo
def calculator():
    LARGE_FONT_STYLE = ("Arial", 40, "bold")
    SMALL_FONT_STYLE = ("Arial", 16)
    DIGITS_FONT_STYLE = ("Arial", 24, "bold")
    DEFAULT_FONT_STYLE = ("Arial", 20)

    OFF_WHITE = "#F8FAFF"
    WHITE = "#FFFFFF"
    LIGHT_BLUE = "#CCEDFF"
    LIGHT_GRAY = "#F5F5F5"
    LABEL_COLOR = "#25265E"


    class Calculator:
        def __init__(self):
            self.window = tk.Tk()
            self.window.geometry("375x667")
            self.window.resizable(0, 0)
            self.window.title("Calculator")

            self.total_expression = ""
            self.current_expression = ""
            self.display_frame = self.create_display_frame()

            self.total_label, self.label = self.create_display_labels()

            self.digits = {
                7: (1, 1), 8: (1, 2), 9: (1, 3),
                4: (2, 1), 5: (2, 2), 6: (2, 3),
                1: (3, 1), 2: (3, 2), 3: (3, 3),
                0: (4, 2), '.': (4, 1)
            }   
            self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
            self.buttons_frame = self.create_buttons_frame()

            self.buttons_frame.rowconfigure(0, weight=1)
            for x in range(1, 5):
                self.buttons_frame.rowconfigure(x, weight=1)
                self.buttons_frame.columnconfigure(x, weight=1)
            self.create_digit_buttons()
            self.create_operator_buttons()
            self.create_special_buttons()
            self.bind_keys()

        def bind_keys(self):
            self.window.bind("<Return>", lambda event: self.evaluate())
            for key in self.digits:
                self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

            for key in self.operations:
                self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

        def create_special_buttons(self):
            self.create_clear_button()
            self.create_equals_button()
            self.create_square_button()
            self.create_sqrt_button()

        def create_display_labels(self):
            total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                                fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
            total_label.pack(expand=True, fill='both')

            label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                            fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
            label.pack(expand=True, fill='both')

            return total_label, label

        def create_display_frame(self):
            frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
            frame.pack(expand=True, fill="both")
            return frame

        def add_to_expression(self, value):
            self.current_expression += str(value)
            self.update_label()

        def create_digit_buttons(self):
            for digit, grid_value in self.digits.items():
                button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                                borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
                button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

        def append_operator(self, operator):
            self.current_expression += operator
            self.total_expression += self.current_expression
            self.current_expression = ""
            self.update_total_label()
            self.update_label()

        def create_operator_buttons(self):
            i = 0
            for operator, symbol in self.operations.items():
                button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                                borderwidth=0, command=lambda x=operator: self.append_operator(x))
                button.grid(row=i, column=4, sticky=tk.NSEW)
                i += 1

        def clear(self):
            self.current_expression = ""
            self.total_expression = ""
            self.update_label()
            self.update_total_label()

        def create_clear_button(self):
            button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                            borderwidth=0, command=self.clear)
            button.grid(row=0, column=1, sticky=tk.NSEW)

        def square(self):
            self.current_expression = str(eval(f"{self.current_expression}**2"))
            self.update_label()

        def create_square_button(self):
            button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                            borderwidth=0, command=self.square)
            button.grid(row=0, column=2, sticky=tk.NSEW)

        def sqrt(self):
            self.current_expression = str(eval(f"{self.current_expression}**0.5"))
            self.update_label()

        def create_sqrt_button(self):
            button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                            borderwidth=0, command=self.sqrt)
            button.grid(row=0, column=3, sticky=tk.NSEW)

        def evaluate(self):
            self.total_expression += self.current_expression
            self.update_total_label()
            try:
                self.current_expression = str(eval(self.total_expression))

                self.total_expression = ""
            except Exception as e:
                self.current_expression = "Error"
            finally:
                self.update_label()

        def create_equals_button(self):
            button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                            borderwidth=0, command=self.evaluate)
            button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

        def create_buttons_frame(self):
            frame = tk.Frame(self.window)
            frame.pack(expand=True, fill="both")
            return frame

        def update_total_label(self):
            expression = self.total_expression
            for operator, symbol in self.operations.items():
                expression = expression.replace(operator, f' {symbol} ')
            self.total_label.config(text=expression)

        def update_label(self):
            self.label.config(text=self.current_expression[:11])

        def run(self):
            self.window.mainloop()


    if __name__ == "__main__":
        calc = Calculator()
        calc.run()
def weather():
    HEIGHT = 500
    WIDTH = 600

    def test_function(entry):
        print("This is the entry:", entry)

    # api.openweathermap.org/data/2.5/forecast?q={city name},{country code}
    # a4aa5e3d83ffefaba8c00284de6ef7c3

    def format_response(weather):
        try:
            name = weather['name']
            desc = weather['weather'][0]['description']
            temp = weather['main']['temp']

            final_str = 'City: %s \nConditions: %s \nTemperature (°F): %s' % (name, desc, temp)
        except:
            final_str = 'There was a problem retrieving that information'

        return final_str

    def get_weather(city):
        weather_key = 'a4aa5e3d83ffefaba8c00284de6ef7c3'
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {'APPID': weather_key, 'q': city, 'units': 'imperial'}
        response = requests.get(url, params=params)
        weather = response.json()

        label['text'] = format_response(weather)



    root = tk.Tk()

    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()

    background_image = tk.PhotoImage(file='BaoAI/landscape.png')
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    frame = tk.Frame(root, bg='#80c1ff', bd=5)
    frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

    entry = tk.Entry(frame, font=40)
    entry.place(relwidth=0.65, relheight=1)

    button = tk.Button(frame, text="Get Weather", font=40, command=lambda: get_weather(entry.get()))
    button.place(relx=0.7, relheight=1, relwidth=0.3)

    lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
    lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

    label = tk.Label(lower_frame)
    label.place(relwidth=1, relheight=1)

    root.mainloop()
    

def bmi():
    #Tạo ra của sổ
    a = Tk()
    a.title("Chương trình tính chỉ số đo cơ thể")
    a.geometry("300x400")
    a.attributes("-topmost", True)
    #tạo ra label1
    name1 = Label(a, font = ("Arial",10), text = "Nhập Chiều Cao(m): ")
    name1.place(x = 10, y = 10)
    #tạo ra label2
    name2 = Label(a, font = ("Arial",10), text = "Nhập Cân nặng(kg): ")
    name2.place(x = 10, y = 50)
    #tạo ra label3
    #tạo ra entry1
    entry = Entry(a, width = 15, font = ("Time New Roman",10))
    entry.place(x = 130, y = 10)
    entry.focus()
    #tạo ra entry2
    entry2 = Entry(a, width = 15, font = ("Time New Roman",10))
    entry2.place(x = 130, y = 50)
    #def dieukien():
        
    #Tạo ra button
    def anvao():
        name1 = Label(a , font = ("Arial",10), text =  "Chỉ số BMI của bạn là: " + str(float(entry2.get()) /( float(entry.get()) * 2)), fg="red")
        name1.place(x= 20, y = 110)
        name3 = Label(a, font = ("Arial",10), text = "BMI <18,5 : Bạn đang gầy")
        name3.place(x = 10, y = 140)
        #tạo ra label4
        name4 = Label(a, font = ("Arial",10), text = "BMI = 18,5 - 22,9: Bạn đang bình thường")
        name4.place(x = 10, y = 160)
        #tạo ra label5
        name5 = Label(a, font = ("Arial",10), text = "BMI >=23,0 : Bạn đang thừa cân")
        name5.place(x = 10, y = 180)
        #tạo ra label6
        name6 = Label(a, font = ("Arial",10), text = "BMI > 25,0 : Bạn đang béo phì")
        name6.place(x = 10, y = 200)
    but = Button(a, text = "Tính Toán", width = 10, height = 1, font = ("Time New Roman",10), command = anvao )
    but.place(x=105 , y = 80)

    a.mainloop()    
    

robot_ear = speech_recognition.Recognizer()
robot_mouth = pyttsx3.init()
robot_brain = ""
robot_mouth = pyttsx3.init()
voices = robot_mouth.getProperty('voices')
robot_mouth.setProperty('voice', voices[17].id)
robot_mouth.say("Hello World")
robot_mouth.runAndWait()
#python terminal colors| thông tin

#print("\033[36m-=-=-= \033[33mTRỢ LÝ ẢO \033[37mKHÁNH\033[35m(AI) \033[36m=-=-=-")
#print("\033[34mTrợ lý ảo KhánhAI \033[33mcode by \033[32mBảo Mondy")
#print("\033[33mRunning Troliaov2")
#print("\033[31mChạy trợ lý ảo...")
#for i in track(range(10), description="\033[31mĐang chạy......"):
#    print(f"\033[33mxong \033[32m{i}\033[33m%")
#   sleep(0.5)
while True:
    with speech_recognition.Microphone() as mic:
        print("\033[32mBảoAI: \033[37mtoi dang nghe...")
        audio = robot_ear.listen(mic)

    print("\033[32mBảoAI: \033[37mđang suy nghĩ...")

#trả lời câu hỏi


    try:
        you = robot_ear.recognize_google(audio)
    except:

        you = ""

    print("\033[33myou: \033[39m" + you)

    if you == "":
        robot_brain = "I can't hear you, try again"
    
    elif you == "hey robot":
        robot_brain = "what's up?"
    elif you == "hello":
        robot_brain = "hello Bao"
    
    elif you == "today":
        today = date.today()
        robot_brain = today.strftime("%B %d, %Y")
    
    elif you == "now":
        now = datetime.datetime.now()
        robot_brain = now.strftime("%I:%M:%p")
   
    elif you == "how do you think about me":
        robot_brain = "Bao is very handsome and smart"
   
    elif you == "how are you":
         robot_brain = "I'm fine thank you and you ?"
   
    elif you == "who are you":
        robot_brain = "I'm Bao's lover"
    
    elif you == "how old are you":
         robot_brain = "I'm 1 year old"
   
    elif "YouTube" in you:
        webbrowser.open('https://www.youtube.com')
        robot_brain = "open youtube"
    
    elif "Google" in you:
        webbrowser.open('https://www.google.com')
        robot_brain = "open google"
    
    elif "Spotify" in you:
        webbrowser.open('https://www.spotify.com')
        robot_brain = "open spotify"
    
    elif "Facebook" in you:
        webbrowser.open('https://www.facebook.com')
        robot_brain = "open facebook"
    
    elif "messenger" in you:
        webbrowser.open('https://www.messenger.com')
        robot_brain = "open messenger"
    
    elif "weather" in you:
        weather()
    elif "BMI" in you:
        bmi()
    elif "calculator" in you:
        calculator()
    elif "screenshot" in you:
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save(r'ảnh.png') 
        robot_brain = "the screen has been captured"


    #kết thúc
    
    elif you == "goodbye":
        robot_brain = "bye Bao"
        print("\033[32mKhanhAI: \033[39m" + robot_brain)
        robot_mouth = pyttsx3.init()
        robot_mouth.setProperty("rate", 150)
        robot_mouth.say(robot_brain)
        robot_mouth.runAndWait()
        break
    
    #các trường hợp còn lại

    else:
        robot_brain = "I can't answer your question"

    print("\033[32mBaoAI: \033[39m" + robot_brain)
   
    #giọng nói

    robot_mouth = pyttsx3.init()
    voices = robot_mouth.getProperty('voices')
    robot_mouth.setProperty('voice', voices[10].id)
    robot_mouth.say(robot_brain)
    robot_mouth.runAndWait()
