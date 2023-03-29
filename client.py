import json
import socket
from datetime import datetime

class Client:

    def __init__(self, host, port=5566):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        print("Client connected !")


    def send_signin(self, name,f_name, mail, password):
        signin_data = {
            "type": "signin",
            "name": name,
            "f_name": f_name,
            "password": password,
            "mail": mail
        }
        msg = json.dumps(signin_data)
        msg = msg.encode("utf8")
        self.client_socket.send(msg)
        response = self.client_socket.recv(1024)
        return response.decode("utf8")


    def send_login(self, username, password):
        login_data = {
            "type": "login",
            "username": username,
            "password": password
        }
        msg = json.dumps(login_data)
        msg = msg.encode("utf8")
        self.client_socket.send(msg)
        response = self.client_socket.recv(1024)
        return response.decode("utf8")


    def create_channel(self, usernameA, usernameB):
        discussion_data = {
            "type": "channel",
            "usernameA": usernameA,
            "usernameB": usernameB
        }
        msg = json.dumps(discussion_data)
        msg = msg.encode("utf8")
        self.client_socket.send(msg)

    def get_channelID(self, usernameA, usernameB):
        channelID_data = {
            "type": "channelID",
            "usernameA": usernameA,
            "usernameB": usernameB
        }
        msg = json.dumps(channelID_data)
        msg = msg.encode("utf8")
        self.client_socket.send(msg)
        response = self.client_socket.recv(1024)
        return response.decode("utf8")


    def askForHistory(self, usernameA, usernameB):
        channelID = self.channelID(usernameA, usernameB)
        history_data = {
            "type": "history",
            "channelID": channelID
        }
        msg = json.dumps(history_data)
        msg = msg.encode("utf8")
        self.client_socket.send(msg)
        response = self.client_socket.recv(1024)
        return response.decode("utf8")


    def send_message(self, userID, content, channelID):
        if len(content) <= 0:
            return print("Message cannot be empty !")
        else :
            message_data = {
                "type": "message",
                "content": content,
                "date": datetime.now().strftime("%d/%m/%Y"),
                "time": datetime.now().strftime("%H:%M:%S"),
                "userID": userID,
                "channelID": channelID
            }
            msg = json.dumps(message_data)
            msg = msg.encode("utf8")
            self.client_socket.send(msg)
            response = self.client_socket.recv(1024)
            return response.decode("utf8")


    def send_emoji(self, discussion, message, emoji):
        emoji_data = {
            "type": "emoji",
            "discussion": discussion,
            "message" : message,
            "emoji": emoji
        }
        msg = json.dumps(emoji_data)
        msg = msg.encode("utf8")
        self.client_socket.send(msg)
        response = self.client_socket.recv(1024)
        return response.decode("utf8")


    def receive_response(self):
        data = self.client_socket.recv(1024)
        return data.decode("utf8")


    def close(self):
        self.client_socket.close()


    def getUserID(self, mail):
        userID_data = {
            "type": "userID",
            "mail": mail
        }
        msg = json.dumps(userID_data)
        msg = msg.encode("utf8")
        self.client_socket.send(msg)
        response = self.client_socket.recv(1024)
        return response.decode("utf8")
    
client = Client("localhost")


"""
print(client.send_message(1, "Hello", 1))
check = (client.getUserID("a"))
print(check)
check = check.replace('[', '').replace(']', '')
print(check)
"""