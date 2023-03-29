from client import Client
import tkinter as tk
import tkinter.ttk as ttk
import time
import json
import re
import sys
import signal

user = ""

# server connection
host_ip = input("Please enter the host IP.\n(if you used it in local, press 1)\n> ")
if host_ip == "1":
    host_ip = "localhost"

client = Client(host_ip)

root = tk.Tk()
root.title("Discord.py")
root.geometry("1200x800")
root.resizable(True, True)
root.configure(bg="#2C2F33")

# function

def detect_space(input):
    if " " in input:
        return False
    else:
        return True


def verif(name, f_name, mail, password, verify_password, frame_account):
    try :
        if entry_check(name) and entry_check(f_name) and email_check(mail) and password_check(password, verify_password):
            client.send_signin(name, f_name, mail, password)
            message_account(frame_account)
    except:
        error_message(frame_account)


def error_message(frame_account):
    label_error = tk.Label(frame_account, text="Error, check if you have on of these problems", bg="#2C2F33", fg="red",
                           font=("Arial Greek", 17))
    label_error.place(relx=0.20, rely=0.80)
    label_error_empty = tk.Label(frame_account, text="* Empty frame", bg="#2C2F33", fg="red",
                                 font=("Arial Greek", 15))
    label_error_empty.place(relx=0.20, rely=0.80)
    label_error_password = tk.Label(frame_account, text="* Password are not the same", bg="#2C2F33", fg="red",
                                    font=("Arial Greek", 15))
    label_error_password.place(relx=0.20, rely=0.85)
    label_error_number = tk.Label(frame_account, text="* Number in name or family name", bg="#2C2F33", fg="red",
                                  font=("Arial Greek", 15))
    label_error_number.place(relx=0.20, rely=0.90)
    label_error_mail = tk.Label(frame_account, text="* Wrong email", bg="#2C2F33", fg="red",
                                  font=("Arial Greek", 15))
    label_error_mail.place(relx=0.20, rely=0.95)
    frame_account.update()


def email_check(mail):
    regex = r"^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$"
    
    if re.match(regex, mail):
        return True
    else:
        return False


def password_check(password, verify_password):
    if password == verify_password:
        return True
    else:
        return False


def entry_check(entry):
    if entry == "":
        return False
    if any(char.isdigit() for char in entry):
        return False
    else:
        return True


# login

def login(mail, password, frame):
    result = client.send_login(mail, password)
    result = json.loads(result)
    if result["status"] == "ok":
        frame.destroy()
        home()
        client.getUserID(mail)
    else:
        pass

def create_account(frame):

    frame_account = tk.Frame(root, bg="#2C2F33")
    frame_account.place(relx=0.46, rely=0.6, anchor="center", height=500)

    label_name = tk.Label(frame_account, text="Name", bg="#2C2F33", fg="#FFFFFF", font=("Arial Greek", 20))
    label_name.grid(row=0, column=0)

    style = ttk.Style()
    style.configure("TEntry", foreground="2C2F33", font=("Arial Greek", 20))
    entry_name = ttk.Entry(frame_account, width=30, font=("Arial Greek", 20), style="TEntry",validate="key", validatecommand=(root.register(detect_space), "%P"))
    entry_name.grid(row=0, column=1)

    label_f_name = tk.Label(frame_account, text="Family name", bg="#2C2F33", fg="#FFFFFF", font=("Arial Greek", 20))
    label_f_name.grid(row=1, column=0, pady=30)

    entry_f_name = ttk.Entry(frame_account, width=30, font=("Arial Greek", 20), style="TEntry",validate="key", validatecommand=(root.register(detect_space), "%P"))
    entry_f_name.grid(row=1, column=1)

    label_mail = tk.Label(frame_account, text="Email", bg="#2C2F33", fg="#FFFFFF", font=("Arial Greek", 20))
    label_mail.grid(row=2, column=0)

    entry_mail = ttk.Entry(frame_account, width=30, font=("Arial Greek", 20), style="TEntry",validate="key", validatecommand=(root.register(detect_space), "%P"))
    entry_mail.grid(row=2, column=1)


    label_password = tk.Label(frame_account, text="Password  ", bg="#2C2F33", fg="#FFFFFF",font=("Arial Greek", 20))
    label_password.grid(row=3, column=0)

    entry_password = ttk.Entry(frame_account, width=30, font=("Arial Greek", 20), show="*", style="TEntry", validate="key", validatecommand=(root.register(detect_space), "%P"))
    entry_password.grid(row=3, column=1, pady=30)

    label_verify_password = tk.Label(frame_account, text="Verify Password  ", bg="#2C2F33", fg="#FFFFFF",font=("Arial Greek", 20))
    label_verify_password.grid(row=4, column=0)

    entry_verify_password = ttk.Entry(frame_account, width=30, font=("Arial Greek", 20), show="*", style="TEntry", validate="key", validatecommand=(root.register(detect_space), "%P"))
    entry_verify_password.grid(row=4, column=1)

    label_connexion = ttk.Button(frame_account, text="Create an account", width=30,padding=15, command=lambda:
    verif(entry_name.get(), entry_f_name.get(), entry_mail.get(), entry_password.get(),
          entry_verify_password.get(), frame_account))
    label_connexion.grid(row=5, column=1,pady=30)


