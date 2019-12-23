import datetime
import requests
import json


class DataBase:  # {"Users":{"Name: "Rimve","Email": "rimve@gmail.com", "Password": "asd"}}
    def __init__(self, filename):
        self.filename = filename
        self.users = None
        self.file = None
        self.load()
        self.url = None
        self.auth_key = None

    def load(self):
        self.users = {}

        self.url = 'https://chat4hack.firebaseio.com/.json'
        self.auth_key = "UnhYnU6mTj1XxiLFPWMy77fXrXgew281oOHcNS0E"  # this is from firebase secret settings

        request = requests.get(self.url + "?auth=" + self.auth_key)
        data = str(request.json())[12:-4]
        data = data.replace("'}, '", "\n")
        data = data.splitlines()

        for line in data:  # getting all info about user from JSON structure and put into dict
            name = line.split("'")[0]
            password = line[::-1].split("'")[0]
            password = password[::-1]
            index = line.find("'")  # index for finding starting place of creating date
            create_date = line[index + 16:index + 26]
            line = line[index + 39:]
            email = line.split("'")[0]
            self.users[email] = (password, name, create_date)

    def get_user(self, email):
        if email in self.users:
            return self.users[email]
        else:
            return -1

    def add_user(self, email, password, name):
        if email.strip() not in self.users:
            self.users[email.strip()] = (password.strip(), name.strip(), DataBase.get_date())
            self.save()
            return 1
        else:
            print("Email exists already!")
            return -1

    def validate(self, email, password):
        if self.get_user(email) != -1:
            return self.users[email][0] == password
        else:
            return False

    def save(self):
        self.url = 'https://chat4hack.firebaseio.com/Users.json'
        data = list(self.users.items())[-1]  # user info is inserted into list
        data_result = '{"' + data[1][1] + '": {"Email": "' + data[0] + '","Password": "' + data[1][0] +\
                      '","Created": "' + data[1][2] + '"}}'

        to_database = json.loads(data_result)  # data_result string is inserted into to_database dict
        requests.patch(url=self.url, json=to_database)

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]