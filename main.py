from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
from kivy.core.window import Window
import calendar
import time
from kivy.clock import Clock

Window.size = (800, 650)


class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1\
                and self.email.text.count(".") > 0:
            if self.password != "":  # password not blank
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "login"  # change window to login page
            else:
                invalid_form()
        else:
            invalid_form()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def login_btn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalid_login()

    def create_btn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
"""
    url = 'https://chat4hack.firebaseio.com/.json'

    def post(self, JSON):
        to_database = json.loads(JSON)
        requests.patch(url=self.url, json=to_database)

    auth_key = "UnhYnU6mTj1XxiLFPWMy77fXrXgew281oOHcNS0E"  # this is from firebase secret settings

    def get_data(self):
        request = requests.get(self.url + "?auth=" + self.auth_key)
        data = str(request.json())[12:-4]
        data = data.replace("'}, '", "\n")
        data = data.splitlines()

        users = {}
        for line in data:  # getting all info about user from JSON structure and put into dict 
            name = line.split("'")[0]
            password = line[::-1].split("'")[0]
            password = password[::-1]
            index = line.find("'") # index for finding starting place of creating date
            create_date = line[index+16:index+26]
            line = line[index+39:]
            email = line.split("'")[0]
            users[email] = (password, name, create_date)
"""


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    clndr = ObjectProperty(None)
    localtime = ObjectProperty(None)
    current = ""

    @staticmethod #rimve@gmail.com
    def logout():
        sm.current = "login"

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        clndr = calendar.month(2019, 11)
        Clock.schedule_interval(self.update_time, 1)

        self.n.text = "Account name: " + name
        self.email.text = "Account email: " + self.current
        self.created.text = "Account Created On: " + created
        self.clndr.text = clndr

    def update_time(self, dt):
        self.localtime.text = time.strftime("Time: %H:%M:%S")


class WindowManager(ScreenManager):
    pass


def invalid_login():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid username or password.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def invalid_form():
    pop = Popup(title='Invalid Form',
                content=Label(text='Please fill in all inputs with information.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class Chat4HackApp(App):
    def build(self):
        self.icon = 'images/ico.ico'
        return sm


if __name__ == "__main__":
    Chat4HackApp().run()