def message_account(frame):
    frame_verification = tk.Frame(frame, bg="#2C2F33", width=700, height=600)
    frame_verification.place(relx=0.5, rely=0.5, anchor="center")
    label_validation = tk.Label(frame, text="Your account has been created", bg="#2C2F33", fg="green", font=("Arial Greek", 27))
    label_validation.place(relx=0.6, rely=0.2, anchor="center")
    frame.update()
    time.sleep(1.5)
    frame.destroy()


def error_login(frame):
    frame_verification = tk.Frame(frame, bg="#2C2F33", width=500, height=100)
    frame_verification.place(relx=0.5, rely=0.75, anchor="center")
    label_validation = tk.Label(frame_verification, text="Your email or password is incorrect", bg="#2C2F33", fg="red", font=("Arial Greek", 27))
    label_validation.pack()
    frame.update()
    time.sleep(1.5)
    frame_verification.destroy()


def connexion():
    frame_main = tk.Frame(root , bg="#2C2F33")
    frame_main.pack(expand=True, fill="both")

    # logo panel
    label_title = tk.Label(frame_main, text="Discord", bg="#2C2F33", fg="#FFFFFF", font=("Arial Greek", 50))
    label_title.pack(pady=70, anchor="center")
    # connexion panel

    frame_connexion = tk.Frame(frame_main, bg="#2C2F33", width=500, height=500)
    frame_connexion.place(relx=0.46, rely=0.47, anchor="center")

    label_pseudo = tk.Label(frame_connexion, text="Email", bg="#2C2F33", fg="#FFFFFF", font=("Arial Greek", 20))
    label_pseudo.grid(row=0, column=0)

    style = ttk.Style()
    style.configure("TEntry", foreground="2C2F33", font=("Arial Greek", 20))
    entry_pseudo = ttk.Entry(frame_connexion, width=30, font=("Arial Greek", 20), style="TEntry",validate="key", validatecommand=(root.register(detect_space), "%P"))
    entry_pseudo.grid(row=0, column=1, pady=3)

    label_password = tk.Label(frame_connexion, text="Password  ", bg="#2C2F33", fg="#FFFFFF",font=("Arial Greek", 20))
    label_password.grid(row=1, column=0 ,pady=30)

    entry_password = ttk.Entry(frame_connexion, width=30, font=("Arial Greek", 20), show="*", style="TEntry", validate="key", validatecommand=(root.register(detect_space), "%P"))
    entry_password.grid(row=1, column=1)

    label_connexion = ttk.Button(frame_connexion, text="Connection", width=30, padding=15,command=lambda: login(entry_pseudo.get(), entry_password.get(),frame_main))
    label_connexion.grid(row=2, column=1)


    # create account panel

    frame_create_account = tk.Frame(frame_main, bg="#2C2F33", width=500, height=500)
    frame_create_account.place(relx=0.46, rely=0.64, anchor="center")

    label_create_account = tk.Label(frame_create_account, text="Still not registred ?", bg="#2C2F33", fg="#FFFFFF", font=("Arial Greek", 10))
    label_create_account.grid(row=0, column=1)

    label_create_account = ttk.Button(frame_create_account, text="Create an account", width=20, command=lambda: create_account(frame_main))
    label_create_account.grid(row=0, column=2)


def signal_handler(sig, frame):
    # Fermer la connexion avec le serveur
    client.close()
    sys.exit(0)


def home():
    client
    frame_main = tk.Frame(root , bg="#2C2F33")
    frame_main.pack(expand=True, fill="both")
    frame_message = tk.Frame(frame_main, bg="#444654", width=900)
    frame_message.pack(anchor="ne", fill="y", expand=True)
    frame_message_entry = tk.Frame(frame_message, bg="#2C2F33", width=600, height=80, borderwidth=2, relief="groove")
    frame_message_entry.place(relx=0.5, rely=0.95, anchor="center")


def on_close():
    client.close()
    root.destroy()
    print("close")



root.protocol("WM_DELETE_WINDOW", on_close)
signal.signal(signal.SIGINT, signal_handler)

connexion()
root.mainloop()